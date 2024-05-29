from django.shortcuts import render, redirect

# Create your views here.
 
from .forms import UploadModelForm
from .models import Photo

def uploadFile(request):
    photos = Photo.objects.all()
    form = UploadModelForm()
    if request.method == 'POST':
        form = UploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            redirect('/photos')
    context = {'photos': photos,
               'form':form
               }
    
    return render(request, 'index.html', locals())