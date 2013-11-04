from django.shortcuts import render
from models import Background


def index (request):
    bg = Background.objects.latest()
    return render(request, 'index.html', {'href': bg.image_file.url})

    