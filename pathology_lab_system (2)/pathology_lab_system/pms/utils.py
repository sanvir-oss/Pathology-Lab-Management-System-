# pms/utils.py (Adapt this function or create a new one)

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_report_ready_email(booking):
    """
    Sends an HTML notification to the user that their report is ready.
    """
    context = {
        'booking': booking,

    }

    # Render the HTML content (create a template named 'report_ready_email.html')
    html_message = render_to_string('pms/email/report_ready_email.html', context)

    subject = f"✅ Your LabXpert Report is Ready (ID: #{booking.id})"
    to_email = booking.user.email

    email = EmailMessage(
        subject,
        html_message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
    )

    email.content_subtype = 'html'

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False