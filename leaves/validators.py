from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

CATEGORIES = ['CASUAL LEAVE', 'EARNED LEAVE', 'MATERNITY LEAVE', 'SPECIAL CASUAL LEAVE', 'RESTRICTED HOLIDAY']

def validate_category(value):
	value = value.upper()
	if not value in CATEGORIES:
		raise ValidationError(value  + " is not a valid leave type")