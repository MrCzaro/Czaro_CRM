from django.contrib import admin

from .models import NortonScale, GlasgowComaScale, NewsScale, PainScale, BodyMassIndex
admin.site.register(BodyMassIndex)
admin.site.register(GlasgowComaScale)
admin.site.register(NewsScale)
admin.site.register(NortonScale)
admin.site.register(PainScale)