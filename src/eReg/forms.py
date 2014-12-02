from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset, MultiWidgetField
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup, FormActions
from functools import partial
from django.contrib.admin import widgets
from models import Demographic
from models import Diagnosis, A_b_sickle_thal, Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10
import autocomplete_light

autocomplete_light.register(icd_10, search_fields=['icd_10_desc'] )
autocomplete_light.autodiscover()

class DemographicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DemographicForm, self).__init__(*args, **kwargs)

        # self.helper.layout.form_class = 'form-horizontal'
        self.fields['date_of_birth']= forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.helper=FormHelper()
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        # self.helper.form_class = 'forms-horizontal'
        self.helper.layout = Layout(
            Field('national_health_care_pat_id'),
            Field('patient_hospital_file_number'),
            Field('patient_id'),
            Field('given_name'),
            Field('surname'),
            Field('date_of_birth'),
            Field('education'),
            Field('profession'),
            Field('family'),
            Field('address_street'),
            Field('address_no'),
            Field('address_city'),
            Field('address_post_code'),
            Field('address_state'),
            Field('address_country'),
            Field('telephone'),
            Field('email'),
            Field('legal_org_name'),
            Field('legal_org_phone'),
            Field('legal_org_email'),
            Field('contact_person_role'),
            Field('contact_person_name'),
            Field('contact_person_phone'),
            Field('contact_person_email'),
            Field('insurance_no'),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel', "Cancel")
            ),

        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Demographic
        exclude = []

class DiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)

        self.fields['icd_10_desc']= forms.ModelChoiceField(queryset=icd_10.objects.all(),
                                    widget=autocomplete_light.ChoiceWidget("icd_10Autocomplete"))
        self.fields['icd_10_desc'].label = "ICD-10 description"
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # 'patient',
            'age_of_diagnosis',
            'diagnosis_option',
            'record_of_genotype',
            'icd_10_desc',
            'icd_10_code',
            'comment',

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Diagnosis
        exclude = ['patient']
        # autocomplete_js_attribute={'name': 'icd_10_code'}



class A_b_sickle_thalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(A_b_sickle_thalForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # 'patient',
            'cbc',
            'hb',
            'mcv',
            'mch',
            'hba2',
            'hbf',
            'haemoglobin',
            'nrbc',
            'reticulocytes',
            'red_cell_morphology',
            'rare_anaemia',
            'cell_acetate_electr',
            'acid_agarose_citrate',
            'isoelect_foc',
            'hlpc_cap_elect',
            'quant_hba2',
            'quant_hbh',
            'quant_hbf',
            'quant_other_var',
            'conf_pres_hbs',
            'conf_pres_hbe',
            'conf_pres_un_haemo_isoprop_option',
            'conf_pres_un_haemo_isoprop',
            'conf_pres_un_haemo_heat_option',
            'conf_pres_un_haemo_heat',
            'conf_pres_un_haemo_ex_ir_transf_sat',
            'conf_pres_un_haemo_ex_ir_transf_serum',
            'conf_pres_un_haemo_ex_ir_transf_zinc',
            'mol_diag_a_thal_gap_pcr',
            'mol_diag_a_thal_gap_mpla',
            'mol_diag_a_thal_gap_seq',
            'mol_diag_b_thal_aso',
            'mol_diag_b_thal_reverse_dot_blot',
            'mol_diag_b_thal_oligonucl',
            'mol_diag_b_thal_arms',
            'mol_diag_b_thal_real_time_pcr',
            'mol_diag_b_thal_dgge',
            'mol_diag_b_thal_gap_pcr',
            'mol_diag_b_thal_mpla',
            'mol_diag_b_thal_seq_anal_a_gene',
            'mol_diag_b_thal_seq_anal_b_gene',
            'mol_diag_b_thal_seq_anal_g_gene',
            'snp_gene',
            'snp_code',
            'snp_allele1',
            'snp_allele1_type',
            'snp_allele2',
            'snp_allele2_type',

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = A_b_sickle_thal
        exclude = ['patient']

class Redcell_enzyme_disForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Redcell_enzyme_disForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # 'patient',
            'enzymes_of_glycol_option',
            'enzymes_of_glycol',
            'hk_option',
            'hk',
            'gpi',
            'pfk_option',
            'pfk',
            'g3ph_option',
            'g3ph',
            'pgk_option',
            'pgk',
            'pk_option',
            'pk_v',
            'tpi_option',
            'tpi',
            'ldh_option',
            'ldh',
            'adolase_option',
            'adolase',
            'enolase_option',
            'enolase',
            'bpgm_option',
            'bpgm',
            'mpgm_option',
            'mpgm',
            'pgm_option',
            'pgm',
            'enz_hexose_option',
            'enz_hexose',
            'g6pd_option',
            'g6pd',
            'no6pgd_option',
            'no6pgd',
            'gcs_option',
            'gcs',
            'gshs_option',
            'gshs',
            'gr_option',
            'gr',
            'gshpx_option',
            'gshpx',
            'gst_option',
            'gst',
            'enz_nuc_meta_option',
            'enz_nuc_meta',
            'ak_option',
            'ak',
            'pyr5nuc_option',
            'pyr5nuc',
            'pur_pyr_ratio_option',
            'pur_pur_ratio',
            'other_rbce_act_option',
            'other_rbce_act',
            'nadh_dia_option',
            'nadh_dia',
            'nadph_dia_option',
            'nadph_dia_act',
            'sod_option',
            'sod_act',
            'catalase_option',
            'catalase',
            'other_option',
            'glycol_interm_option',
            'glycol_interm',
            'g6p_option',
            'g6p',
            'f6p_option',
            'f6p',
            'fbp_option',
            'fbp',
            'dhap_option',
            'dhap',
            'gap_option',
            'gap',
            'no2_3dpg_option',
            'no2_3dpg',
            'no3pga_option',
            'no3pga',
            'no2pga_option',
            'no2pga',
            'pep_option',
            'pep',
            'amp_option',
            'amp',
            'ab_option',
            'ab',
            'atp_option',
            'atp',
            'gssg_gsh_option',
            'gssg_gsp',
            'pyr_option',
            'pyr',
            'lact_option',
            'lact',

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Redcell_enzyme_dis
        exclude = ['patient']

class Redcell_membrane_disForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Redcell_membrane_disForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # 'patient',
            'red_cell_morph_sm',
            'osm_fr_fresh_blood',
            'osm_fr_pre_incu_blood',
            'osm_fr_two_dif_nacl',
            'osm_fr_curve_str',
            'osm_fr_curve',
            'glt',
            'aglt',
            'cryohemolysis_tst',
            'pink_tst',
            'flow_commercial_tst',
            'sds_page_rbc_proteins',
            'ektacytometer',
            'lorrca',
            'rbc_retic_auto_prm',
            'molec_char_rna_dna_level',
            'method_best_sensi_speci',

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Redcell_membrane_dis
        exclude = ['patient']

class Cong_dyseryth_anaemiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cong_dyseryth_anaemiaForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # 'patient',
            'complt_blood_cnt',
            'abs_reticulo_cnt',
            'soluble_transf_recept',
            'bone_marrow_recept',
            'sds_page',
            'moleculare_analysis',

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Cong_dyseryth_anaemia
        exclude = ['patient']