from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from platformapp.models import Threat, TrafficLog, Alert


class Command(BaseCommand):
    help = 'Demo maglumatlaryny döredýär'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')

        for i in range(1, 16):
            TrafficLog.objects.create(
                source_ip=f'192.168.1.{i}',
                destination_ip='10.0.0.10',
                protocol='tcp',
                bytes_transferred=3000 * i,
                is_anomaly=i % 5 == 0,
            )

        Threat.objects.get_or_create(title='SYN Flood synanyşygy', attack_type='ddos', severity=4, description='Köp sanly SYN paketleri.')
        Threat.objects.get_or_create(title='Galp login sahypasy', attack_type='phishing', severity=3, description='Phishing URL ýüze çykdy.')
        Threat.objects.get_or_create(title='Trojan ýerine ýetirildi', attack_type='malware', severity=5, description='Şübheli executable tapyldy.')

        Alert.objects.get_or_create(message='Ilkinji duýduryş döredildi.')

        self.stdout.write(self.style.SUCCESS('Demo maglumatlary taýýar.'))
