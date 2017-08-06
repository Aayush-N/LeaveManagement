from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .utils import unique_slug_generator
from .validators import validate_category
from django.conf import settings
from datetime import date


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

User = settings.AUTH_USER_MODEL
choices = (
    (1, ("CASUAL LEAVE")),
    (2, ("EARNED LEAVE")),
    (3, ("MATERNITY LEAVE")),
    (4, ("SPECIAL CASUAL LEAVE")),
    (5, ("RESTRICTED HOLIDAY"))
)

class LeaveType(models.Model):
	class Meta:
		verbose_name = ("Faculty Name")
	owner		= models.ForeignKey(User, default=1)
	name		= models.CharField(max_length=120, null=False, default="No name")
	CL 			= models.IntegerField(default=15, validators=[MaxValueValidator(15),MinValueValidator(0)])
	EL			= models.IntegerField(default=10, validators=[MaxValueValidator(10),MinValueValidator(0)])
	ML 			= models.IntegerField(default=132, validators=[MaxValueValidator(132),MinValueValidator(0)])
	SCL 		= models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
	RH			= models.IntegerField(default=2, validators=[MaxValueValidator(2),MinValueValidator(0)])
	timestamp	= models.DateTimeField(auto_now=True, auto_now_add=False, null=True)

	def __str__(self):
		return self.name

class TempLeaveType(models.Model):#on applying TempTable is updated, master table is untouched. On approval, temp value is copied onto master value
	class Meta:
		verbose_name = ("Temp Leaves")
	owner		= models.ForeignKey(User, default=1)
	name		= models.CharField(max_length=120, null=False, default="No name")
	TCL 		= models.IntegerField(default=0, validators=[MaxValueValidator(15),MinValueValidator(0)])
	TEL			= models.IntegerField(default=0, validators=[MaxValueValidator(10),MinValueValidator(0)])
	TML 		= models.IntegerField(default=0, validators=[MaxValueValidator(132),MinValueValidator(0)])
	TSCL 		= models.IntegerField(default=0, validators=[MaxValueValidator(100),MinValueValidator(0)])
	TRH			= models.IntegerField(default=0, validators=[MaxValueValidator(2),MinValueValidator(0)])
	timestamp	= models.DateTimeField(auto_now=True, auto_now_add=False, null=True)

	def __str__(self):
		return self.name
#when a leave is taken add its details to the below model
class LeaveTaken(models.Model):
	user 		= models.ForeignKey(User, default=1)
	category 	= models.IntegerField(choices = choices, default=1)
	dateStart	= models.DateField(auto_now=False, null=False, default=date.today())
	dateEnd		= models.DateField(auto_now=False, null=False, default=date.today())
	approval	= models.BooleanField(null=False, default=False)


	def __str__(self):
		return str(self.dateStart)

class UserProfile(models.Model):
    user 		= models.OneToOneField(User)
    designation = models.CharField(max_length=100, blank=False, default="Assistant Professor")
    birth_date 	= models.DateField(null=True, blank=True)
    hod			= models.CharField(max_length=35, blank=False, default="G Thippeswamy")
    dep			= models.CharField(max_length=3, blank=False, default="CSE")
    image 		= models.ImageField('profile picture', upload_to='static/profile/', null=False, blank=False, default='static/profile/default.png')

    def __unicode__(self):
        return 'Test'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''
