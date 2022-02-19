import random
import string
from hashlib import md5

from django.conf import settings
from django.core.mail import send_mail


def generate_random_string(length: int) -> str:
    """Сгенерировать прописную строку."""
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string.upper()


def send_confirmation_code(email: str, code: str) -> None:
    """Отправить код по указанному адресу."""
    send_mail(
        'Подтвердите регистрацию',
        f'Ваш confirmation_code:\n{code}',
        f'{settings.EMAIL_ADMIN}',
        [email],
        fail_silently=False,
    )


def get_hash(code: str) -> str or None:
    """Захешировать строку."""
    if not code:
        return None
    code = code.encode('utf-8')
    return md5(code).hexdigest()


def generate_code() -> dict:
    """Генерировать код и его хеш. Вернуть их в дикте."""
    code = generate_random_string(10)
    hash_str = get_hash(code)
    return {"code": code, "hash": hash_str}
