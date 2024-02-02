from django.contrib import admin

from .models import NortonScale, GlasgowComaScale, NewsScale
admin.site.register(NortonScale)
admin.site.register(GlasgowComaScale)
admin.site.register(NewsScale)