from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import re


class UppercaseValidator(object):
    def __init__(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(_("The password must contain at least 1 uppercase letter, A-Z."),
                                  code='password_no_upper')

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )

# def UppercaseValidator(password):
#     if not re.search(r"[A-Z]+", password):
#         raise ValidationError(_("The password must contain at least 1 uppercase letter, A-Z."),
#                               code='password_no_upper')

class LowercaseValidator(object):
    def __init__(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(_("The password must contain at least 1 lowercase letter, a-z."),
                                  code='password_no_lower')

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class NumberValidator(object):
    def __init__(self, min_length=0):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_length:
            raise ValidationError(
                _("The password must contain at least %(min_length)d digit(s), 0-9."),
                code='password_no_number',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d digit(s), 0-9." % {'min_length': self.min_length}
        )


class ValidateFileExtension(object):
    def __init__(self, document):
        if not document.name.endswith('.pdf'):
            raise ValidationError("Only PDF file is accepted")


class OnlyNumberValidator(object):
    def __init__(self, pincode, user=None):
        if not re.findall('[0-9]', pincode):
            raise ValidationError(_("The pincode must contain only integer."), code='field_numeric')

    def get_help_text(self):
        return _(
            "The pincode must contain only integer."
        )
