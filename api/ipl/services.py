from ipl.models import Match, Deliveries
from django.db.models import Count, Avg, Max, Min, Sum



class Service(object):
    pass


class MatchService(Service):
    
    @classmethod
    def _get_all_matches(cls):
        return Match.objects.all()

    @classmethod
    def _get_all_seasons(self):
        return Match.objects.values('season').distinct()

class SeasonService(Service):
    def __init__(self, season):
        super(SeasonService, self).__init__()
        self.season = season

    def _get_all_matches(self):
        return MatchService._get_all_matches().filter(season=self.season)

    def _count_of_matches(self):
        return self._get_all_matches().count()

    def get_sorted_list_based_field(self, field='', order_by='Ascending', limit=None):
        qs = self._get_all_matches().values(field).annotate(total=Count(field))
        if order_by != 'Ascending':
            qs = qs.order_by('-total')
        else:
            qs = qs.order_by('-total')
        if limit:
            return qs[0:limit]
        return qs
