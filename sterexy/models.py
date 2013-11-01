from django.db import models
from django.core.files import File
import os
import urllib


class Background(models.Model):

    class Meta:
        get_latest_by = 'im_date'

    image_file = models.ImageField(upload_to='sterexy/static/images/')
    image_url = models.URLField()
    im_date = models.DateField()

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                    'background.jpg',
                    File(open(result[0]))
                    )
            self.save()
