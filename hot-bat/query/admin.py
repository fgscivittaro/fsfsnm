from django.contrib import admin

from .models import Marcel, Regression, RegularData, BattedBallData

admin.site.register(Marcel)
admin.site.register(Regression)
admin.site.register(RegularData)
admin.site.register(BattedBallData)