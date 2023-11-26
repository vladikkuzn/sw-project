from django.contrib import admin

from sports.models import Athlete, FootballEvent, Position, Team


class AthleteAdmin(admin.ModelAdmin):
    pass


class FootballEventAdmin(admin.ModelAdmin):
    pass


class PositionAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Athlete, AthleteAdmin)
admin.site.register(FootballEvent, FootballEventAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Team, TeamAdmin)
