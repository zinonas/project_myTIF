from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, ButtonHolder, Fieldset, MultiWidgetField
from crispy_forms.bootstrap import TabHolder, Tab, Accordion, AccordionGroup, FormActions
from functools import partial
from django.contrib.admin import widgets
from models import demographic
from models import diagnosis


class DemographicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DemographicForm, self).__init__(*args, **kwargs)
        self.helper=FormHelper(self)
        self.fields['date_of_birth'].widget = widgets.AdminDateWidget()
        self.helper.layout = Layout(
           TabHolder(
                        Tab('Demographics Information',
                            'national_health_care_pat_id',
                            'patient_hospital_file_number',
                            'patient_id',
                            'given_name',
                            'surname',
                            'date_of_birth',
                            'education',
                            'profession',
                            'family',
                            'address_street',
                            'address_no',
                            'address_city',
                            'address_post_code',
                            'address_state',
                            'address_country',
                            'telephone',
                            'email',
                            'legal_org_name',
                            'legal_org_phone',
                            'legal_org_email',
                            'contact_person_role',
                            'contact_person_name',
                            'contact_person_phone',
                            'contact_person_email',
                            'insurance_no',),

                        #Tab('Diagnosis'),
                        #Tab('More Diagnosis')
            ),
                    FormActions(
                        Submit('submit', "Save changes"),
                        Submit('cancel',"Cancel")
                    ),

                )



        self.helper.form_tag = False
        self.helper.form_show_labels = True



    class Meta:
        model = demographic

class DiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        inlines = (DemographicForm)
        super(DiagnosisForm, self).__init__(*args, **kwargs)
        DemographicForm.helper=FormHelper(self)
        DemographicForm.helper.layout = Layout(
               TabHolder(
                            Tab('Diagnosis',
                                'patient',),

                            #Tab('Diagnosis'),
                            #Tab('More Diagnosis')
                ),
                        #FormActions(
                        #    Submit('submit', "Save changes"),
                        #   Submit('cancel',"Cancel")
                        #),

                    )

        DemographicForm.helper.form_tag = False
        DemographicForm.helper.form_show_labels = True

    class Meta:
        model = diagnosis