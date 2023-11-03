from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

USER_TYPE_CHOICES = (
    ('Customer', 'Customer'),
    ('Admin', 'Admin'),
)


class UserManager(BaseUserManager):
    def create_user(self, password=None, **kwargs):
        # email = self.normalize_email(email)
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Store User account details.
    """
    # Use either of the username fields below:

    phone_no = models.CharField(
        'phone number',
        max_length=10,  # Adjust the max length as needed for your specific use case
        primary_key=True,
        help_text='Required. Enter a valid phone number.',
        validators=[
            validators.RegexValidator(
                r'^\+?1?\d{9,10}$',  # Modify the regex pattern as needed
                'Enter a valid phone number. It should contain only digits and an optional "+" at the beginning.',
            ),
        ],
        error_messages={
            'unique': 'A user with that phone number already exists.',
        },
    )
    password = models.CharField(
        'password',
        max_length=128,
        validators=[validate_password],
        null=True,
        blank=True
    )

    first_name = models.CharField('First name', max_length=30, blank=True)
    last_name = models.CharField('Last name', max_length=30, blank=True)
    dob = models.DateTimeField("Date of Birth",null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0])
    type = models.CharField("User Type", max_length=10, choices=USER_TYPE_CHOICES, default=USER_TYPE_CHOICES[0][0])

    # models related to Django admin panel
    is_active = models.BooleanField('active', default=True,
                                    help_text=('Designates whether this user should be treated as '
                                               'active.  Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text=('Designates whether the user can log into this admin '
                                              'site.'))

    objects = UserManager()

    # Modify USERNAME_FIELD and REQUIRED_FIELDS as required.
    USERNAME_FIELD = 'phone_no'

    # REQUIRED_FIELDS = ['phone_no']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        permissions = (
        )
        ordering = ['date_joined']

    # Use Either one of __str__ methods.
    def __str__(self):
        return '{phone_no}'.format(phone_no=self.phone_no)

    def calculate_age(self, *args, **kwargs):
        """
        Sends an email to this User.
        """
        pass


class UserEmail(models.Model):
    email = models.EmailField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user_email'

