from django.core.mail import send_mail


def send_email(subject, message, recipient_list):
    from_email = "clubhouse@clubhouse.com"
    send_mail(subject=subject, message=message, from_email=from_email,
              recipient_list=recipient_list, fail_silently=False)
