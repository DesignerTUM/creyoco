import asyncio
import json
import os
import shutil
import logging

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import IntegrityError
from django.db.models import signals
from django.dispatch import receiver

from django_autobahn.signals import message_received, signal_registrant
from exeapp.models import UserProfile
from exeapp.models import Package


log = logging.getLogger(__file__)


def create_debug_superuser(app, created_models, **kwargs):
    if settings.DEBUG and not getattr(settings, "TEST", False):
        SU_LOGIN = "admin"
        SU_PASSWORD = "admin"
        try:
            su = auth_models.User.objects.create_superuser(SU_LOGIN,
                                                           "admin@exe.org",
                                                           SU_PASSWORD)
            Package.objects.create(title="test", user=su)
            log.info("Created superuser {} with password {}".format(SU_LOGIN,
                                                                    SU_PASSWORD))
        except IntegrityError as error:
            log.error(str(error))


@receiver(signal=signals.post_save, sender=auth_models.User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile. \
            objects.create(user=instance)
        profile.save()
        try:
            os.makedirs(profile.media_path)
        except Exception as e:
            log.info("Folder for user {0} at {1} already exists.". \
                     format(profile, profile.media_path))


@receiver(signal=signals.pre_delete, sender=auth_models.User)
def user_pre_delete(sender, instance, **kwargs):
    profile = instance.profile
    try:
        shutil.rmtree(profile.media_path)
    except OSError as e:
        log.error(str(e))
    profile.delete()


# @signal_registrant.receiver_new("message")
# def message_received(sender, message, **kwargs):
#     log.info("Message: {}".format(message))

@signal_registrant.receiver_new("idevice_changed")
def handle_opened_idevice(sender, message, **kwargs):
    print("#" * 20)
    data =json.loads(message)
    idevice_id = data['idevice_id']
    status = data['status']
    print("Idevice %s is now %s" % (idevice_id, status))
