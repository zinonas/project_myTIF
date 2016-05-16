from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
import autocomplete_light
from django.contrib import admin
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_mytif.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'eReg.views.home', name='home'),
    url(r'^test/', 'eReg.views.test', name='test'),
    url(r'^module_selection/', 'eReg.views.modules', name='modules'),
    url(r'^input/', 'eReg.views.input', name='input'),
    url(r'^search/', 'eReg.views.search', name='search'),
    url(r'^results/', 'eReg.views.results', name='results'),
    #url(r'^search_patient_card/', 'eReg.views.search_patient_card', name='search_patient_card'),
    #url(r'^results_patient_card/', 'eReg.views.results_patient_card', name='results_patient_card'),
    url(r'statistics/','eReg.views.statistics', name='statistics'),
    url(r'externalcenters/','eReg.views.external_centers', name='extcenters'),
    # url(r'^input/', 'eReg.views.icd_10_view', name='icd_10_view'),
    # url(r'^input/', 'eReg.views.icd_10_view', name='icd_10_view'),
    url(r'^login/', 'eReg.views.login', name='login'),
    url(r'^logout/', 'eReg.views.logout_view', name='logout_view'),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

#if DEBUG is true 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
