from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def statistic_table(request):
    competitive_maps = ['Anticient', 'Vertigo', 'Overpass', 'Inferno', 'Nuke', 'Dust II', 'Mirage']
    return render(request, 'statistic_table.html', {
        'maps': competitive_maps,
    })
