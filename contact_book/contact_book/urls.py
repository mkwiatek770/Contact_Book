"""contact_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Home.as_view(), name="home"),
    path('modify/<int:id>/', views.modify_person, name='modify'),
    path('show/<int:id>/', views.PersonInfo.as_view(), name='show'),
    path('delete/<int:id>/', views.delete_person, name='delete_person'),
    path('groups/', views.Groups.as_view(), name='groups'),
    path('group/<int:id>/', views.GroupInfo.as_view(), name='group_info'),
    path('group_delete/<int:id>/', views.delete_group, name="delete_group"),
    path('delete-phone/<int:person_id>/<int:number_id>',
         views.delete_phone, name='delete_phone'),
    path('delete-email/<int:person_id>/<int:email_id>',
         views.delete_email, name='delete_email'),
    path('delete-person-group/<int:person_id>/<int:group_id>/',
         views.delete_person_group, name='delete_person_group'),
    path('add-contact/', views.AddContact.as_view(), name="add_contact"),
    path('add-group/', views.AddGroup.as_view(), name="add_group"),

]
