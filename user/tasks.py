import celery
from django.utils.crypto import get_random_string



# Celery Task for Email Verification
@celery.shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    token = get_random_string(length=32)
    redis_instance.setex(f'verification_token:{token}', 3600, user.id)  # Expiry: 1 hour
    verification_link = f"http://localhost:8000/api/users/verify/?token={token}"
    send_mail(
        'Verify Your Account',
        f'Click the link to verify your account: {verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )