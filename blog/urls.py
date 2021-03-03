from django.urls import path
from .import views

urlpatterns = [
    path('blog/', views.blogpost, name='blog'),
    path('blog/<int:pk>/',views.blogdetails,name='blogdetails')
    

]