from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django import forms
from django.db.models import Q

from .models import Upload

import logging

logger = logging.getLogger("django.server")

class UploadForm(forms.ModelForm):
  class Meta:
    model = Upload
    fields = ["file"]

def index(request: HttpRequest):
  upload_form = UploadForm()
  upload_complete = False
  file = None
  files_to_process = list(Upload.objects.filter(~Q(state=Upload.UploadState.DELETED)).all())
      
  return render(request, 'dash-index.html', {
    "upload_form": upload_form,
    "upload_complete": upload_complete,
    "uploaded_file": file,
    "files_to_process": files_to_process
  })

def upload(request: HttpRequest):
  if request.method != "POST":
    return HttpResponse("must POST to endpoint", status=400)
  
  upload_form = UploadForm(request.POST, request.FILES)
  files_to_process = list(Upload.objects.filter(~Q(state=Upload.UploadState.DELETED)).all())
  
  if upload_form.is_valid():
    file = request.FILES["file"]
    logger.info("got file upload: %s", file)
    logger.info("saving file to disk now...")
    finished_form = upload_form.save()
    logger.info(str(finished_form.file))
    upload_complete = True
    
  return render(request, 'dash-index.html', {
    "upload_form": upload_form,
    "upload_complete": upload_complete,
    "uploaded_file": file,
    "files_to_process": files_to_process,
    "reload": True
  })
  
def process(request: HttpRequest):
  pk = request.GET.get('pk', None)
  if pk is None:
    return HttpResponse("must have pk query param", status=400)

  upload = Upload.objects.get(pk=pk)
    
  return render(request, 'dash-processing.html', {
    "upload": upload
  })

def delete(request: HttpRequest):
  pk = request.GET.get('pk', None)
  if pk is None:
    return HttpResponse("must have pk query param", status=400)

  num_updated = Upload.objects.filter(pk=pk).update(state=Upload.UploadState.DELETED)
  logger.info(f"set deletion for {num_updated} objects")
    
  upload_form = UploadForm()
  upload_complete = False
  file = None
  files_to_process = list(Upload.objects.filter(~Q(state=Upload.UploadState.DELETED)).all())
      
  return render(request, 'dash-index.html', {
    "upload_form": upload_form,
    "upload_complete": upload_complete,
    "uploaded_file": file,
    "files_to_process": files_to_process,
    "reload": True
  })