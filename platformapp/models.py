from django.db import models
from django.contrib.auth.models import User


class TrafficLog(models.Model):
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    protocol = models.CharField(max_length=20)
    bytes_transferred = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anomaly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.source_ip} -> {self.destination_ip} ({self.protocol})"


class Threat(models.Model):
    ATTACK_TYPES = [
        ('ddos', 'DDoS'),
        ('phishing', 'Phishing'),
        ('malware', 'Malware'),
        ('other', 'Beýleki'),
    ]
    title = models.CharField(max_length=120)
    attack_type = models.CharField(max_length=20, choices=ATTACK_TYPES)
    severity = models.IntegerField(default=1)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Alert(models.Model):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AIModelRecord(models.Model):
    ALGORITHMS = [
        ('rf', 'Random Forest'),
        ('nn', 'Neural Network'),
        ('lr', 'Logistic Regression'),
    ]
    name = models.CharField(max_length=120)
    algorithm = models.CharField(max_length=2, choices=ALGORITHMS)
    accuracy = models.FloatField(default=0)
    precision = models.FloatField(default=0)
    recall = models.FloatField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    trained_at = models.DateTimeField(auto_now_add=True)


class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
