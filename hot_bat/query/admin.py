from django.contrib import admin

from .models import BattedBallData, RegularData

admin.site.register(BattedBallData)
admin.site.register(RegularData)