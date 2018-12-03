from django.contrib import admin
from .models import Person, Group, Email, Phone


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    pass
