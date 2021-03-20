from users.utils import generate_key
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, EmailAddress, EmailConfirmation, Profile


@receiver(post_save, sender=User)
def save_emailaddress(sender, instance, created, *args, **kwargs):
    if created:
        email_addr = EmailAddress.objects.create(
            user=instance, 
            email=instance.email
        )
        email_addr.save()
        email_conf = EmailConfirmation.objects.create(
            email=email_addr,
            key=generate_key(instance.email)
        )
        email_conf.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
