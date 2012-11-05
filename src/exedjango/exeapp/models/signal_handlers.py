from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.dispatch import receiver


from exeapp.models import UserProfile
import os
import shutil
from exeapp.models import Package

def create_debug_superuser(app, created_models, **kwargs):
    if settings.DEBUG and not getattr(settings, "TEST", False):
        SU_LOGIN = "admin"
        SU_PASSWORD = "admin"
        su = auth_models.User.objects.create_superuser(SU_LOGIN, "admin@exe.org",
                                                  SU_PASSWORD)
        Package.objects.create(title="test", user=su)
        print "Created superuser %s with password %s" % (SU_LOGIN, SU_PASSWORD)

if settings.DEBUG and not getattr(settings, "TEST", False):
    print "DISABLING SUPERUSER CREATIONG"
    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_debug_superuser,
            sender=auth_models, dispatch_uid='common.models.create_testuser')
    
@receiver(signal=signals.post_save, sender=auth_models.User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.\
                    objects.create(user=instance)
        profile.save()
        try:
            os.mkdir(profile.media_path)
        except Exception, e:
            if not getattr(settings, "TEST", False):
                print "Folder for user {0} at {1} was not created".\
                    format(profile, profile.media_path)
                raise e
        
@receiver(signal=signals.pre_delete, sender=auth_models.User)
def user_pre_delete(sender, instance, **kwargs):
    profile = instance.userprofile
    shutil.rmtree(profile.media_path)
    profile.delete()
        

    