import os
import urllib

from django.db import models
from django.core.files import File
from django.dispatch import receiver

from sterexy_project import settings



class Background(models.Model):

    class Meta:
        get_latest_by = 'im_date'

    image_file = models.ImageField(upload_to='background')
    image_url = models.URLField()
    im_date = models.DateTimeField()

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0]))
                    )
            self.save()

@receiver(models.signals.post_delete, sender=Background)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Background` object is deleted.
    """
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)
