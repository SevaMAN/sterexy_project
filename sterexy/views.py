from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import lxml.html
from models import Background
import time
from time import mktime
from datetime import datetime

def index (request):
    page = urllib2.urlopen('http://apod.nasa.gov/apod/')
    doc = lxml.html.document_fromstring(page.read())
    href = doc.xpath('/html/body/center[1]/p[last()]/a')[0].get('href')

    bg = Background(image_url='http://apod.nasa.gov/apod/'+href)
    picdate = doc.xpath('/html/body/center[1]/p[last()]')[0].text_content().replace('\n','')
    picdate = time.strptime(picdate.strip(), "%Y %B %d")
    bg.im_date = time.strftime("%Y-%m-%d",picdate)

    prevbg = None

    try:
        prevbg = Background.objects.latest()
    except ObjectDoesNotExist:
        pass

    if prevbg is not None:
        if prevbg.im_date.replace(tzinfo=None) < datetime.fromtimestamp(mktime(picdate)):
            prevbg.delete()
            bg.get_remote_image()
    else:
        bg.get_remote_image()

    return render(request, 'index.html', {'href':href})
    