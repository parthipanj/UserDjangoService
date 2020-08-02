import uuid

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    username_validator = UnicodeUsernameValidator()

    class Gender(models.TextChoices):
        MALE = 'M', _('MALE')
        FEMALE = 'F', _('FEMALE')
        TRANSGENDER = 'T', _('TRANSGENDER')
        OTHERS = 'O', _('OTHERS')

        __empty__ = _('(Unknown)')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=False,
        null=False
    )
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=150, blank=True)
    email = models.EmailField(_('Email Address'), blank=True)
    mobile_number = models.CharField(_('Mobile Number'), blank=True, max_length=20)
    password = models.CharField(_('password'), max_length=128, blank=False, null=False)
    avatar = models.ImageField(_('avatar'), blank=True)
    dob = models.DateField(_('Date of Birth'), blank=True, null=True)
    gender = models.CharField(_('gender'), blank=True, max_length=1, choices=Gender.choices)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), default=timezone.now)

    class Meta:
        app_label = _('users')
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-created',)
