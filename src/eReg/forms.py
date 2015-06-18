from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset, MultiWidgetField,MultiField
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup, FormActions
from functools import partial
from django.contrib.admin import widgets
from models import Demographic
from models import Diagnosis, A_b_sickle_thal, Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, Pregnancy, Clinical_data, Outcome_measures, Life_events
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
                    Div('blood_group',css_class="col-md-6"),
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
                    Div('address_no',css_class='col-md-4'),
                    Div('address_street',css_class="col-md-4"),
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
                '<b>Preferred Health Professional/Legal organization</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('legal_org_name',css_class='col-md-4'),
                    Div('legal_org_phone',css_class="col-md-4"),
                    Div('legal_org_email',css_class="col-md-4"),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Contact person</b>',
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
                    Div('paternity',css_class="col-md-6"),
                    #Div('maternity',css_class="col-md-6"),
                    #Div('no_of_children',css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    #Div('family_situation',css_class='col-md-6'),
                    #Div('paternity',css_class="col-md-6"),
                    Div('maternity',css_class="col-md-6"),
                    Div('no_of_children',css_class="col-md-6"),
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

        self.fields['clinical_data_cholelithiasis_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_cholecystectomy_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_splenectomy_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_iron_overload_heart_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_heart_failure_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_cardiac_arrythmia_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_glucose_intolerance_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_diabetes_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_hypothyroidism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_hypoparathyroidism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_hypogonadism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['clinical_data_iron_overload_liver_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['clinical_data_others_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_one_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_two_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_serrum_three_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))


        self.fields['assessment_of_iron_load_liver_mri_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.fields['assessment_of_iron_load_fibroscan_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        #YEAR ONLY
        self.fields['current_treatment_chelation_start']= forms.DateField(label=('Start of chelation therapy'),required=False,
        widget=DateTimePicker(options={"format": "YYYY",
                                       "pickTime": False,
                                       "startDate": "1900"}))

        self.fields['current_treatment_bone_marrow_date']= forms.DateField(label=('Date of occurrence'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))

        self.helper=FormHelper(form=self)
        self.helper.field_class = 'col-md-8'
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
                '<h2>Diagnostic tests</h2>',
                'clinical_data_date_of_examination',
                'clinical_data_weight',
                'clinical_data_height',
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
                '<b>Assessment of iron load serrum</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_one',css_class='col-md-6'),
                    Div('assessment_of_iron_load_serrum_one_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_two',css_class='col-md-6'),
                    Div('assessment_of_iron_load_serrum_two_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_serrum_three',css_class='col-md-6'),
                    Div('assessment_of_iron_load_serrum_three_date',css_class="col-md-5"),
                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('assessment_of_iron_load_liver_mri',css_class='col-md-6'),
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
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div( 'assessment_of_iron_load_ti_bassal_per_hbf',css_class='col-md-6'),
                    css_class='row',
                    ),
                ),
            Fieldset(
                '<b>Serological data</b>',
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
                    Div('current_treatment_chelation_drug',css_class="col-md-5"),
                    css_class='row',
                    ),
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
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_hepatitis_treatment_c',css_class="col-md-6"),
                    Div('current_treatment_hepatitis_treatment_b',css_class='col-md-6'),

                    css_class='row',
                    ),
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('current_treatment_by_hydroxyurea',css_class="col-md-6"),
                    Div('current_treatment_by_hydroxyurea_with_epo',css_class='col-md-6'),
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
        # self.fields['clinical_data_cholelithiasis_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_cholecystectomy_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_splenectomy_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_iron_overload_heart_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_heart_failure_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_cardiac_arrythmia_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_glucose_intolerance_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_diabetes_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_hypothyroidism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_hypoparathyroidism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_hypogonadism_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        # self.fields['clinical_data_iron_overload_liver_date']= forms.DateField(label=('Date of occurrence'),required=False,
        # widget=DateTimePicker(options={"format": "YYYY-MM-DD",
        #                                "pickTime": False,
        #                                "startDate": "1900-01-01"}))
        #
        #
        # self.fields['clinical_data_others_date']= forms.DateField(label=('Date of occurrence'),required=False,
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
            Field('diagnosis_genotype'),
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
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
            Fieldset (
                # 'patient',
                '<b>Tests</b>',
                'cbc',
                'hb',
                'mcv',
                'mch',
                'hba2',
                'hbf',
                'haemoglobin',
                'nrbc',
                'reticulocytes',
                'red_cell_morphology',),
            Fieldset (
                '<b>Haemoglobin pattern analysis</b>',
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
                'mol_diag_b_thal_seq_anal_a_gene',
                'mol_diag_b_thal_seq_anal_b_gene',
                'mol_diag_b_thal_seq_anal_g_gene',
            ),
            Fieldset(
                '<b>Pertaining SNPs</b>',
                'snp_gene',
                'snp_code',
                'snp_allele1',
                'snp_allele1_type',
                'snp_allele2',
                'snp_allele2_type',
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
                '<b>Tests</b>',
                # 'patient',
                #'enzymes_of_glycol_option',
                #'enzymes_of_glycol',
                'hk_option',
                'hk',
                'gpi_option',
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
                #'enz_hexose_option',
                #'enz_hexose',
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
                #'enz_nuc_meta_option',
                #'enz_nuc_meta',
                'ak_option',
                'ak',
                'pyr5nuc_option',
                'pyr5nuc',
                'pur_pyr_ratio_option',
                'pur_pur_ratio',
                #'other_rbce_act_option',
                #'other_rbce_act',
                'nadh_dia_option',
                'nadh_dia',
                'nadph_dia_option',
                'nadph_dia_act',
                'sod_option',
                'sod_act',
                'catalase_option',
                'catalase',
                'other_option',
                #'glycol_interm_option',
                #'glycol_interm',
                #'g6p_option',
                'g6p',
                #'f6p_option',
                'f6p',
                #'fbp_option',
                'fbp',
                #'dhap_option',
                'dhap',
                #'gap_option',
                'gap',
                #'no2_3dpg_option',
                'no2_3dpg',
                #'no3pga_option',
                'no3pga',
                #'no2pga_option',
                'no2pga',
                #'pep_option',
                'pep',
                #'amp_option',
                'amp',
                #'ab_option',
                'ab',
                #'atp_option',
                'atp',
                #'gssg_gsh_option',
                'gssg_gsp',
                #'pyr_option',
                'pyr',
                #'lact_option',
                'lact',
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
                '<b>Tests</b>',
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


class OutcomeMeasuresForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OutcomeMeasuresForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.fields['date_of_transition_from_irregular_to_regular_tranfusions']= forms.DateField(label=('Date of transition from irregular to regular tranfusions'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(
             Fieldset (
                '<b>Mortality</b>',
                Div(
                    #HTML(u'<div class="col-md-2"></div>'),
                    Div('mortality_date_of_death',css_class='col-md-6'),
                    Div('mortality_cause_of_death',css_class="col-md-6"),
                    css_class='row',
                    ),
                ),
             Fieldset(
                '<b>Clinical Information</b>',
                Div(
                    Div('age_of_first_transfusion', css_class="col-md-6"),
                    #HTML("years<br/>"),
                    Div('transfusion_depentent_anaemia', css_class="col-md-6"),
                    Div('date_of_transition_from_irregular_to_regular_tranfusions', css_class="col-md-6"),
                    Div('splenomegaly', css_class="col-md-6"),
                    css_class='row',
                    ),
                Div(
                    Div('t2_of_heart', css_class="col-md-6"),
                    Div('r2_of_heart',css_class="col-md-6"),
                    Div('pre_transfusion_hb_level_mid_year', css_class="col-md-6"),
                    Div('pre_transfusion_hb_level_end_of_year', css_class="col-md-6"),
                    Div('serum_ferritin', css_class="col-md-6"),
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
        model = Outcome_measures
        exclude = ['patient', 'date_of_input']


class LifeEventsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LifeEventsForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        #self.fields['patient'].queryset = Demographic.objects.filter(patient_id=self.instance.patient)
        self.fields['HSCT_date']= forms.DateField(label=('Date'),required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False,
                                       "startDate": "1900-01-01"}))
        self.helper.field_class = 'col-md-8'
        self.helper.label_class = 'col-md-3'
        self.helper.layout = Layout(

             Fieldset (
                '<b>Hematopoietic Stem Cell Transplantation</b>',

                Div(
                    Div('HSCT_date',css_class='col-md-6'),
                    Div('HSCT_outcome',css_class="col-md-6"),
                    Div('partaker_in_clinical_trial', css_class='col-md-6'),
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
        model = Life_events
        exclude = ['patient', 'date_of_input']