from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(Category, self).delete()

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(Priority, self).delete()

    def __str__(self):
        return self.name


class Task(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def clean(self):
        # Валидация поля completed и status
        if self.completed and self.status != 'completed':
            raise ValidationError("If 'completed' is True, 'status' must be 'completed'.")
        if not self.completed and self.status == 'completed':
            raise ValidationError("If 'status' is 'completed', 'completed' must be True.")

    def save(self, *args, **kwargs):
        # Синхронизация поля status с completed
        if self.completed:
            self.status = 'completed'
            if not self.completed_at:
                self.completed_at = timezone.now()
        else:
            if self.status == 'completed':
                self.completed = True
                if not self.completed_at:
                    self.completed_at = timezone.now()
            elif self.status != 'completed':
                self.completed_at = None

        super(Task, self).save(*args, **kwargs)

    def soft_delete(self):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(Task, self).delete()

    def __str__(self):
        return self.title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
