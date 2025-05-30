from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# SENDING MAIL WHILE REGISTERING
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\n Please activate your account by clicking the link below: \n {activation_url}\n\n Thank You'
        recipient_list = [instance.email]
        try:
            send_mail(subject,  message, settings.EMAIL_HOST_USER, recipient_list)
            print("Email Send Successfully 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
        except Exception as e:
            print(f"Filed to send email to {instance.email}: {str(e)} 🚀🚀🚀")
            
# SETTING DEFAULT ROLE WHILE REGISTERING
@receiver(post_save, sender=User)         
def assign_role(sender, instance, created, **kwargs):
    if created:
        participants, createdgroup = Group.objects.get_or_create(name='participants')
        instance.groups.add(participants)
        instance.save()
            
            
    