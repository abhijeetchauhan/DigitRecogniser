from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from ml import predictDigit

def uploadImage(request):
    if request.method == "POST":
      form = ImageUploadForm(request.POST, request.FILES)
      if  form.is_valid():
          form = form.save(commit= False)
          form.result = -100
          form.correct = False
          form.save()
          no = predictDigit(form.image.path)
          return HttpResponse(no)
    else:
        form = ImageUploadForm()
    return render(request, 'digitRecognizer/form.html', {'form': form})