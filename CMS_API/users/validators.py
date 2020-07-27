from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.password_validation import MinimumLengthValidator
import re


class ValidateFileExtension(object):
    def __init__(self, document):
        if not document.name.endswith('.pdf'):
            raise ValidationError("Only PDF file is accepted")

