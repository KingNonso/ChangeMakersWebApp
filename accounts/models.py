from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='members')
    other_name = models.CharField('Other name', max_length=255, blank=True, null=True)
    primary_phone = models.CharField('Primary Phone Number', max_length=255, blank=True, null=True, help_text="Enter your WhatsApp Number here")
    secondary_phone = models.CharField('Secondary Phone Number', max_length=255, blank=True, null=True)
    dob = models.DateField('Date of Birth', help_text='Enter your date of birth')
    address = models.CharField('Home Address', max_length=255, blank=True, null=True)
    work = models.CharField('Workplace/ Office', max_length=255, blank=True, null=True)
    job = models.CharField('Position/ Title',max_length=255, blank=True, null=True)
    bio = models.TextField('Professional Bio/ Citation')
    photo = models.ImageField('Profile Picture', blank=True, null=True, upload_to='accounts/' )
    gender = models.BooleanField('Gender', choices=((0,'Male'), (1,'Female')), max_length=50, default=1)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Member profile'
        verbose_name_plural = 'Member Profiles'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        if self.user.first_name:
            first_name = self.user.first_name
        else:
            first_name = ''
        if self.user.last_name:
            last_name = self.user.last_name
        else:
            last_name = ''
        if self.other_name:
            other_name = self.other_name
        else:
            other_name = ''

        full_name = '%s, %s %s' % (last_name, first_name, other_name)
        return full_name.strip()
    
    full_name = property(get_full_name)

    def get_abbrev_name(self):
        '''
        Returns the Abbreivated name with initials
        '''
        if self.user.first_name:
            first_name = self.user.first_name
            first_name = first_name[0].capitalize()+'.'
        else:
            first_name = ''
        if self.user.last_name:
            last_name = self.user.last_name.capitalize()
        else:
            last_name = ''
        if self.other_name:
            other_name = self.other_name
            other_name = other_name[0].capitalize()+'.'
        else:
            other_name = ''

        full_name = '%s %s %s' % (first_name, other_name, last_name)
        return full_name.strip()

    def get_phone_number(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        if self.primary_phone:
            primary_phone = self.primary_phone
        else:
            primary_phone = ''
        if self.secondary_phone:
            secondary_phone = ", "+ self.secondary_phone
        else:
            secondary_phone = ''

        phone = '%s %s' % (primary_phone, secondary_phone)
        return phone.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.user.first_name

    def get_username(self):
        '''
        Returns the short name for the user.
        '''
        return self.user.username

    def get_absolute_url(self):
        return reverse('membership:detail', args=[self.user.username])

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this Member.
        '''
        send_mail(subject, message, from_email, [self.user.email], **kwargs)

    def get_is_active(self):
        if self.user.is_active:
            return 'Active'
        else:
            return 'Inactive'
    def get_is_admin(self):
        if self.user.is_admin:
            return True
        else:
            return False

