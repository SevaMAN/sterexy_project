from django.shortcuts import render
import urllib2
import lxml.html

def index (request):
    page = urllib2.urlopen('http://apod.nasa.gov/apod/')
    doc = lxml.html.document_fromstring(page.read())
    href = doc.xpath('/html/body/center[1]/p[last()]/a')[0].get('href')
    return render(request, 'index.html', {'href':href})
    