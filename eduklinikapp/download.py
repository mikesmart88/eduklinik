from django.http import FileResponse, Http404
from django.conf import settings
import os

def download_zip(request):
    zip_file_path = os.path.join(settings.BASE_DIR, '/media/')