# sports/urls.py
from django.urls import path
from .views import fetch_and_store_data, all_athletes, athlete_detail, position_detail, team_detail, event_detail

urlpatterns = [
    path('fetch_and_store_data/', fetch_and_store_data, name='fetch_and_store_data'),
    path('all_athletes/', all_athletes, name='all_athletes'),
    path('athlete_detail/<int:athlete_id>/', athlete_detail, name='athlete_detail'),
    path('position_detail/<int:position_id>/', position_detail, name='position_detail'),
    path('team_detail/<int:team_id>/', team_detail, name='team_detail'),
    path('event_detail/<int:event_id>/', event_detail, name='event_detail'),
]
