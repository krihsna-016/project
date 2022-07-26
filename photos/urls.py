from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('photo/<str:pk>/', views.ImageDownloadView, name='download'),
    path('photo/<str:id>', views.s3_delete, name="delete-image"),
    path('add/', views.addPhoto, name='add'),
]
