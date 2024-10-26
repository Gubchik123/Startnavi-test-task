from typing import NoReturn

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_content_(text: str) -> None | NoReturn:
    """Validate that the given text does not contain censored words."""
    text = text.lower()
    for censored_word in settings.CENSORED_WORDS:
        if censored_word in text:
            raise ValidationError(
                f"Content contains censored word '{censored_word}' !"
            )
