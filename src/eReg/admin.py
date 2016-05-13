from django.contrib import admin

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

class DemographicsAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Demographic

class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Diagnosis

class a_b_sickle_Admin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = A_b_sickle_thal

class redcell_enzAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Redcell_enzyme_dis

class redcell_memb_Admin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Redcell_membrane_dis

class cong_dyserAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Cong_dyseryth_anaemia

class icd10Admin (admin.ModelAdmin):
    list_display = ('pub_date','author')
    class Meta:
        model = icd_10

class pregnancyAdmin (admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Pregnancy

class clinical_dataAdmin (admin.ModelAdmin):
    list_display = ('pub_date', 'author')
    class Meta:
        model = Clinical_data

admin.site.register(Demographic, DemographicsAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(A_b_sickle_thal,a_b_sickle_Admin)
admin.site.register(Redcell_enzyme_dis,redcell_enzAdmin)
admin.site.register(Redcell_membrane_dis,redcell_memb_Admin)
admin.site.register(Cong_dyseryth_anaemia,cong_dyserAdmin)
admin.site.register(icd_10, icd10Admin)
admin.site.register(Pregnancy,pregnancyAdmin)
admin.site.register(Clinical_data,clinical_dataAdmin)