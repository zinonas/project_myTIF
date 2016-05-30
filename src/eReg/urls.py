__author__ = 'zinwnas'

from .views import IcdTenAutocomplete,OrphaAutocomplete
from django.conf.urls import patterns, include, url
from .models import Diagnosis



urlpatterns = patterns('',
    url(r'^icd10-autocomplete/$',IcdTenAutocomplete.as_view(),name='icd10-autocomplete'),
    url(r'^oprha-autocomplete/$',OrphaAutocomplete.as_view(),name='orpha-autocomplete'),
    )