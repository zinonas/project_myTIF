from django.contrib import admin
from django.contrib.auth.models import User, Group
from simple_history import register

# Register your models here.
from .models import Demographic
from .models import Diagnosis
from .models import A_b_sickle_thal
from .models import Redcell_enzyme_dis
from .models import Redcell_membrane_dis
from .models import Cong_dyseryth_anaemia
from .models import icd_10
from .models import Pregnancy
from .models import Clinical_data
from .models import Clinical_data_two
from .models import Patient_reported_outcome
from .models import DiagnosisOption
from .models import Institution

from simple_history.admin import SimpleHistoryAdmin

class DemographicsAdmin(SimpleHistoryAdmin):
    list_display = ('patient_id','pub_date', 'author')
    class Meta:
        model = Demographic

class DiagnosisAdmin(SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Diagnosis

class a_b_sickle_Admin(SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = A_b_sickle_thal

class redcell_enzAdmin(SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Redcell_enzyme_dis

class redcell_memb_Admin(SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Redcell_membrane_dis

class cong_dyserAdmin(SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Cong_dyseryth_anaemia

class icd10Admin (SimpleHistoryAdmin):
    list_display = ('pub_date','author')
    class Meta:
        model = icd_10

class pregnancyAdmin (SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Pregnancy

class clinical_dataAdmin (SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Clinical_data

class clinical_data_twoAdmin (SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Clinical_data_two

class patient_rep_outAdmin (SimpleHistoryAdmin):
    list_display = ('patient','pub_date', 'author')
    class Meta:
        model = Patient_reported_outcome

class diag_optAdmin (SimpleHistoryAdmin):
    list_display = ('id','diag_option')
    class Meta:
        model = DiagnosisOption

class institutionAdmin (SimpleHistoryAdmin):
    list_display = ('user', 'department')
    class Meta:
        model = Institution


register(User, inherit=True)
register(Group, inherit=True)

#admin.site.register(User, SimpleHistoryAdmin)
admin.site.register(Institution, institutionAdmin)
admin.site.register(Demographic, DemographicsAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(DiagnosisOption,diag_optAdmin)
admin.site.register(A_b_sickle_thal,a_b_sickle_Admin)
admin.site.register(Redcell_enzyme_dis,redcell_enzAdmin)
admin.site.register(Redcell_membrane_dis,redcell_memb_Admin)
admin.site.register(Cong_dyseryth_anaemia,cong_dyserAdmin)
admin.site.register(icd_10, icd10Admin)
admin.site.register(Pregnancy,pregnancyAdmin)
admin.site.register(Clinical_data,clinical_dataAdmin)
admin.site.register(Clinical_data_two,clinical_data_twoAdmin)
admin.site.register(Patient_reported_outcome,patient_rep_outAdmin)




# admin.site.register(Demographic, SimpleHistoryAdmin)
# admin.site.register(Diagnosis, SimpleHistoryAdmin)
# admin.site.register(DiagnosisOption,SimpleHistoryAdmin)
# admin.site.register(A_b_sickle_thal,SimpleHistoryAdmin)
# admin.site.register(Redcell_enzyme_dis,SimpleHistoryAdmin)
# admin.site.register(Redcell_membrane_dis,SimpleHistoryAdmin)
# admin.site.register(Cong_dyseryth_anaemia,SimpleHistoryAdmin)
# admin.site.register(icd_10, SimpleHistoryAdmin)
# admin.site.register(Pregnancy,SimpleHistoryAdmin)
# admin.site.register(Clinical_data,SimpleHistoryAdmin)
# admin.site.register(Patient_reported_outcome,SimpleHistoryAdmin)

