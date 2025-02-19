from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
# Signals
@receiver(m2m_changed, sender=Event.participants.through)
def notify_participant_on_event_registration(sender, instance, action, pk_set, **kwargs):

    if action == 'post_add' and pk_set:
        users = User.objects.filter(pk__in=pk_set)
        for user in users:
            email = user.email
            username = user.username
        try:
            send_mail(
                f"Registration Confirmation for {instance.name}",
                f"Hello {username},\n\n"
                f"Thank you for registering for the event: {instance.name}.\n\n"
                "We look forward to seeing you there!\n"
                "Best regards,\n"
                "Event Management Team",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
            print("Email Send Successfully 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀")
        except Exception as e:
            print(f"Filed to send email to {instance}: {str(e)} 🚀🚀🚀")
            
        
            