from django.contrib import admin

# Register your models here.
from .models import Demographic
from .models import Diagnosis
from .models import A_b_sickle_thal
from .models import Redcell_enzyme_dis
from .models import Redcell_membrane_dis
from .models import Cong_dyseryth_anaemia

class DemographicsAdmin(admin.ModelAdmin):
    class Meta:
        model = Demographic

class DiagnosisAdmin(admin.ModelAdmin):
    class Meta:
        model = Diagnosis

class a_b_sickle_Admin(admin.ModelAdmin):
    class Meta:
        model = A_b_sickle_thal

class redcell_enzAdmin(admin.ModelAdmin):
    class Meta:
        model = Redcell_enzyme_dis

class redcell_memb_Admin(admin.ModelAdmin):
    class Meta:
        model = Redcell_membrane_dis

class cong_dyserAdmin(admin.ModelAdmin):
    class Meta:
        model = Cong_dyseryth_anaemia
        
admin.site.register(Demographic, DemographicsAdmin)
admin.site.register(Diagnosis, DiagnosisAdmin)
admin.site.register(A_b_sickle_thal,a_b_sickle_Admin)
admin.site.register(Redcell_enzyme_dis,redcell_enzAdmin)
admin.site.register(Redcell_membrane_dis,redcell_memb_Admin)
admin.site.register(Cong_dyseryth_anaemia,cong_dyserAdmin)
