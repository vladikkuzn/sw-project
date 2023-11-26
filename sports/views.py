# sports/views.py
from django.shortcuts import render, get_object_or_404
from .sparql_queries import get_all_athletes, get_player_details
from .models import Athlete, FootballEvent, Position, Team


def fetch_and_store_data(request):
    # Fetch and store athletes
    all_athletes = get_all_athletes()

    for entry in all_athletes:
        print(entry)
        athlete_name = entry['athleteName']['value']
        birth_date = entry['birthDate']['value']

        # Create Athlete object
        athlete, created = Athlete.objects.get_or_create(name=athlete_name, birth_date=birth_date)

        # Fetch and store athlete details
        entry = get_player_details(athlete_name)[0]
        # Create Position objects and associate with Athlete
        positions = entry.get('positions', {}).get('value', '').split(', ')
        for position_label in positions:
            position, created = Position.objects.get_or_create(label=position_label)
            athlete.positions.add(position)

        # Create Team objects and associate with Athlete
        teams = entry.get('teams', {}).get('value', '').split(', ')
        for team_label in teams:
            team, created = Team.objects.get_or_create(label=team_label)
            athlete.teams.add(team)

        # Create FootballEvent objects and associate with Athlete
        events = entry.get('events', {}).get('value', '').split(', ')
        for event_label in events:
            event, created = FootballEvent.objects.get_or_create(
                label=event_label,
                defaults={
                    'label': event_label,
                    'country': entry.get('eventCountry', {}).get('value', ''),
                    'champions': entry.get('championsLabel', {}).get('value', ''),
                    'athlete_names': entry.get('athleteNames', {}).get('value', ''),
                }
            )
            athlete.events.add(event)

    return render(request, 'sports/data_fetched.html')


def all_athletes(request):
    athletes = Athlete.objects.all()[:100]
    return render(request, 'sports/all_athletes.html', {'athletes': athletes})


def athlete_detail(request, athlete_id):
    athlete = get_object_or_404(Athlete, pk=athlete_id)
    return render(
        request,
        'sports/athlete_detail.html',
        {
            'athlete': athlete,
        },
    )


def position_detail(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    athletes = position.athlete_set.all()
    return render(request, 'sports/position_detail.html', {'position': position, 'athletes': athletes})


def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    athletes = team.athlete_set.all()
    return render(request, 'sports/team_detail.html', {'team': team, 'athletes': athletes})


def event_detail(request, event_id):
    event = get_object_or_404(FootballEvent, pk=event_id)
    athletes = event.athlete_set.all()
    return render(request, 'sports/event_detail.html', {'event': event, 'athletes': athletes})

