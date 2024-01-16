import os

from django.core.exceptions import ValidationError


def allow_images_only_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions = ['png', 'jpg', 'jpeg']
    seperator = ' or '
    valid_options = seperator.join(valid_extensions)
    if not ext.lower() in valid_extensions:
        raise ValidationError("unsupported file type allowed " + valid_options)
