from django.contrib import admin

# Register your models here.
from .models import *
from import_export.admin import ImportExportActionModelAdmin

@admin.register(land, city)
class ViewAdmin(ImportExportActionModelAdmin):
    pass