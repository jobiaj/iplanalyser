from django.shortcuts import render

from django.shortcuts import render

from ipl.models import Match, Deliveries
from django.db.models import Count, Avg, Max, Min, Sum


def ipl_analyser(request):
    years = Match.objects.values('season').distinct()
    context = {
        "years": years,
        "selected_year": 0
    }

    return render(request, "base_site.html", context)


def year_summary(request, year):
    years = Match.objects.exclude(season=year).values('season').distinct()
    season_matches = Match.objects.filter(season=year)
    total_count = season_matches.count()
    winner_group = season_matches.values('winner').annotate(total=Count('winner')).order_by('-total')
    toss_winner_max = season_matches.values('toss_winner').annotate(total=Count('toss_winner')).order_by('-total').first()
    player_of_match_max = season_matches.values('player_of_match').annotate(total=Count('player_of_match')).order_by('-total').first()
    maximum_winner = season_matches.values('winner').annotate(total=Count('winner')).order_by('-total').first()
    winning_location_max = season_matches.values('winner', 'venue').annotate(total=Count('winner')).order_by('-total').first()
    toss_descision = season_matches.filter(toss_decision='bat').values('toss_decision').annotate(total=Count('toss_decision')).order_by('-total').first()
    average_to_decide_to_bat = (toss_descision['total'] / total_count) * 100
    maximum_no_venue = season_matches.aggregate(Max('venue'))
    maximum_win_by_runs = season_matches.values('winner', 'win_by_runs').aggregate(Max('win_by_runs'))
    team_which_won_with_maximum_runs = season_matches.filter(win_by_runs=maximum_win_by_runs['win_by_runs__max']).values('winner', 'win_by_runs').last()

    context = {
        "years": years,
        "winners": winner_group[0:4],
        "toss_winner_max": toss_winner_max,
        "player_of_match": player_of_match_max,
        "maximum_winner": maximum_winner,
        "winning_location_max": winning_location_max,
        "selected_year": year,
        "average_to_decide_to_bat": average_to_decide_to_bat,
        "maximum_no_venue": maximum_no_venue,
        "team_which_won_with_maximum_runs": team_which_won_with_maximum_runs
    }

    return render(request, "analysis.html", context)

def get_required_data(season_matches):
    
    winner_group = season_matches.values('winner').annotate(total=Count('winner')).order_by('-total')
    toss_winner_group = season_matches.values('toss_winner').annotate(total=Count('toss_winner')).order_by('-total')
    player_of_match = season_matches.values('player_of_match').annotate(total=Count('player_of_match')).order_by('-total')
    winning_location = season_matches.values('winner', 'venue').annotate(total=Count('winner')).order_by('-total')
    toss_descision = season_matches.values('toss_decision').annotate(total=Count('toss_decision')).order_by('-total')
    data = {"winner": winner_group, "toss_winner": toss_winner_group, 
            "player_of_match": player_of_match,
            "venue": winning_location,
            "toss_decision": toss_descision}
    return data


def charts(request, year):
    years = Match.objects.values('season').distinct()
    season_matches = Match.objects.filter(season=year)

    data = get_required_data(season_matches)
    response = {
        "years": years,
        "selected_year": year
    }
    draw_data_list = []
    for key in data.keys():
        labels = []
        draw_data = []
        for item in data[key]:
            labels.append(item[key])
            draw_data.append(item['total'])
        response[key] = {"data": draw_data, "labels": labels}
    maximum_win_by_runs = season_matches.order_by('-win_by_runs').values('winner', 'win_by_runs')
    run_by_max_data = []
    run_by_max_label = []
    for item in maximum_win_by_runs:
        run_by_max_label.append(item['winner'])
        run_by_max_data.append(item['win_by_runs'])
    response["win_by_runs"] = {"data": run_by_max_data, "labels": run_by_max_label}
    return render(request, "charts.html", response)