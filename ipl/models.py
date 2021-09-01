from django.db import models


class Match(models.Model):
    season = models.PositiveIntegerField(editable=False)
    city = models.CharField(max_length=100)
    date = models.DateField()
    season = models.CharField(max_length=100)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    dl_applied = models.BooleanField(default=False, editable=True)
    winner = models.CharField(max_length=100)
    win_by_runs = models.PositiveIntegerField(editable=False)
    win_by_wickets = models.PositiveIntegerField(editable=False)
    player_of_match = models.CharField(max_length=100)
    venue = models.CharField(max_length=1024)
    umpire1 = models.CharField(max_length=100)
    umpire2 = models.CharField(max_length=100)
    umpire3 = models.CharField(max_length=100)

    class Meta(object):
        app_label = 'ipl'

    def __str__(self):
        return self.season


class Deliveries(models.Model):
    match = models.ForeignKey(
        'Match', editable=False, on_delete=models.CASCADE)
    inning = models.PositiveIntegerField(editable=False)
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)
    over = models.PositiveIntegerField(editable=False)
    ball = models.PositiveIntegerField(editable=False)
    batsman = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
    bowler = models.CharField(default='', max_length=100)
    is_super_over = models.BooleanField(default=False, editable=True)
    wide_runs = models.PositiveIntegerField(editable=False)
    bye_runs = models.PositiveIntegerField(editable=False)
    legbye_runs = models.PositiveIntegerField(editable=False)
    noball_runs = models.PositiveIntegerField(editable=False)
    penalty_runs = models.PositiveIntegerField(editable=False)
    batsman_runs = models.PositiveIntegerField(editable=False)
    extra_runs = models.PositiveIntegerField(editable=False)
    total_runs = models.PositiveIntegerField(editable=False)
    player_dismissed = models.CharField(max_length=100)
    dismissal_kind = models.CharField(max_length=100)
    fielder = models.CharField(max_length=100)


    class Meta(object):
        app_label = 'ipl'
        # unique_together = ('match', 'inning', 'over', 'ball')

    def __str__(self):
        return self.batting_team + 'vs' + self.bowling_team
        