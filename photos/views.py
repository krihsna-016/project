from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# Create your views here.


def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)


@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})



import os
import magic

from django.views.generic import View
from django.http import HttpResponse

from wsgiref.util import FileWrapper
# from django.core.servers.basehttp import FileWrapper
import mimetypes

# class ImageDownloadView(View):
@login_required(login_url='login')
def ImageDownloadView(request, pk):
    img = Photo.objects.get(id=pk)
    wrapper      = FileWrapper(open(img.file))  # img.file returns full path to the image
    content_type = mimetypes.guess_type(filename)[0]  # Use mimetypes to get file type
    response     = HttpResponse(wrapper,content_type=content_type)  
    response['Content-Length']      = os.path.getsize(img.file)    
    response['Content-Disposition'] = "attachment; filename=%s" %  img.name
    # return response
    return render(response, 'photos/photo.html', {'download': response})

# instance.image, content_type="image/jpeg"
import boto
from boto.s3.key import Key
from django.conf import settings


def s3_delete(id):
    s3conn = boto.connect_s3(settings.AWS_ACCESS_KEY,
            settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3conn.get_bucket(settings.S3_BUCKET)

    k = Key(bucket)
    k.key = str(id)
    k.delete()




@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
