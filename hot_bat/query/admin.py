from django.contrib import admin

from .models import BattedBallData, Players, RegularData

admin.site.register(BattedBallData)
admin.site.register(Players)
admin.site.register(RegularData)