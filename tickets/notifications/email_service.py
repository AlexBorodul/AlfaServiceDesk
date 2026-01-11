from django.core.mail import EmailMessage
from django.conf import settings


class EmailNotificationService:

    @staticmethod
    def send(subject: str, message: str, recipient: str, files=None):
        """
        files — список UploadedFile (request.FILES.getlist)
        """
        if not recipient:
            return

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        if files:
            for f in files:
                email.attach(
                    f.name,
                    f.read(),
                    f.content_type
                )

        email.send(fail_silently=False)