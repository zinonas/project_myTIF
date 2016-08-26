from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views import generic

from dal import autocomplete
from django.contrib import admin

from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.views import password_reset
# import every app/autocomplete_light_registry.py
#autocomplete_light.autodiscover()


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_mytif.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('eReg.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'eReg.views.home', name='home'),
    url(r'^test/', 'eReg.views.test', name='test'),
    url(r'^module_selection/', 'eReg.views.modules', name='modules'),
    url(r'^input/', 'eReg.views.input', name='input'),
    url(r'^search/', 'eReg.views.search', name='search'),
    url(r'^results/', 'eReg.views.results', name='results'),
    url(r'^results_anonymised/', 'eReg.views.results_anonymised', name='results_anonymised'),
    url(r'^about/', 'eReg.views.about', name='about'),
    url(r'^patient/', 'eReg.views.patient', name='patient'),
    #url(r'^search_patient_card/', 'eReg.views.search_patient_card', name='search_patient_card'),
    #url(r'^results_patient_card/', 'eReg.views.results_patient_card', name='results_patient_card'),
    url(r'^statistics/','eReg.views.statistics', name='statistics'),
    url(r'^externalcenters/','eReg.views.external_centers', name='extcenters'),
    # url(r'^input/', 'eReg.views.icd_10_view', name='icd_10_view'),
    # url(r'^input/', 'eReg.views.icd_10_view', name='icd_10_view'),
    url(r'^accounts/login/', 'eReg.views.login', name='login_view'),
    url(r'^accounts/logout/', 'eReg.views.logout_view', name='logout_view'),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    url(r'^login/', 'eReg.views.login', name='login'),
    #url(r'^logout/', 'eReg.views.logout_view', name='logout_view'),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),



    #url(r'^cookies/', include('cookie_consent.urls')),


    #url(r'^accounts/password_change/$',  # hijack password_change's url
    #    'django.contrib.auth.views.password_change',
    #    {'password_change_form': AdminPasswordChangeForm},
    #    name="password_change"),


)

#if DEBUG is true
#if settings.DEBUG:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
