# app_name/admin.py

from django.contrib import admin
from .models import *

admin.site.register(Patient)

admin.site.register(Hospital)
