from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Member


@receiver(post_save, sender=Member)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # only when new user is created
        subject = "Welcome to Library Management System 📚"
        message = f"""
Hi {instance.user.username},

Welcome to our Library Management System 🎉

Your account has been successfully created.

Happy Reading! 📖
Library Team
        """

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.user.email],
            fail_silently=False,
        )
