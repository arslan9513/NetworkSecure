import csv
import io
import json
from datetime import timedelta

import jwt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import SignUpForm, TrafficUploadForm, UserForm
from .models import AIModelRecord, Alert, Threat, TrafficLog, UserActionLog
from .services.ml_service import train_algorithm


def _log_action(request, action):
    if request.user.is_authenticated:
        UserActionLog.objects.create(user=request.user, action=action)


def home(request):
    threats = Threat.objects.order_by('-detected_at')[:5]
    return render(request, 'platformapp/home.html', {
        'threat_count': Threat.objects.count(),
        'log_count': TrafficLog.objects.count(),
        'threats': threats,
    })


def register_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        login(request, user)
        _log_action(request, 'Ulgama ýazylmak')
        return redirect('dashboard')
    return render(request, 'platformapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            _log_action(request, 'Ulgama girmek')
            return redirect('dashboard')
        messages.error(request, 'Ulanyjy ady ýa-da açar söz nädogry.')
    return render(request, 'platformapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    recent_logs = TrafficLog.objects.order_by('-created_at')[:10]
    threat_levels = Threat.objects.values('severity').annotate(total=Count('id')).order_by('severity')
    alerts = Alert.objects.order_by('-created_at')[:10]
    return render(request, 'platformapp/dashboard.html', {
        'recent_logs': recent_logs,
        'threat_levels': list(threat_levels),
        'alerts': alerts,
    })


@login_required
def traffic_analysis(request):
    form = TrafficUploadForm(request.POST or None, request.FILES or None)
    parsed = []

    if request.method == 'POST' and form.is_valid():
        f = form.cleaned_data['file']
        text = f.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            log = TrafficLog.objects.create(
                source_ip=row.get('source_ip', '0.0.0.0'),
                destination_ip=row.get('destination_ip', '0.0.0.0'),
                protocol=row.get('protocol', 'tcp'),
                bytes_transferred=int(row.get('bytes_transferred', 0)),
                is_anomaly=int(row.get('bytes_transferred', 0)) > 50000,
            )
            parsed.append(log)
        messages.success(request, f'{len(parsed)} ýazgy üstünlikli ýüklendi.')
        _log_action(request, 'Trafik loglary ýüklendi')

    return render(request, 'platformapp/traffic_analysis.html', {
        'form': form,
        'logs': TrafficLog.objects.order_by('-created_at')[:20],
    })


@login_required
def ai_model_management(request):
    if request.method == 'POST':
        algorithm = request.POST.get('algorithm', 'rf')
        result = train_algorithm(algorithm)
        AIModelRecord.objects.create(
            name=f'Model-{timezone.now().strftime("%Y%m%d%H%M%S")}',
            algorithm=algorithm,
            accuracy=result.accuracy,
            precision=result.precision,
            recall=result.recall,
            created_by=request.user,
        )
        messages.success(request, 'Model tälimi tamamlandy.')
        _log_action(request, f'Model tälimi: {algorithm}')

    models = AIModelRecord.objects.order_by('-trained_at')[:10]
    return render(request, 'platformapp/ai_models.html', {'models': models})


@login_required
def alerts_view(request):
    attack_type = request.GET.get('type')
    threats = Threat.objects.order_by('-detected_at')
    if attack_type:
        threats = threats.filter(attack_type=attack_type)
    return render(request, 'platformapp/alerts.html', {'threats': threats[:100]})


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_management(request):
    users = User.objects.all().order_by('id')
    return render(request, 'platformapp/users.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_staff)
def user_edit(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ulanyjy maglumatlary täzelendi.')
        return redirect('user_management')
    return render(request, 'platformapp/user_edit.html', {'form': form, 'user_obj': user_obj})


@login_required
def reports_view(request):
    if request.GET.get('format') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="threat_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Ady', 'Hüjüm görnüşi', 'Howplulyk', 'Wagty'])
        for t in Threat.objects.order_by('-detected_at')[:500]:
            writer.writerow([t.title, t.attack_type, t.severity, t.detected_at.isoformat()])
        return response

    return render(request, 'platformapp/reports.html', {
        'threats': Threat.objects.order_by('-detected_at')[:50],
    })


@login_required
def settings_view(request):
    if request.method == 'POST':
        messages.success(request, 'Sazlamalar ýatda saklandy (demo).')
    return render(request, 'platformapp/settings.html')


def api_stats(request):
    data = {
        'logs': TrafficLog.objects.count(),
        'threats': Threat.objects.count(),
        'alerts': Alert.objects.count(),
        'last_24h': Threat.objects.filter(detected_at__gte=timezone.now() - timedelta(hours=24)).count(),
    }
    return JsonResponse(data)


def api_detect(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Diňe POST rugsat edilýär'}, status=405)
    payload = json.loads(request.body.decode('utf-8'))
    bytes_tx = int(payload.get('bytes_transferred', 0))
    anomaly = bytes_tx > 50000
    if anomaly:
        threat = Threat.objects.create(
            title='Awto-duýduryş',
            attack_type='other',
            severity=3,
            description='Uly trafik mukdary sebäpli şübheli hereket.',
        )
        Alert.objects.create(message=f'Täze howp: {threat.title}')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'alerts',
            {
                'type': 'push_alert',
                'data': {'habar': threat.title, 'dereje': threat.severity}
            }
        )
    return JsonResponse({'anomaly': anomaly})


def api_token(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Diňe POST rugsat edilýär'}, status=405)
    data = json.loads(request.body.decode('utf-8'))
    user = authenticate(request, username=data.get('username'), password=data.get('password'))
    if not user:
        return JsonResponse({'error': 'Nädogry maglumat'}, status=401)
    token = jwt.encode({'sub': user.username, 'exp': timezone.now() + timedelta(hours=8)}, settings.SECRET_KEY, algorithm='HS256')
    return JsonResponse({'token': token})
