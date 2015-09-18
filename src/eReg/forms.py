from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset, MultiWidgetField,MultiField
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup, FormActions
from functools import partial
from django.contrib.admin import widgets
from models import Demographic
from models import Diagnosis, A_b_sickle_thal, Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, Pregnancy, Clinical_data
from sympy import pretty_print as pp, latex

import autocomplete_light
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
        exclude = ['age']

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
        self.fields['current_treatment_chelation_drug']=forms.MultipleChoiceField(choices=current_treatment_chelation_drug_option, widget=forms.CheckboxSelectMultiple(),required=False)
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
        exclude = ['patient']

class DiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(DiagnosisForm, self).__init__(*args, **kwargs)

        self.fields['diagnosis_circumstances_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        # self.fields['clinical_data_date_of_examination']= forms.DateField(label=('Date of examination'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_cholelithiasis_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_cholecystectomy_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_splenectomy_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_iron_overload_heart_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_heart_failure_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_cardiac_arrythmia_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_glucose_intolerance_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_diabetes_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_hypothyroidism_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_hypoparathyroidism_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_hypogonadism_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_iron_overload_liver_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_others_date']= forms.DateField(label=('Date measured'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))

        self.helper=FormHelper(form=self)

        self.fields['icd_10_desc']= forms.ModelChoiceField(queryset=icd_10.objects.all(),
                                    widget=autocomplete_light.ChoiceWidget("icd_10Autocomplete"))
        self.fields['icd_10_desc'].label = "ICD-10 description"
        diagnosis_option_value = (
        ('b-thalassaemia syndromes', 'b-thalassaemia syndromes'),
        ('a-thalassaemia syndromes', 'a-thalassaemia syndromes'),
        ('Sickle cell syndromes', 'Sickle cell syndromes'),
        ('Other haemoglobin variants','Other haemoglobin variants'),
        ('Rare cell membrane disorders','Rare cell membrane disorders'),
        ('Rare cell enzyme disorders','Rare cell enzyme disorders'),
        ('Congenital dyserythropoietic anaemias','Congenital dyserythropoietic anaemias')
    )
        self.fields['diagnosis_option']=forms.MultipleChoiceField(choices=diagnosis_option_value, widget=forms.CheckboxSelectMultiple())

        diag_sub_options =(
            ('a-thalassaemia silent trait(a+)','a-thalassaemia silent trait(a+)'),
            ('a-thalassaemia trait a^o aa|-- a-|a-','a-thalassaemia trait  a^o aa|--  a-|a-' ),
            ('a-thalassaemia Hb disease','a-thalassaemia Hb disease'),
            ('a-thalassaemia hydrops fetalis','a-thalassaemia hydrops fetalis'),
            ('b-thalassaemia trait', 'b-thalassaemia trait'),
            ('b-thalassaemia Intermedia', 'b-thalassaemia Intermedia'),
            ('b-thalassaemia Major', 'b-thalassaemia Major'),
        )
        self.fields['comment']=forms.MultipleChoiceField(choices=diag_sub_options, widget=forms.CheckboxSelectMultiple())

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
                'icd_10_code',
                'orpha_code',
                'comment',
                ),

            Fieldset(
                '<b>Diagnosis circumstances</b>',
                'diagnosis_circumstances',
                'diagnosis_circumstances_date',
                #'diagnosis_circumstances_caring_year',
                ),
            # Fieldset(
            #     '<b>Clinical data</b>',
            #     'clinical_data_date_of_examination',
            #     'clinical_data_weight',
            #     'clinical_data_height',
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_cholelithiasis',css_class='col-md-6'),
            #         Div('clinical_data_cholelithiasis_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #      Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_cholecystectomy',css_class='col-md-6'),
            #         Div('clinical_data_cholecystectomy_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #      Div(
            #         #HTML(u'<div class="col-md-2"></div>'),,
            #         Div('clinical_data_splenectomy',css_class='col-md-6'),
            #         Div('clinical_data_splenectomy_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #      Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_iron_overload_heart',css_class='col-md-6'),
            #         Div('clinical_data_iron_overload_heart_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_heart_failure',css_class='col-md-6'),
            #         Div('clinical_data_heart_failure_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_cardiac_arrythmia',css_class='col-md-6'),
            #         Div('clinical_data_cardiac_arrythmia_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_glucose_intolerance',css_class='col-md-6'),
            #         Div('clinical_data_glucose_intolerance_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_diabetes',css_class='col-md-6'),
            #         Div('clinical_data_diabetes_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_hypothyroidism',css_class='col-md-6'),
            #         Div('clinical_data_hypothyroidism_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_hypoparathyroidism',css_class='col-md-6'),
            #         Div('clinical_data_hypoparathyroidism_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_hypogonadism',css_class='col-md-6'),
            #         Div('clinical_data_hypogonadism_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_iron_overload_liver',css_class='col-md-6'),
            #         Div('clinical_data_iron_overload_liver_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #     Div(
            #         #HTML(u'<div class="col-md-2"></div>'),
            #         Div('clinical_data_others',css_class='col-md-6'),
            #         Div('clinical_data_others_date',css_class="col-md-5"),
            #         css_class='row',
            #         ),
            #    ),


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
                    HTML(u'<div class="col-md-9"><h4><b>Quantizations</b></h4></div><br/><br/>'),
                    Div('quant_hba2',css_class='col-md-2'),
                    Div(HTML('%'), css_class="col-md-2"),
                    Div('quant_hbh',css_class="col-md-2"),
                    Div(HTML("%"), css_class="col-md-2"),
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
                 HTML(u'<div class="col-md-9"><h4><b>Molecular mutations</b></h4></div><br/><br/>'),
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
        exclude = ['patient']

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
        exclude = ['patient']

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
        exclude = ['patient']

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
        exclude = ['patient']

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
                #print (self.fields['%s' % question].label)
                #yield (self.fields['%s' % question].label, question)

