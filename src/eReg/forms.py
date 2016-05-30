from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset, MultiWidgetField,MultiField
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup, FormActions
from functools import partial
from django.contrib.admin import widgets
from models import Demographic
from models import Diagnosis, A_b_sickle_thal, Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, Pregnancy, Clinical_data, Clinical_data_two, Ext_centers,Patient_reported_outcome,DiagnosisOption
from sympy import pretty_print as pp, latex
from dal import autocomplete



#import autocomplete_light
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

#autocomplete_light.register(icd_10, search_fields=['icd_10_desc'] )
#autocomplete_light.autodiscover()

class DemographicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DemographicForm, self).__init__(*args, **kwargs)

        # self.helper.layout.form_class = 'form-horizontal'
        self.fields['date_of_birth']= forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['creation_of_consent_form']= forms.DateField(label='Creation date',
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        #self.fields['patient_consent_for_data_storage']=forms.CharField(required=True)

        self.helper=FormHelper()
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        # self.helper.form_class = 'forms-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Patient consent</b>',
                Div(
                    Div('patient_consent_for_data_storage', css_class='col-md-6'),
                    Div('patient_consent_for_data_reusage', css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('creation_of_consent_form', css_class='col-md-6'),
                    Div('data_entered_by', css_class='col-md-6'),
                    css_class='row',
                ),
                Div(
                    Div('data_entered_by_name', css_class='col-md-6'),
                    Div('data_entered_by_relationship', css_class='col-md-6'),
                    css_class='row',
                ),
            ),
            Fieldset(
                '<b>Identification</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('national_health_care_pat_id',css_class='col-md-6'),
                    Div('patient_hospital_file_number',css_class="col-md-6"),
                    css_class='row',
                    ),

                Div(
                    Div('guid', css_class='col-md-6'),
                    css_class='row',
                ),
                ),
            Fieldset(
                '<b>Personal information</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('patient_id',css_class='col-md-6'),
                    Div('date_of_birth',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('surname',css_class='col-md-6'),
                    Div('given_name',css_class="col-md-6"),
                    Div('middle_name',css_class="col-md-6"),
                    Div('maiden_name',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('gender',css_class='col-md-6'),
                    Div('race', css_class='col-md-6'),
                    Div('country_of_birth', css_class='col-md-6'),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Contact information</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('telephone',css_class='col-md-4'),
                    Div('email',css_class="col-md-4"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    #Div('address_no',css_class='col-md-4'),
                    Div('address_street',css_class="col-md-6"),
                    Div('address_post_code',css_class='col-md-4'),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('address_city',css_class="col-md-4"),
                    Div('address_state',css_class='col-md-4'),
                    Div('address_country',css_class="col-md-4"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Preferred Health Professional</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('legal_org_name',css_class='col-md-6'),
                    Div('legal_org_clinic',css_class='col-md-6'),
                    Div('legal_org_phone',css_class="col-md-6"),
                    Div('legal_org_email',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Contact person (Next of kin)</b>',
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('contact_person_role',css_class='col-md-4'),
                    Div('contact_person_name',css_class="col-md-4"),
                    Div('contact_person_surname', css_class="col-md-4"),
                    css_class='row',
                    ),
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('contact_person_phone',css_class='col-md-4'),
                    Div('contact_person_email',css_class="col-md-4"),
                    css_class='row',
                    ),
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('cp_address_no',css_class='col-md-4'),
                    Div('cp_address_street',css_class="col-md-4"),
                    Div('cp_address_city',css_class="col-md-4"),
                    Div('cp_address_post_code',css_class="col-md-4"),
                    Div('cp_address_state',css_class="col-md-4"),
                    Div('cp_address_country',css_class="col-md-4"),
                    css_class='row',
                    ),
                 ),
            Fieldset(
                '<b>Insurance Information</b>',
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('insurance_no_public',css_class='col-md-6'),
                    Div('insurance_no_private',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Social Data</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('education',css_class='col-md-6'),
                    Div('profession',css_class="col-md-6"),
                    Div('father_education',css_class="col-md-6"),
                    Div('mother_education',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('family_situation',css_class='col-md-6'),
                    Div('no_of_children',css_class="col-md-6"),
                    #Div('paternity',css_class="col-md-6"),
                    #Div('maternity',css_class="col-md-6"),
                    #Div('no_of_children',css_class="col-md-6"),
                    css_class='row',
                    ),

                ),


            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel', "Cancel")
            ),

        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Demographic
        exclude = ['age', 'author']
        list_display = ('patient_id', 'pub_date', 'author')

class ClinicalDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ClinicalDataForm, self).__init__(*args, **kwargs)

        self.fields['clinical_data_date_of_examination']= forms.DateField(label=('Date of examination'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_cholelithiasis_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_cholecystectomy_date']= forms.DateField(label=('Date of operation'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_splenectomy_date']= forms.DateField(label=('Date of operation'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_iron_overload_heart_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_heart_failure_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_cardiac_arrythmia_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_glucose_intolerance_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_diabetes_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_hypothyroidism_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_hypoparathyroidism_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_hypogonadism_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_iron_overload_liver_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_others_date']= forms.DateField(label=('Date of diagnosis'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_one_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_two_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_three_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['assessment_of_iron_load_liver_mri_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_fibroscan_date']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        #YEAR ONLY
        self.fields['current_treatment_chelation_start']= forms.DateField(label=('Start of chelation therapy'),required=False,
        widget=DateTimePicker(options={"format": "YYYY",
                                       "pickTime": False,
                                       "viewMode": 'years',
                                       "startDate": "1900"}))

        self.fields['current_treatment_bone_marrow_date']= forms.DateField(label=('Date performed'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_method_mri']= forms.DateField(label=('Date measured'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['serological_data_date']= forms.DateField(label=('Date positive'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['date_of_transition_from_irregular_to_regular_tranfusions']= forms.DateField(label=('Date of transition from irregular to regular tranfusions'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['mortality_date_of_death']= forms.DateField(label=('Date of death'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        current_treatment_chelation_drug_option= (
        ('Desferrioxamine','Desferrioxamine'),
        ('Deferiprone','Deferiprone'),
        ('Deferasirox','Deferasirox'),
        ('Other','Other'),
        )
        self.fields['current_treatment_chelation_drug']=forms.MultipleChoiceField(label='Current Chelator regime',choices=current_treatment_chelation_drug_option, widget=forms.CheckboxSelectMultiple(),required=False)
        self.helper=FormHelper(form=self)
        self.helper.field_class = 'col-md-9'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            # Fieldset (
            #     # 'patient',
            #     '<b>Diagnosis information</b>',
            #     'age_of_diagnosis',
            #     'diagnosis_option',
            #     'record_of_genotype',
            #     'icd_10_desc',
            #     'icd_10_code',
            #     'comment',
            #     ),
            # Fieldset(
            #     '<b>Diagnosis circumstances</b>',
            #     'diagnosis_circumstances',
            #     'diagnosis_circumstances_date',
            #     #'diagnosis_circumstances_caring_year',
            #     ),
            Fieldset(
                '<b>Clinical Findings of Thalassaemia and Severe Anaemias</b>',
                Div(
                     Div('clinical_data_date_of_examination',css_class='col-md-6'),
                     css_class='row',
                     ),
                Div(
                     Div('clinical_data_weight',css_class='col-md-4'),
                     Div(HTML('kg'), css_class="col-md-1"),
                     Div('clinical_data_height',css_class='col-md-4'),
                     Div(HTML('cm'), css_class="col-md-1"),
                     css_class='row',
                     ),
                Div(
                     Div('clinical_data_spleen_size',css_class='col-md-4'),
                     Div(HTML('cm'), css_class="col-md-1"),
                     Div('clinical_data_liver_size',css_class='col-md-4'),
                     Div(HTML('cm'), css_class="col-md-1"),
                     css_class='row',
                     ),
                ),
            Fieldset(
                '<b>Family Tree</b>',
                ),
            Fieldset(
                '<b>Transfusion history</b>',
                Div(
                    #HTML(u'<div class="col-md-9"><h4><b>Transfusion history</b></h4></div><br/><br/>'),
                    Div('blood_group',css_class="col-md-6"),
                    Div('age_of_first_transfusion', css_class="col-md-6"),
                    #HTML("years<br/>"),

                    Div('transfusion_depentent_anaemia', css_class="col-md-6"),
                    Div('date_of_transition_from_irregular_to_regular_tranfusions', css_class="col-md-8"),

                    css_class='row',
                    ),
            ),
            Fieldset(
                '<b>Assessment of iron load serrum</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_one',css_class='col-md-5'),
                    Div(HTML("mg/L"), css_class="col-md-1"),
                    Div('assessment_of_iron_load_serrum_one_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_two',css_class='col-md-5'),
                    Div(HTML("mg/L"), css_class="col-md-1"),
                    Div('assessment_of_iron_load_serrum_two_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_three',css_class='col-md-5'),
                    Div(HTML("mg/L"), css_class="col-md-1"),
                    Div('assessment_of_iron_load_serrum_three_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_liver_mri',css_class='col-md-5'),
                    Div(HTML("mg/g dry weight"), css_class="col-md-2"),
                    Div('assessment_of_iron_load_liver_mri_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_fibroscan',css_class='col-md-6'),
                    Div('assessment_of_iron_load_fibroscan_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_intra_hepatic_iron',css_class='col-md-6'),
                    Div('assessment_of_iron_load_method_mri',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_method_cardiac_iron',css_class='col-md-6'),
                    Div('assessment_of_iron_load_ti_bassal_hb_rate',css_class="col-md-5"),
                    css_class='row',
                    ),

                ),
            Fieldset(
                '<b>Serological data (Viral)</b>',
                Div(
                    Div('serological_data_date',css_class='col-md-6'),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('serolocigal_data_HCV',css_class='col-md-6'),
                    Div('serolocigal_data_HCV_PCR',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('serolocigal_data_HBV',css_class='col-md-6'),
                    Div('serolocigal_data_HIV',css_class="col-md-5"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Current treatment</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),

                    Div('current_treatment_transfusion_regime',css_class='col-md-6'),
                    Div('current_treatment_chelation',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_chelation_start',css_class='col-md-6'),

                    css_class='row',
                    ),
                Field ('current_treatment_chelation_drug'),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_bone_marrow',css_class='col-md-6'),
                    Div('current_treatment_bone_marrow_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(

                    Div('current_treatment_bone_marrow_success',css_class='col-md-6'),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Replacement therapy</b>',
                Div(
                    #HTML(u'<p><b>Replacement therapy</b></p>'),
                    Div('current_treatment_replacement_ther',css_class="col-md-6"),
                    Div('current_treatment_sex_horm',css_class='col-md-6'),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_insulin',css_class="col-md-6"),
                    Div('current_treatment_thyroid',css_class='col-md-6'),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Hepatitis treatment</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_hepatitis_treatment_c',css_class="col-md-6"),
                    Div('current_treatment_hepatitis_treatment_b',css_class='col-md-6'),

                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Complications/Outcomes</b>',

                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_cholelithiasis',css_class='col-md-6'),
                    Div('clinical_data_cholelithiasis_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_cholecystectomy',css_class='col-md-6'),
                    Div('clinical_data_cholecystectomy_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),,
                    Div('clinical_data_splenectomy',css_class='col-md-6'),
                    Div('clinical_data_splenectomy_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_iron_overload_heart',css_class='col-md-6'),
                    Div('clinical_data_iron_overload_heart_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_heart_failure',css_class='col-md-6'),
                    Div('clinical_data_heart_failure_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_cardiac_arrythmia',css_class='col-md-6'),
                    Div('clinical_data_cardiac_arrythmia_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_glucose_intolerance',css_class='col-md-6'),
                    Div('clinical_data_glucose_intolerance_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_diabetes',css_class='col-md-6'),
                    Div('clinical_data_diabetes_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_hypothyroidism',css_class='col-md-6'),
                    Div('clinical_data_hypothyroidism_date',css_class="col-md-5"),
                    css_class='row',
                    ),

                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_hypoparathyroidism',css_class='col-md-6'),
                    Div('clinical_data_hypoparathyroidism_date',css_class="col-md-5"),
                    css_class='row',
                    ),

                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_hypogonadism',css_class='col-md-6'),
                    Div('clinical_data_hypogonadism_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_iron_overload_liver',css_class='col-md-6'),
                    Div('clinical_data_iron_overload_liver_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('clinical_data_others',css_class='col-md-6'),
                    Div('clinical_data_others_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                ),

            Fieldset(
                '<b>Supportive therapy</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_by_hydroxyurea',css_class="col-md-6"),
                    Div('current_treatment_by_hydroxyurea_with_epo',css_class='col-md-6'),
                    css_class='row',
                    ),
                Div(
                    Div('current_treatment_other',css_class='col-md-6'),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Outcomes</b>',

                 Div(
                     HTML(u'<div class="col-md-9"><h4><b>Mortality</b></h4></div><br/><br/>'),
                    Div('mortality_date_of_death',css_class='col-md-6'),
                    Div('mortality_cause_of_death',css_class="col-md-6"),
                    css_class='row',
                    ),

             ),



            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True


    class Meta:
        model = Clinical_data
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')

class ClinicalDataTwo(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(ClinicalDataTwo, self).__init__(*args, **kwargs)

        self.fields['prophylactic_measures_antibiotic_prophylaxis_penicillin_date']= forms.DateField(label=('Date started'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['prophylactic_measures_antibiotic_prophylaxis_other_date']= forms.DateField(label=('Date started'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['prophylactic_measures_vaccinations_pneumococcal_OCV_date']= forms.DateField(label=('Date given'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_liver_profile_date']= forms.DateField(label=('Date abnormal'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_renal_profile_blood_urea_date']= forms.DateField(label=('Date abnormal'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_renal_profile_creatine_date']= forms.DateField(label=('Date abnormal'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_renal_profile_proteiuria_date']= forms.DateField(label=('Date detected'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_pulmonary_function_date']= forms.DateField(label=('Date abnormal'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_hip_radiology_date']= forms.DateField(label=('Date abnormal'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_dactylitis_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_stroke_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_splenic_sequestration_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_aplastic_crisis_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_acute_chest_syndrome_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_multi_organ_failure_syndrome_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_priapism_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_heart_failure_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_pulmonary_hypertension_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_allo_immunation_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_iron_overload_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_serious_infection_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['complications_azoospermia_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.fields['monitoring_tests_annual_parvovirus_serology_date']= forms.DateField(label=('Date found positive'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.helper=FormHelper(form=self)
        self.helper.field_class = 'col-md-9'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(

            Fieldset(
                '<b>Clinical findings of Sickle Cell Disease</b>',),
            Fieldset(
                '<b>A. Prophylactic measures</b>',),
            Fieldset(
                'Antibiotic prophylaxis',
                Div(
                     Div('prophylactic_measures_antibiotic_prophylaxis_penicillin',css_class='col-md-6'),
                     Div('prophylactic_measures_antibiotic_prophylaxis_penicillin_date',css_class='col-md-6'),
                     css_class='row',
                     ),
                Div(
                     Div('prophylactic_measures_antibiotic_prophylaxis_other',css_class='col-md-6'),
                     Div('prophylactic_measures_antibiotic_prophylaxis_other_date',css_class='col-md-6'),
                     css_class='row',
                     ),
                ),
            Fieldset(
                'Vaccinations',
                Div(
                     Div('prophylactic_measures_vaccinations_pneumococcal_OCV',css_class='col-md-6'),
                     Div('prophylactic_measures_vaccinations_pneumococcal_OCV_date',css_class='col-md-6'),
                     css_class='row',
                     ),
                Div(
                     Div('prophylactic_measures_vaccination_other',css_class='col-md-6'),
                     css_class='row',
                     ),
                ),
            Fieldset(
                '<b>B. Monitoring tests annual</b>',),
            Fieldset(
                'Liver profile',
                Div(
                     Div('monitoring_tests_annual_liver_profile',css_class='col-md-6'),
                     Div('monitoring_tests_annual_liver_profile_date',css_class='col-md-6'),
                     css_class='row',
                     ),
                ),
            Fieldset(
                'Renal profile',
                Div(
                     Div('monitoring_tests_annual_renal_profile_blood_urea',css_class='col-md-6'),
                     Div('monitoring_tests_annual_renal_profile_blood_urea_date',css_class='col-md-6'),
                     css_class='row',
                     ),
                Div(
                     Div('monitoring_tests_annual_renal_profile_creatine',css_class='col-md-6'),
                     Div('monitoring_tests_annual_renal_profile_creatine_date',css_class='col-md-6'),
                     css_class='row',
                ),
                Div(
                    Div('monitoring_tests_annual_renal_profile_proteiuria',css_class='col-md-6'),
                    Div('monitoring_tests_annual_renal_profile_proteiuria_date',css_class='col-md-6'),
                )

            ),
            Fieldset(
                'Serrum ferritin',
                Div(
                     Div('monitoring_tests_annual_serum_ferritin',css_class='col-md-6'),
                     css_class='row',
                     ),
                ),
            Fieldset(
                'Calcium metabolism',
                Div(
                     Div('monitoring_tests_annual_calcium_metabolism_serum_calcium',css_class='col-md-3'),
                     Div('monitoring_tests_annual_calcium_metabolism_vitamin_D_level',css_class='col-md-4'),
                     Div('monitoring_tests_annual_calcium_metabolism_parathormone_level',css_class='col-md-5'),
                     css_class='row',
                     ),
                ),
            Fieldset(
                'Parvovirus serology',
                Div(
                    Div('monitoring_tests_annual_parvovirus_serology',css_class='col-md-6'),
                    Div('monitoring_tests_annual_parvovirus_serology_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                'Pulmonary function',
                Div(
                    Div('monitoring_tests_annual_pulmonary_function',css_class='col-md-6'),
                    Div('monitoring_tests_annual_pulmonary_function_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                'Hepatic ultrasound',
                Div(
                    Div('monitoring_tests_annual_hepatic_ultrasound',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                'Hip radiology (after 6 years)',
                Div(
                    Div('monitoring_tests_annual_hip_radiology',css_class='col-md-6'),
                    Div('monitoring_tests_annual_hip_radiology_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                'Opthalmic evaluation',
                Div(
                    Div('monitoring_tests_annual_ophthalmic_evaluation',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '<b>C. Compilations</b>'
            ),
            Fieldset(
                '1. Dactylitis (hand/foot syndrome)',
                 Div(
                    Div('complications_dactylitis',css_class='col-md-6'),
                    Div('complications_dactylitis_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '2. Stroke',
                 Div(
                    Div('complications_stroke',css_class='col-md-6'),
                    Div('complications_stroke_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '3. Splenic sequestration',
                 Div(
                    Div('complications_splenic_sequestration',css_class='col-md-6'),
                    Div('complications_splenic_sequestration_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '4. Aplastic crisis',
                 Div(
                    Div('complications_aplastic_crisis',css_class='col-md-6'),
                    Div('complications_aplastic_crisis_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '5. Acute chest syndrome',
                 Div(
                    Div('complications_acute_chest_syndrome',css_class='col-md-6'),
                    Div('complications_acute_chest_syndrome_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '6. Multi-organ failure syndrome',
                 Div(
                    Div('complications_multi_organ_failure_syndrome',css_class='col-md-6'),
                    Div('complications_multi_organ_failure_syndrome_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '7. Priapism',
                 Div(
                    Div('complications_priapism',css_class='col-md-6'),
                    Div('complications_priapism_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '8. Heart failure',
                 Div(
                    Div('complications_heart_failure',css_class='col-md-6'),
                    Div('complications_heart_failure_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '9. Pulmonary hypertension',
                 Div(
                    Div('complications_pulmonary_hypertension',css_class='col-md-6'),
                    Div('complications_pulmonary_hypertension_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '10. Allo-immunisation',
                 Div(
                    Div('complications_allo_immunation',css_class='col-md-6'),
                    Div('complications_allo_immunation_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '11. Iron overload',
                 Div(
                    Div('complications_iron_overload',css_class='col-md-6'),
                    Div('complications_iron_overload_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '12. Serious infection',
                 Div(
                    Div('complications_serious_infection',css_class='col-md-6'),
                    Div('complications_serious_infection_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
            Fieldset(
                '13. Azoospermia',
                 Div(
                    Div('complications_azoospermia',css_class='col-md-6'),
                    Div('complications_azoospermia_date',css_class='col-md-6'),
                    css_class='row',
                )
            ),
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")

        )

        self.helper.form_tag = False
        self.helper.form_show_labels = True


    class Meta:
        model = Clinical_data_two
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')

class DiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(DiagnosisForm, self).__init__(*args, **kwargs)

        self.fields['diagnosis_circumstances_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.helper=FormHelper(form=self)

        # self.fields['icd_10_desc']= forms.ModelChoiceField(queryset=icd_10.objects.all(),
        #                             widget=autocomplete_light.ChoiceWidget("icd_10Autocomplete"))

        diagnosis_option_value = (
        ('b-thalassaemia syndromes', 'b-thalassaemia syndromes',),
        ('a-thalassaemia syndromes', 'a-thalassaemia syndromes'),
        ('Sickle cell syndromes', 'Sickle cell syndromes'),
        ('Other haemoglobin variants','Other haemoglobin variants'),
        ('Red cell membrane disorders','Red cell membrane disorders'),
        ('Red cell enzyme disorders','Red cell enzyme disorders'),
        ('Congenital dyserythropoietic anaemias','Congenital dyserythropoietic anaemias')
    )
        self.fields['diagnosis_option']=forms.MultipleChoiceField(choices=DiagnosisOption.objects.all().values_list('id','diag_option'), widget=forms.CheckboxSelectMultiple())
        #self.fields['icd_10_desc']=forms.MultipleChoiceField(label='ICD 10 description', choices=icd_10.objects.all().values_list('id','icd_10_desc'), widget=autocomplete.ModelSelect2Multiple())
        self.fields['icd_10_desc'].label = 'ICD-10 description'
        self.fields['orpha_code'].label = 'Orpha code description'


        diagnosis_circumstances_value = (
        ('Antenatal diagnosis','Antenatal diagnosis'),
        ('Neonatal diagnosis','Neonatal diagnosis'),
        ('By the presence of affected related','By the presence of affected related'),
        ('Clinical diagnosis', 'Clinical diagnosis'),
        ('Other','Other')

        )
        self.fields['diagnosis_circumstances']=forms.MultipleChoiceField(choices=diagnosis_circumstances_value, widget=forms.CheckboxSelectMultiple())
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'

        #self.helper.form_class = 'forms-horizontal'
        self.helper.layout = Layout(
            Fieldset (
                # 'patient',
                '<b>Diagnosis information</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('age_of_diagnosis',css_class='col-md-6'),
                    Div('age_at_onset_of_symptoms',css_class="col-md-6"),
                    css_class='row',
                    ),



                'diagnosis_option',
                'record_of_genotype',


                'icd_10_desc',
                'orpha_code',
                'comment',
                ),

            Fieldset(
                '<b>Diagnosis circumstances</b>',
                'diagnosis_circumstances',
                'diagnosis_circumstances_date',
                #'diagnosis_circumstances_caring_year',
                ),



            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Diagnosis
        exclude = ['patient', 'author']

        list_display = ('patient', 'pub_date', 'author')
        widgets = {
        'icd_10_desc': autocomplete.ModelSelect2Multiple(url='icd10-autocomplete'),
        'orpha_code': autocomplete.ModelSelect2Multiple(url='orpha-autocomplete')
        }
        #widgets={'icd_10_desc' : autocomplete.ModelSelect2Multiple(url='icd10-autocomplete' )}
        # autocomplete_js_attribute={'name': 'icd_10_code'}

    # def clean_diagnosis_option(self):
    #     self.fields['diagnosis_option'] = self.cleaned_data['diagnosis_option']
    #     if not self.fields['diagnosis_option']:
    #         raise forms.ValidationError("...")
    #
    #     self.fields['diagnosis_option'] = ' '.join(self.fields['diagnosis_option'])
    #     print(self.fields['diagnosis_option'])
    #     return self.fields['diagnosis_option']



class A_b_sickle_thalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(A_b_sickle_thalForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-9'
        self.helper.label_class = 'col-md-3'

        self.helper.layout = Layout(
            Fieldset (
                # 'patient',
                '<b>CBC</b>',

                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('hb',css_class='col-md-2'),
                    Div(HTML('g/dl'), css_class="col-md-2"),
                    Div('mcv',css_class="col-md-2"),
                    Div(HTML("fl"), css_class="col-md-2"),
                    Div('mch',css_class="col-md-2"),
                    Div(HTML("pg"), css_class="col-md-1"),
                    css_class='row',
                    ),

                 Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('nrbc',css_class='col-md-2'),
                    Div(HTML('/100 WBC'), css_class="col-md-2"),
                    Div('reticulocytes',css_class="col-md-5"),
                    Div(HTML("%"), css_class="col-md-1"),
                    Div('red_cell_morphology', css_class="col-md-9"),

                    css_class='row',
                    ),

                ),
            Fieldset (
                '<b>Haemoglobin pattern analysis</b>',

                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Celluloce acetate electrophoresis, pH 8.6</b></h4></div><br/><br/>'),
                    Div('cell_acetate_electr',css_class='col-md-6'),
                    Div('cell_acetate_electr_comment',css_class="col-md-6"),
                    css_class='row',
                    ),

                Div(
                    HTML(u'<br/><div class="col-md-9"><h4><b>Acid Agarose or citrate agar pH 6.0</b></h4></div><br/><br/>'),
                    Div('acid_agarose_citrate',css_class='col-md-6'),
                    Div('acid_agarose_citrate_comment',css_class="col-md-6"),
                    css_class='row',
                    ),

                Div(
                    HTML(u'<br/><div class="col-md-9"><h4><b>Isoelectric focusing</b></h4></div><br/><br/>'),
                    Div('isoelect_foc',css_class='col-md-6'),
                    Div('isoelect_foc_comment',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<br/><div class="col-md-9"><h4><b>HPLC or Capillary Electrophoresis</b></h4></div><br/><br/>'),
                    Div('hlpc_cap_elect',css_class='col-md-6'),
                    Div('hlpc_cap_elect_comment',css_class="col-md-6"),
                    css_class='row',
                    ),

                 Div(
                    HTML(u'<div class="col-md-12"><h4><b>Quantizations</b></h4></div><br/><br/>'),
                    Div('quant_hba2',css_class='col-md-2'),
                    Div(HTML('%'), css_class="col-md-1"),
                    Div('quant_hbh',css_class="col-md-2"),
                    Div(HTML("%"), css_class="col-md-1"),
                    Div('quant_hbf', css_class="col-md-2"),
                    Div(HTML("%"), css_class="col-md-1"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<br/><div class="col-md-9"><h4><b>HPLC or Capillary Electrophoresis</b></h4></div><br/><br/>'),
                    Div('quant_other_var',css_class='col-md-6'),
                    Div('quantity',css_class="col-md-5"),
                    css_class='row',
                    ),


                'conf_pres_hbs',
                'conf_pres_hbe',
                Div(
                    HTML(u'<br/><div class="col-md-9"><h4><b>Confirm the presence of unstable haemoglobin</b></h4></div><br/><br/>'),
                    Div('conf_pres_un_haemo_isoprop_option',css_class='col-md-6'),
                    Div('conf_pres_un_haemo_isoprop',css_class="col-md-6"),
                    #Div('conf_pres_un_haemo_heat_option',css_class='col-md-6'),
                    #Div('conf_pres_un_haemo_heat',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    Div('conf_pres_un_haemo_heat_option',css_class='col-md-6'),
                    Div('conf_pres_un_haemo_heat',css_class="col-md-6"),
                    css_class='row',
                    ),


                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Exclusion of iron deficiency</b></h4></div><br/><br/>'),
                    Div('conf_pres_un_haemo_ex_ir_transf_sat',css_class='col-md-8'),
                    Div(HTML('%'), css_class="col-md-2"),
                    Div('conf_pres_un_haemo_ex_ir_transf_serum',css_class="col-md-8"),
                    Div(HTML("mg/L"), css_class="col-md-2"),
                    Div('conf_pres_un_haemo_ex_ir_transf_zinc',css_class="col-md-8"),
                    #Div(HTML("%"), css_class="col-md-1"),
                    css_class='row',
                    ),


            ),
            Fieldset (
                '<b>Molecular diagnosis confirming and characterizing a-thalassaemia</b>',
                'mol_diag_a_thal_gap_pcr',
                'mol_diag_a_thal_gap_mpla',
                'mol_diag_a_thal_gap_seq',
            ),
            Fieldset (
                '<b>Molecular diagnosis of b-thalassaemia</b>',
                'mol_diag_b_thal_aso',
                'mol_diag_b_thal_reverse_dot_blot',
                'mol_diag_b_thal_oligonucl',
                'mol_diag_b_thal_arms',
                'mol_diag_b_thal_real_time_pcr',
                'mol_diag_b_thal_dgge',
                'mol_diag_b_thal_gap_pcr',
                'mol_diag_b_thal_mpla',
                 HTML(u'<div class="col-md-12"><h4><b>Molecular mutations</b></h4></div><br/><br/>'),
                'mol_diag_b_thal_seq_anal_a_gene',
                'mol_diag_b_thal_seq_anal_b_gene',
                'mol_diag_b_thal_seq_anal_g_gene',
            ),
            Fieldset(
                '<b>Pertaining SNPs</b>',
                'snp_gene',
                'snp_code',

                Div(
                    #HTML(u'<div class="col-md-9"><h4><b>Transfusion history</b></h4></div><br/><br/>'),
                    Div('snp_allele1', css_class="col-md-6"),
                    #HTML("years<br/>"),
                    Div('snp_allele1_type',css_class="col-md-6"),
                    Div('snp_allele2', css_class="col-md-6"),
                    Div('snp_allele2_type', css_class="col-md-6"),

                    css_class='row',
                    ),
                ),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = A_b_sickle_thal
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')

class Redcell_enzyme_disForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Redcell_enzyme_disForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Enzymes of glycolysis</b>',

                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Hexokinase (HK)</b></h4></div><br/><br/>'),
                    Div('hk_option', css_class="col-md-6"),
                    Div('hk',css_class="col-md-6"),
                    css_class='row',
                    ),
                 Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glucosephosphate isomerase (GPI)</b></h4></div><br/><br/>'),
                    Div('gpi_option', css_class="col-md-6"),
                    Div('gpi',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Phosphofructokinase (PFK)</b></h4></div><br/><br/>'),
                    Div('pfk_option', css_class="col-md-6"),
                    Div('pfk',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glyceraldehyde-3-phosphate dehydrogenase</b></h4></div><br/><br/>'),
                    Div('g3ph_option', css_class="col-md-6"),
                    Div('g3ph',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Phosphoglycerate kinase (PGK)</b></h4></div><br/><br/>'),
                    Div('pgk_option', css_class="col-md-6"),
                    Div('pgk',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Pyruvate kinase (PK)</b></h4></div><br/><br/>'),
                    Div('pk_option', css_class="col-md-6"),
                    Div('pk_v',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Triosephorate isomerase (TPI)</b></h4></div><br/><br/>'),
                    Div('tpi_option', css_class="col-md-6"),
                    Div('tpi',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Lactate dehydrogenase (LDH)</b></h4></div><br/><br/>'),
                    Div('ldh_option', css_class="col-md-6"),
                    Div('ldh',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Adolase</b></h4></div><br/><br/>'),
                    Div('adolase_option', css_class="col-md-6"),
                    Div('adolase',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Enolase</b></h4></div><br/><br/>'),
                    Div('enolase_option', css_class="col-md-6"),
                    Div('enolase',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Biphosphoglycerate mutase (BPGM)</b></h4></div><br/><br/>'),
                    Div('bpgm_option', css_class="col-md-6"),
                    Div('bpgm',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Monophosphoglycerate mutase (MPGM)</b></h4></div><br/><br/>'),
                    Div('mpgm_option', css_class="col-md-6"),
                    Div('mpgm',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Phosphocluconate mutase (PGM)</b></h4></div><br/><br/>'),
                    Div('pgm_option', css_class="col-md-6"),
                    Div('pgm',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Enzymes of hwxose-monophosphate shunt and glutathione metabolism</b>',

                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glucose-6-phosphate dehydrogenase (G6PD)</b></h4></div><br/><br/>'),
                    Div('g6pd_option', css_class="col-md-6"),
                    Div('g6pd',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>6-phosphogluconate dehydrogenase (6-PGD)</b></h4></div><br/><br/>'),
                    Div('no6pgd_option', css_class="col-md-6"),
                    Div('no6pgd',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Gamma-glutamylcysteine synthetase (GCS)</b></h4></div><br/><br/>'),
                    Div('gcs_option', css_class="col-md-6"),
                    Div('gcs',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glutathione synthetase (GSH-S)</b></h4></div><br/><br/>'),
                    Div('gshs_option', css_class="col-md-6"),
                    Div('gshs',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glutathione reductase (GR)</b></h4></div><br/><br/>'),
                    Div('gr_option', css_class="col-md-6"),
                    Div('gr',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glutathione peroxidase (GSH-Px)</b></h4></div><br/><br/>'),
                    Div('gshpx_option', css_class="col-md-6"),
                    Div('gshpx',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Glutathione s-transferase (GST)</b></h4></div><br/><br/>'),
                    Div('gst_option', css_class="col-md-6"),
                    Div('gst',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Enzymes of nucleotide metabolism</b>',

                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Adenylate kinase (AK)</b></h4></div><br/><br/>'),
                    Div('ak_option', css_class="col-md-6"),
                    Div('ak',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Pyrimidine-5 nucleotidase</b></h4></div><br/><br/>'),
                    Div('pyr5nuc_option', css_class="col-md-6"),
                    Div('pyr5nuc',css_class="col-md-6"),
                    css_class='row',
                    ),
                 Div(
                    HTML(u'<div class="col-md-9"><h4><b>Purine/pyrimidine nucleotides ratio</b></h4></div><br/><br/>'),
                    Div('pur_pyr_ratio_option', css_class="col-md-6"),
                    Div('pur_pur_ratio',css_class="col-md-6"),
                    css_class='row',
                    ),
                 ),
            Fieldset(
                '<b>Other red blood cell enzyme activities</b>',

                Div(
                    HTML(u'<div class="col-md-9"><h4><b>NADH diaphorase</b></h4></div><br/><br/>'),
                    Div('nadh_dia_option', css_class="col-md-6"),
                    Div('nadh_dia',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>NADPH diaphorase</b></h4></div><br/><br/>'),
                    Div('nadph_dia_option', css_class="col-md-6"),
                    Div('nadph_dia_act',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Superoxide dismutase</b></h4></div><br/><br/>'),
                    Div('sod_option', css_class="col-md-6"),
                    Div('sod_act',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    HTML(u'<div class="col-md-9"><h4><b>Catalase</b></h4></div><br/><br/>'),
                    Div('catalase_option', css_class="col-md-6"),
                    Div('catalase',css_class="col-md-6"),
                    Div('other', css_class="col-md-6"),
                    Div('other_option',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Glycolysis intermediates</b>',


                 Div(
                    #HTML(u'<div class="col-md-9"><h4><b>Catalase</b></h4></div><br/><br/>'),
                    Div('g6p', css_class="col-md-6"),
                    Div('f6p',css_class="col-md-6"),
                    Div('fbp',css_class="col-md-6"),
                    Div('dhap',css_class="col-md-6"),
                    Div('gap',css_class="col-md-6"),
                    Div('no2_3dpg',css_class="col-md-6"),
                    Div('no3pga',css_class="col-md-6"),
                    Div('no2pga',css_class="col-md-6"),
                    Div('pep',css_class="col-md-6"),
                    Div('amp',css_class="col-md-6"),
                    Div('ab',css_class="col-md-6"),
                    Div('atp',css_class="col-md-6"),

                    ),

                Div(
                    Div('gssg_gsp', css_class="col-md-6"),
                    Div('pyr', css_class="col-md-6"),
                    Div('lact', css_class="col-md-6"),
                    css_class='row',
                    ),

            ),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Redcell_enzyme_dis
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')

class Redcell_membrane_disForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Redcell_membrane_disForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
             Fieldset(
                '<b>Diagnostic Tests Performed</b>',
                # 'patient',

                Div(
                    #HTML(u'<div class="col-md-9"><h4><b>NADH diaphorase</b></h4></div><br/><br/>'),
                    Div('red_cell_morph_sm', css_class="col-md-6"),
                    Div('osm_fr_fresh_blood',css_class="col-md-6"),
                    Div('osm_fr_pre_incu_blood',css_class="col-md-6"),
                    Div('osm_fr_two_dif_nacl',css_class="col-md-6"),
                    Div('osm_fr_curve_str',css_class="col-md-6"),
                    Div('osm_fr_curve',css_class="col-md-6"),
                    Div('glt',css_class="col-md-6"),
                    Div('aglt',css_class="col-md-6"),
                    Div('cryohemolysis_tst',css_class="col-md-6"),
                    Div('pink_tst',css_class="col-md-6"),
                    Div('flow_commercial_tst',css_class="col-md-6"),
                    Div('sds_page_rbc_proteins',css_class="col-md-6"),
                    Div('ektacytometer',css_class="col-md-6"),
                    Div('lorrca',css_class="col-md-6"),
                    Div('rbc_retic_auto_prm',css_class="col-md-6"),
                    Div('molec_char_rna_dna_level',css_class="col-md-6"),
                    Div('method_best_sensi_speci',css_class="col-md-6"),
                    css_class='row',
                    ),

             ),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Redcell_membrane_dis
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')

class Cong_dyseryth_anaemiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cong_dyseryth_anaemiaForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Diagnostic Tests</b>',
                Div(
                        #HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('complt_blood_cnt',css_class='col-md-6'),
                        Div('abs_reticulo_cnt',css_class="col-md-6"),
                        Div('soluble_transf_recept',css_class="col-md-6"),
                        Div('bone_marrow_recept',css_class="col-md-6"),

                        css_class='row',
                        ),
                Div('sds_page'),


                Div(
                        HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('moleculare_analysis',css_class='col-md-6'),
                        Div('moleculare_analysis_comment',css_class="col-md-6"),
                        css_class='row',
                        ),
                ),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Cong_dyseryth_anaemia
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')


class Patient_Reported_outcomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Patient_Reported_outcomeForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Patient reported outcomes</b>',
                Div(
                        #HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('days_missed_from_school',css_class='col-md-12'),
                        Div('days_missed_from_work',css_class="col-md-12"),
                        Div('transfusion_times',css_class="col-md-12"),
                        Div('distance_from_center',css_class="col-md-12"),

                        css_class='row',
                        ),
                ),

            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Patient_reported_outcome
        exclude = ['patient', 'author']
        list_display = ('patient', 'pub_date', 'author')


class UserCreationForm(forms.Form):
     def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        #self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)

        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'

        #self.helper.layout = Layout(Fieldset('Summary Card'))
        for i, question in enumerate(extra):

            if question == 'Demographics':
                self.fields['%s' % question] = forms.CharField(label=question, required=False)
            else:
                self.fields['%s' % question] = forms.CharField(label=question, required=False)
                self.fields['%s' % question].widget.attrs['readonly'] = True
                print (self.fields['%s' % question].label)
                #yield (self.fields['%s' % question].label, question)


class ExternalCentersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExternalCentersForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Center Information</b>',
                Div(
                        #HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('location_of_center',css_class='col-md-6'),
                        Div('name_of_center',css_class="col-md-6"),
                        Div('type_of_center',css_class="col-md-6"),
                        css_class='row',
                        ),

                Div(
                        #HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('center_address',css_class='col-md-6'),
                        Div('center_city',css_class="col-md-6"),
                        Div('center_country',css_class="col-md-6"),
                        css_class='row',
                        ),
                ),


            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Ext_centers
        exclude = ['center_id', 'author']
        list_display = ('title', 'pub_date', 'author')


class ExternalCentersDiagnosticForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExternalCentersDiagnosticForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>Diagnostic categories</b>',
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>B-Thalassaemia major</b></h4></div>'),
                        Div('diagn_categ_b_thal_major_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_b_thal_major_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Non transfusion dependent</b></h4></div>'),
                        Div('diagn_categ_non_transfusion_dep_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_non_transfusion_dep_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>HbH Disease</b></h4></div>'),
                        Div('diagn_categ_hbh_disease_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_hbh_disease_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),

                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Sickle cell disease SS</b></h4></div>'),
                        Div('diagn_categ_sickle_ss_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_sickle_ss_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),

                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Sickle cell disease SC</b></h4></div>'),
                        Div('diagn_categ_sickle_sc_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_sickle_sc_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>SCD S/b-thalassaemia</b></h4></div>'),
                        Div('diagn_categ_scd_s_b_thal_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_scd_s_b_thal_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Other SCD</b></h4></div>'),
                        Div('diagn_categ_other_scd_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_other_scd_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hereditary Spherocytosis</b></h4></div>'),
                        Div('diagn_categ_hered_sphero_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_hered_sphero_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hereditary Elliptocytosis</b></h4></div>'),
                        Div('diagn_categ_hered_ellipto_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_hered_ellipto_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Pyropoikilocytosis</b></h4></div>'),
                        Div('diagn_categ_pyropoikilc_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pyropoikilc_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),

                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Stomatocytosis</b></h4></div>'),
                        Div('diagn_categ_stomatoc_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_stomatoc_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Southern Asian Ovalocytosis</b></h4></div>'),
                        Div('diagn_categ_south_asian_oval_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_south_asian_oval_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>CDA type I</b></h4></div>'),
                        Div('diagn_categ_cda_type_i_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_cda_type_i_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>CDA type II</b></h4></div>'),
                        Div('diagn_categ_cda_type_ii_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_cda_type_ii_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>CDA type III</b></h4></div>'),
                        Div('diagn_categ_cda_type_iii_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_cda_type_iii_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>G6PD deficiency</b></h4></div>'),
                        Div('diagn_categ_g6pd_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_g6pd_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Pyruvate kinase deficiency</b></h4></div>'),
                        Div('diagn_categ_pyruvate_k_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pyruvate_k_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hexokinase deficiency</b></h4></div>'),
                        Div('diagn_categ_hexokinase_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_hexokinase_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GPI deficiency</b></h4></div>'),
                        Div('diagn_categ_gpi_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gpi_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>PFK deficiency</b></h4></div>'),
                        Div('diagn_categ_pfk_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pfk_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>PGK deficiency</b></h4></div>'),
                        Div('diagn_categ_pgk_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pgk_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>TPI deficiency</b></h4></div>'),
                        Div('diagn_categ_tpi_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_tpi_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>LDH deficiency</b></h4></div>'),
                        Div('diagn_categ_ldh_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_ldh_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Aldolase deficiency</b></h4></div>'),
                        Div('diagn_categ_aldolase_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_aldolase_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Enolase deficiency</b></h4></div>'),
                        Div('diagn_categ_enolase_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_enolase_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>BPGM deficiency</b></h4></div>'),
                        Div('diagn_categ_bpgm_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_bpgm_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>MPGM deficiency</b></h4></div>'),
                        Div('diagn_categ_mpgm_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_mpgm_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>PGM deficiency</b></h4></div>'),
                        Div('diagn_categ_pgm_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pgm_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>6-PGD deficiency</b></h4></div>'),
                        Div('diagn_categ_6pgd_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_6pgd_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GCS deficiency</b></h4></div>'),
                        Div('diagn_categ_gcs_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gcs_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GSH-S deficiency</b></h4></div>'),
                        Div('diagn_categ_gsh_s_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gsh_s_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GR deficiency</b></h4></div>'),
                        Div('diagn_categ_gr_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gr_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GSH-Px deficiency</b></h4></div>'),
                        Div('diagn_categ_gsh_px_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gsh_px_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>GST deficiency</b></h4></div>'),
                        Div('diagn_categ_gst_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_gst_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>AK deficiency</b></h4></div>'),
                        Div('diagn_categ_ak_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_ak_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Pyrimidine-5&#39; nucleotidase</b></h4></div>'),
                        Div('diagn_categ_p5_nuc_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_p5_nuc_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>NADH diaphorase deficiency</b></h4></div>'),
                        Div('diagn_categ_nadh_dia_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_nadh_dia_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>NADPH diaphorase deficiency</b></h4></div>'),
                        Div('diagn_categ_nadph_dia_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_nadph_dia_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>SOD diaphorase deficiency</b></h4></div>'),
                        Div('diagn_categ_sod_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_sod_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Catalase deficiency</b></h4></div>'),
                        Div('diagn_categ_catalas_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_catalas_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Diamond-Blackfan anaemia</b></h4></div>'),
                        Div('diagn_categ_diamond_blackfan_anae_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_diamond_blackfan_anae_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Fanconi anaemia</b></h4></div>'),
                        Div('diagn_categ_fanconi_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_fanconi_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hereditary or Congenital Sideroblastic anaemia</b></h4></div>'),
                        Div('diagn_categ_here_congenit_side_anaemia_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_here_congenit_side_anaemia_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Aceruloplasminemia</b></h4></div>'),
                        Div('diagn_categ_aceruloplasm_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_aceruloplasm_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Atrasferrinemia</b></h4></div>'),
                        Div('diagn_categ_atransfer_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_atransfer_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>DMT1-deficiency anaemia</b></h4></div>'),
                        Div('diagn_categ_dmt1_def_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_dmt1_def_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Iron refractory iron deficiency anaemia (IRIDA)</b></h4></div>'),
                        Div('diagn_categ_irida_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_irida_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Paroxysmal nocturnal haemoglobinuria (PNH)</b></h4></div>'),
                        Div('diagn_categ_pnh_no_patient',css_class='col-md-6'),
                        Div('diagn_categ_pnh_distribution',css_class="col-md-6"),
                        css_class='row',
                        ),


                ),
            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Ext_centers
        exclude = ['center_id', 'author']
        list_display = ('title', 'pub_date', 'author')

class ExternalCentersOutcomesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExternalCentersOutcomesForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>1. Deaths</b>',
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2010</b></h4></div>'),
                        Div('outcomes_year2010_thal',css_class='col-md-6'),
                        Div('outcomes_year2010_sickle',css_class="col-md-6"),
                        Div('outcomes_year2010_rare',css_class="col-md-6"),
                        css_class='row',
                        ),

                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2011</b></h4></div>'),
                        Div('outcomes_year2011_thal',css_class='col-md-6'),
                        Div('outcomes_year2011_sickle',css_class="col-md-6"),
                        Div('outcomes_year2011_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2012</b></h4></div>'),
                        Div('outcomes_year2012_thal',css_class='col-md-6'),
                        Div('outcomes_year2012_sickle',css_class="col-md-6"),
                        Div('outcomes_year2012_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2013</b></h4></div>'),
                        Div('outcomes_year2013_thal',css_class='col-md-6'),
                        Div('outcomes_year2013_sickle',css_class="col-md-6"),
                        Div('outcomes_year2013_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2014</b></h4></div>'),
                        Div('outcomes_year2014_thal',css_class='col-md-6'),
                        Div('outcomes_year2014_sickle',css_class="col-md-6"),
                        Div('outcomes_year2014_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>2015</b></h4></div>'),
                        Div('outcomes_year2015_thal',css_class='col-md-6'),
                        Div('outcomes_year2015_sickle',css_class="col-md-6"),
                        Div('outcomes_year2015_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                ),
            Fieldset(
                 '<b>2. Causes of death in the last 5 years</b>',
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Anaemia</b></h4></div>'),
                        Div('anaemia_thal',css_class='col-md-6'),
                        Div('anaemia_sickle',css_class="col-md-6"),
                        Div('anaemia_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Cardiac</b></h4></div>'),
                        Div('cardiac_thal',css_class='col-md-6'),
                        Div('cardiac_sickle',css_class="col-md-6"),
                        Div('cardiac_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Infection</b></h4></div>'),
                        Div('infection_thal',css_class='col-md-6'),
                        Div('infection_sickle',css_class="col-md-6"),
                        Div('infection_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hepatic</b></h4></div>'),
                        Div('hepatic_thal',css_class='col-md-6'),
                        Div('hepatic_sickle',css_class="col-md-6"),
                        Div('hepatic_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Malignancy</b></h4></div>'),
                        Div('malignancy_thal',css_class='col-md-6'),
                        Div('malignancy_sickle',css_class="col-md-6"),
                        Div('malignancy_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Other</b></h4></div>'),
                        Div('other_thal',css_class='col-md-6'),
                        Div('other_sickle',css_class="col-md-6"),
                        Div('other_rare',css_class="col-md-6"),
                        css_class='row',
                        ),
            ),


            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Ext_centers
        exclude = ['center_id', 'author']
        list_display = ('title', 'pub_date', 'author')


class ExternalCentersOutcomes2Form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExternalCentersOutcomes2Form, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset(
                '<b>2. More measurements</b>',
                Div(
                        #HTML(u'<br/><div class="col-md-9"><h4><b>Molecular analysis</b></h4></div><br/><br/>'),
                        Div('out_patients_married',css_class='col-md-6'),
                        Div('out_patients_divorced',css_class="col-md-6"),
                        Div('out_patients_single',css_class="col-md-6"),
                        Div('out_patients_cohabiting',css_class="col-md-6"),
                        Div('out_patients_parented_children',css_class="col-md-6"),
                        Div('out_thal_women_preg',css_class="col-md-6"),
                        Div('out_patients_splene',css_class="col-md-6"),
                        css_class='row',
                        ),
                ),
            Fieldset(
                '<b>Complications measurements</b>',

                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Cholelithiasis</b></h4></div>'),
                        Div('choleitithiasis_hb',css_class='col-md-6'),
                        Div('choleitithiasis_ra',css_class="col-md-6"),
                        Div('choleitithiasis_per_hb',css_class="col-md-6"),
                        Div('choleitithiasis_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Heart failure</b></h4></div>'),
                        Div('heart_f_hb',css_class='col-md-6'),
                        Div('heart_f_ra',css_class="col-md-6"),
                        Div('heart_f_per_hb',css_class="col-md-6"),
                        Div('heart_f_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Arrythmias</b></h4></div>'),
                        Div('arryth_hb',css_class='col-md-6'),
                        Div('arryth_ra',css_class="col-md-6"),
                        Div('arryth_per_hb',css_class="col-md-6"),
                        Div('arryth_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Pulmonary hypertension</b></h4></div>'),
                        Div('pulm_hyp_hb',css_class='col-md-6'),
                        Div('pulm_hyp_ra',css_class="col-md-6"),
                        Div('pulm_hyp_per_hb',css_class="col-md-6"),
                        Div('pulm_hyp_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Glucose intolerance</b></h4></div>'),
                        Div('gluc_int_hb',css_class='col-md-6'),
                        Div('gluc_int_ra',css_class="col-md-6"),
                        Div('gluc_int_per_hb',css_class="col-md-6"),
                        Div('gluc_int_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Diabetes</b></h4></div>'),
                        Div('diab_hb',css_class='col-md-6'),
                        Div('diab_ra',css_class="col-md-6"),
                        Div('diab_per_hb',css_class="col-md-6"),
                        Div('diab_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hypogonadism</b></h4></div>'),
                        Div('hypogon_hb',css_class='col-md-6'),
                        Div('hypogon_ra',css_class="col-md-6"),
                        Div('hypogon_per_hb',css_class="col-md-6"),
                        Div('hypogon_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hypothyroidism</b></h4></div>'),
                        Div('hypothyr_hb',css_class='col-md-6'),
                        Div('hypothyr_ra',css_class="col-md-6"),
                        Div('hypothyr_per_hb',css_class="col-md-6"),
                        Div('hypothyr_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hypoparathyroidism</b></h4></div>'),
                        Div('hypoparath_hb',css_class='col-md-6'),
                        Div('hypoparath_ra',css_class="col-md-6"),
                        Div('hypoparath_per_hb',css_class="col-md-6"),
                        Div('hypoparath_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Liver fibrosis/cirrhosis</b></h4></div>'),
                        Div('liver_hb',css_class='col-md-6'),
                        Div('liver_ra',css_class="col-md-6"),
                        Div('liver_per_hb',css_class="col-md-6"),
                        Div('liver_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>HCV infections</b></h4></div>'),
                        Div('hcv_hb',css_class='col-md-6'),
                        Div('hcv_ra',css_class="col-md-6"),
                        Div('hcv_per_hb',css_class="col-md-6"),
                        Div('hcv_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hepatocellular carcinoma</b></h4></div>'),
                        Div('hypatoc_hb',css_class='col-md-6'),
                        Div('hypatoc_ra',css_class="col-md-6"),
                        Div('hypatoc_per_hb',css_class="col-md-6"),
                        Div('hypatoc_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Other malignancy</b></h4></div>'),
                        Div('other_mal_hb',css_class='col-md-6'),
                        Div('other_mal_ra',css_class="col-md-6"),
                        Div('other_mal_per_hb',css_class="col-md-6"),
                        Div('other_mal_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Osteoporosis</b></h4></div>'),
                        Div('osteopor_hb',css_class='col-md-6'),
                        Div('osteopor_ra',css_class="col-md-6"),
                        Div('osteopor_per_hb',css_class="col-md-6"),
                        Div('osteopor_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Osteomyelitis</b></h4></div>'),
                        Div('osteomye_hb',css_class='col-md-6'),
                        Div('osteomye_ra',css_class="col-md-6"),
                        Div('osteomye_per_hb',css_class="col-md-6"),
                        Div('osteomye_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Thromboembolism</b></h4></div>'),
                        Div('thrombo_hb',css_class='col-md-6'),
                        Div('thrombo_ra',css_class="col-md-6"),
                        Div('thrombo_per_hb',css_class="col-md-6"),
                        Div('thrombo_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Dactylitis</b></h4></div>'),
                        Div('dact_hb',css_class='col-md-6'),
                        Div('dact_ra',css_class="col-md-6"),
                        Div('dact_per_hb',css_class="col-md-6"),
                        Div('dact_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Splenic sequestration</b></h4></div>'),
                        Div('splenic_seq_hb',css_class='col-md-6'),
                        Div('splenic_seq_ra',css_class="col-md-6"),
                        Div('splenic_seq_per_hb',css_class="col-md-6"),
                        Div('splenic_seq_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Liver sequestration</b></h4></div>'),
                        Div('liver_seq_hb',css_class='col-md-6'),
                        Div('liver_seq_ra',css_class="col-md-6"),
                        Div('liver_seq_per_hb',css_class="col-md-6"),
                        Div('liver_seq_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Mesenteric syndrome</b></h4></div>'),
                        Div('mes_synd_hb',css_class='col-md-6'),
                        Div('mes_synd_ra',css_class="col-md-6"),
                        Div('mes_synd_per_hb',css_class="col-md-6"),
                        Div('mes_synd_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Aplastic crisis</b></h4></div>'),
                        Div('aplas_cris_hb',css_class='col-md-6'),
                        Div('aplas_cris_ra',css_class="col-md-6"),
                        Div('aplas_cris_per_hb',css_class="col-md-6"),
                        Div('aplas_cris_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Hyperhaemilysis</b></h4></div>'),
                        Div('hyperhae_hb',css_class='col-md-6'),
                        Div('hyperhae_ra',css_class="col-md-6"),
                        Div('hyperhae_per_hb',css_class="col-md-6"),
                        Div('hyperhae_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Stroke</b></h4></div>'),
                        Div('stroke_hb',css_class='col-md-6'),
                        Div('stroke_ra',css_class="col-md-6"),
                        Div('stroke_per_hb',css_class="col-md-6"),
                        Div('stroke_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Silent infarct</b></h4></div>'),
                        Div('sil_inf_hb',css_class='col-md-6'),
                        Div('sil_inf_ra',css_class="col-md-6"),
                        Div('sil_inf_per_hb',css_class="col-md-6"),
                        Div('sil_inf_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Acute chest syndrome</b></h4></div>'),
                        Div('ac_chest_synd_hb',css_class='col-md-6'),
                        Div('ac_chest_synd_ra',css_class="col-md-6"),
                        Div('ac_chest_synd_per_hb',css_class="col-md-6"),
                        Div('ac_chest_synd_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Priapism</b></h4></div>'),
                        Div('priap_hb',css_class='col-md-6'),
                        Div('priap_ra',css_class="col-md-6"),
                        Div('priap_per_hb',css_class="col-md-6"),
                        Div('priap_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Avascular necrosis femoral head</b></h4></div>'),
                        Div('ava_nec_fem_hd_hb',css_class='col-md-6'),
                        Div('ava_nec_fem_hd_ra',css_class="col-md-6"),
                        Div('ava_nec_fem_hd_per_hb',css_class="col-md-6"),
                        Div('ava_nec_fem_hd_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Retinopathy</b></h4></div>'),
                        Div('retin_hb',css_class='col-md-6'),
                        Div('retin_ra',css_class="col-md-6"),
                        Div('retin_per_hb',css_class="col-md-6"),
                        Div('retin_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                Div(
                        HTML(u'<div class="col-md-9"><h4><b>Kidney disease</b></h4></div>'),
                        Div('kid_dis_hb',css_class='col-md-6'),
                        Div('kid_dis_ra',css_class="col-md-6"),
                        Div('kid_dis_per_hb',css_class="col-md-6"),
                        Div('kid_dis_per_ra',css_class="col-md-6"),
                        css_class='row',
                        ),
                ),


            FormActions(
                Submit('submit', "Save changes"),
                Submit('cancel',"Cancel")
            ),
        )
        self.helper.form_tag = False
        self.helper.form_show_labels = True

    class Meta:
        model = Ext_centers
        exclude = ['center_id', 'author']
        list_display = ('title', 'pub_date', 'author')


