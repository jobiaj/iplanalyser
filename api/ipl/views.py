from django.shortcuts import render
from django.db.models import Count, Avg, Max, Min, Sum

from ipl.services import SeasonService, MatchService


def ipl_analyser(request):

    years = MatchService._get_all_seasons()
    context = {
        "years": years,
        "selected_year": 0
    }

    return render(request, "base_site.html", context)


def year_summary(request, year):
    season_service = SeasonService(year)

    years = MatchService._get_all_matches().exclude(season=year).values('season').distinct()
    season_matches = season_service._get_all_matches()
    total_count = season_service._count_of_matches()
    winner_group = season_service.get_sorted_list_based_field(field='winner', order_by='Decending', limit=4)

    toss_winner_max =  season_service.get_sorted_list_based_field(field='toss_winner', order_by='Decending').first()
    player_of_match_max = season_service.get_sorted_list_based_field(field='player_of_match', order_by='Decending').first()
    maximum_winner = winner_group.first()
    winning_location_max = season_matches.values('winner', 'venue').annotate(total=Count('winner')).order_by('-total').first()
    toss_descision = season_matches.filter(toss_decision='bat').values('toss_decision').annotate(total=Count('toss_decision')).order_by('-total').first()
    average_to_decide_to_bat = (toss_descision['total'] / total_count) * 100
    maximum_no_venue = season_matches.aggregate(Max('venue'))
    maximum_win_by_runs = season_matches.values('winner', 'win_by_runs').aggregate(Max('win_by_runs'))
    team_which_won_with_maximum_runs = season_matches.filter(win_by_runs=maximum_win_by_runs['win_by_runs__max']).values('winner', 'win_by_runs').last()

    context = {
        "years": years,
        "winners": winner_group,
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

def charts(request, year):
    season_service = SeasonService(year)

    years = MatchService._get_all_matches().exclude(season=year).values('season').distinct()

    season_matches = season_service._get_all_matches()
    winner_group = season_service.get_sorted_list_based_field(field='winner', order_by='Decending')
    toss_winner_group = season_service.get_sorted_list_based_field(field='toss_winner', order_by='Decending')
    player_of_match = season_service.get_sorted_list_based_field(field='player_of_match', order_by='Decending')
    toss_descision = season_service.get_sorted_list_based_field(field='toss_decision', order_by='Decending')
    winning_location = season_matches.values('winner', 'venue').annotate(total=Count('winner')).order_by('-total')
 
    data = {"winner": winner_group, 
            "toss_winner": toss_winner_group, 
            "player_of_match": player_of_match,
            "venue": winning_location,
            "toss_decision": toss_descision}

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