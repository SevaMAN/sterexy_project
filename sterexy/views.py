from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import lxml.html
from models import Background
import time

def index (request):
    page = urllib2.urlopen('http://apod.nasa.gov/apod/')
    doc = lxml.html.document_fromstring(page.read())
    href = doc.xpath('/html/body/center[1]/p[last()]/a')[0].get('href')

    try:
        a = Background.objects.latest()
        a.delete()
    except ObjectDoesNotExist:
        bg = Background(image_url='http://apod.nasa.gov/apod/'+href)
        picdate = doc.xpath('/html/body/center[1]/p[last()]')[0].text_content().replace('\n','')
        picdate = time.strptime(picdate, "%Y %B %d")
        bg.im_date = time.strftime("%Y-%m-%d",picdate)
        bg.get_remote_image()

    return render(request, 'index.html', {'href':href})
    