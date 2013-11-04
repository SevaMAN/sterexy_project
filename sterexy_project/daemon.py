import urllib2
import lxml.html
import time

from datetime import datetime
from sterexy.models import Background
from django.core.exceptions import ObjectDoesNotExist

APOD = 'http://apod.nasa.gov/apod/'


def checkbg():
    page = urllib2.urlopen(APOD)
    doc = lxml.html.document_fromstring(page.read())
    href = doc.xpath('/html/body/center[1]/p[last()]/a')[0].get('href')
    picdate = doc.xpath('/html/body/center[1]/p[last()]')[0].text_content()
    picdate = time.strptime(picdate.strip(), "%Y %B %d")

    try:
        prevbg = Background.objects.latest()
    except ObjectDoesNotExist:
        prevbg = None

    bg = Background(image_url=APOD + href, im_date=time.strftime("%Y-%m-%d", picdate))
    if prevbg is None:
        bg.get_remote_image()
    elif prevbg.im_date < datetime.fromtimestamp(time.mktime(picdate)):
        prevbg.delete()
        bg.get_remote_image()

    return True

if __name__ == '__main__':
    checkbg()