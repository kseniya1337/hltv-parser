from django.shortcuts import render

from hltv_parser.models import Map, Team, Match, MatchVeto


def index(request):
    maps = Map.objects.all()
    teams = Team.objects.all()
    matches = Match.objects.all()
    return render(request, 'index.html', {
        'maps': maps,
        'teams': teams,
        'matches': matches,
    })


def statistic_table(request):
    competitive_maps = ['Anticient', 'Vertigo', 'Overpass', 'Inferno', 'Nuke', 'Dust II', 'Mirage']
    return render(request, 'statistic_table.html', {
        'maps': competitive_maps,
    })


def team_profile(request):
    return render(request, 'team_profile.html')
