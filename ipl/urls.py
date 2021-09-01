from django.urls import path, reverse
from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from . import views

urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect(reverse('ipl_analyser'))),
    path("index", views.ipl_analyser, name="ipl_analyser"),
    path("year_summary/(?P<year>\d+)/", views.year_summary, name="year_summary"),
    path("chart_summary/(?P<year>\d+)/", views.charts, name="charts"),

]