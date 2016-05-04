# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets
from django.utils.encoding import smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.conf import settings
# Create Demographic models here



class Demographic(models.Model):
    anonymisation_code = models.IntegerField('Anonymisation code', null=True,blank=True)
    patient_option = (
        ('','Please select'),
        ('I agree','I agree'),
        ('I do not agree','I do not agree')
    )
    patient_consent_for_data_storage= models.CharField('Data Storage', max_length=20,choices=patient_option, default=patient_option[0][0])
    patient_consent_for_data_reusage= models.CharField('Data Reuse',max_length=20,choices=patient_option, default=patient_option[0][0])
    creation_of_consent_form = models.DateField('Creation date')
    data_provider = (
        ('','Please select'),
        #('Provider','Provider'),
        ('Patient','Patient'),
        ('Other', 'Other')
    )
    data_entered_by = models.CharField('Entered by',max_length=15,choices=data_provider, default=data_provider[0][0])
    data_entered_by_name = models.CharField('Other name', max_length=30,null=True,blank=True)
    data_entered_by_relationship =  models.CharField('Other relationship',max_length=30,null=True,blank=True)
    national_health_care_pat_id = models.IntegerField('National Health Care patient id', null=True,blank=True)
    guid =  models.IntegerField('Global unique identifier', null=True,blank=True)
    patient_hospital_file_number = models.IntegerField(null=True,blank=True)
    patient_id = models.IntegerField(unique= True ,primary_key=True)
    given_name = models.CharField(max_length=30,null=True,blank=True)
    surname = models.CharField(max_length=30,null=True,blank=True)
    middle_name = models.CharField('Middle name',max_length=30,null=True,blank=True)
    maiden_name = models.CharField('Maiden name',max_length=30,null=True,blank=True)
    date_of_birth= models.DateField('Date of birth',null=True,blank=True)
    country_of_birth = models.CharField(max_length=30,null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    # def __str__(self):
    #     today = date.today()
    #     delta = relativedelta(today, self.date_of_birth)
    #     return str(delta.years)

    gender_option = (
        ('','Please select'),
        ('Male','Male'),
        ('Female','Female')
    )
    gender = models.CharField(max_length=6,null=True,blank=True, choices=gender_option, default=gender_option[0][0])
    race = models.CharField('Race/Ethnicity',max_length=30,null=True,blank=True)


    family = models.CharField('Family name',max_length=15,null=True,blank=True)
    address_street = models.CharField('Address',max_length=25,null=True,blank=True)
    #address_no = models.IntegerField('Number',null=True,blank=True)
    address_city = models.CharField('City',max_length=25,null=True,blank=True)
    address_post_code = models.IntegerField('Post code',null=True,blank=True)
    address_state = models.CharField('State',max_length=25,null=True,blank=True)
    address_country = models.CharField('Country',max_length=25,null=True,blank=True)
    telephone = models.IntegerField(null=True,blank=True)
    email = models.EmailField('E-mail',null=True,blank=True)
    legal_org_clinic=models.CharField('Hospital/Clinic',max_length=25,null=True,blank=True)
    legal_org_name = models.CharField('Name',max_length=30,null=True,blank=True)
    legal_org_phone = models.IntegerField('Telephone',null=True,blank=True)
    legal_org_email = models.EmailField('E-mail',null=True,blank=True)
    contact_person_role = models.CharField('Role',max_length=20,null=True,blank=True)
    contact_person_name = models.CharField('Name',max_length=30,null=True,blank=True)
    contact_person_surname = models.CharField('Surname',max_length=30,null=True,blank=True)
    cp_address_street = models.CharField('Street',max_length=25,null=True,blank=True)
    cp_address_no = models.IntegerField('Number',null=True,blank=True)
    cp_address_city = models.CharField('City',max_length=25,null=True,blank=True)
    cp_address_post_code = models.IntegerField('Post code',null=True,blank=True)
    cp_address_state = models.CharField('State',max_length=25,null=True,blank=True)
    cp_address_country = models.CharField('Country',max_length=25,null=True,blank=True)
    contact_person_phone = models.IntegerField('Telephone', null=True,blank=True)
    contact_person_email = models.EmailField('E-mail',null=True,blank=True)
    insurance_no_public = models.IntegerField('National Insurance Number',null=True,blank=True)
    insurance_no_private = models.IntegerField('Private Insurance Number',null=True,blank=True)
    education_option = (
        ('','Please select'),
        ('Primary','Primary'),
        ('Secondary','Secondary'),
        ('University','University'),
        ('Other','Other')

    )
    education = models.CharField('Educational situation', max_length=20,null=True,blank=True, choices=education_option, default=education_option[0][0])
    father_education = models.CharField('Education of father', max_length=20,null=True,blank=True, choices=education_option, default=education_option[0][0])
    mother_education = models.CharField('Education of mother', max_length=20,null=True,blank=True, choices=education_option, default=education_option[0][0])
    profession_option = (
        ('','Please select'),
        ('Full time','Full time'),
        ('Part time', 'Part time'),
        ('Unemployed','Unemployed'),
    )
    profession= models.CharField('Professional situation (work)',max_length=20,null=True,blank=True, choices=profession_option, default=profession_option[0][0])
    family_situation_option = (
        ('', 'Please select'),
        ('single','single'),
        ('married','married'),
        ('marital cohabitation','marital cohabitation'),
        ('divorced', 'divorced')
    )
    family_situation = models.CharField('Family situation', max_length=20, null=True,blank=True, choices=family_situation_option, default=family_situation_option[0][0])
    data_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    #paternity = models.CharField('Paternity', max_length=3, null=True,blank=True, choices=data_option, default=data_option[0][0])
    no_of_children = models.IntegerField('Number of children',null=True,blank=True)
    #year of birth of each child
    #maternity = models.CharField('Maternity', max_length=3, null=True,blank=True, choices=data_option, default=data_option[0][0])
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)



    def __str__(self):
        return str(self.patient_id)

class icd_10(models.Model):
    id = models.IntegerField(unique=True,primary_key=True,null=False,blank=False)
    icd_10_desc = models.CharField('ICD-10 description',max_length=80,null=True,blank=True)
    icd_10_code = models.CharField('ICD-10 code',max_length=10,null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.icd_10_desc)

class Pregnancy(models.Model):
    patient = models.ForeignKey(Demographic)
    #pregnancy_id = models.AutoField(unique=True ,primary_key=True)
    year = models.DateField('Pregnancy year',null=True,blank=True)
    outcome_birth = models.CharField('Outcome birth',max_length=100,null=True,blank=True)
    other = models.CharField('Other',max_length=50, null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)


class Diagnosis(models.Model):
    patient = models.ForeignKey(Demographic)
    age_of_diagnosis = models.IntegerField(null=True,blank=True)
    age_at_onset_of_symptoms = models.IntegerField(null=True,blank=True)
    diagnosis_option_value = (
        ('', 'Please select a diagnosis'),
        ('b-thalassaemia syndromes', 'b-thalassaemia syndromes'),
        ('a-thalassaemia syndromes', 'a-thalassaemia syndromes'),
        ('Sickle cell syndromes', 'Sickle cell syndromes'),
        ('Other haemoglobin variants','Other haemoglobin variants'),
        ('Rare cell membrane disorders','Rare cell membrane disorders'),
        ('Rare cell enzyme disorders','Rare cell enzyme disorders'),
        ('Congenital dyserythropoietic anaemias','Congenital dyserythropoietic anaemias')
    )
    diagnosis_option = models.CharField( max_length=150)
    record_of_genotype = models.CharField(max_length=45,null=True,blank=True)
    # icd_10_code = models.ForeignKey(icd_10)
    icd_10_code = models.CharField('ICD-10 code', max_length=20,null=True,blank=True)
    # icd_10_desc = models.CharField('ICD-10 description',max_length=80,null=True,blank=True)
    icd_10_desc = models.ForeignKey(icd_10)
    orpha_code = models.CharField('Oprha code', max_length=20,null=True,blank=True)
    comment = models.CharField(max_length=100,null=True,blank=True)
    #diagnosis_genotype = models.CharField('Diagnosis genotype', max_length=100, null=True, blank=True)

    diagnosis_circumstances = models.CharField(max_length=150)
    diagnosis_circumstances_date = models.DateField('Date of diagnosis',null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)
    #diagnosis_circumstances_caring_year = models.DateField('Date of diagnosis',null=True,blank=True)
    # clinical_data_date_of_examination= models.DateField('Date of examination',null=True,blank=True)
    # clinical_data_weight = models.IntegerField('Weight (kg)', null=True,blank=True)
    # clinical_data_height = models.IntegerField('Height (cm)', null=True,blank=True)
    # clinical_data_option = (
    #     ('','Please select'),
    #     ('Yes','Yes'),
    #     ('No','No')
    # )
    # clinical_data_cholelithiasis = models.CharField('Cholelithiasis', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_cholelithiasis_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_cholecystectomy = models.CharField('Cholecystectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_cholecystectomy_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_splenectomy = models.CharField('Splenectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_splenectomy_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_iron_overload_heart = models.CharField('Iron overload heart', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_iron_overload_heart_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_heart_failure = models.CharField('Heart failure', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_heart_failure_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_cardiac_arrythmia = models.CharField('And/or cardiac arrythmia', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_cardiac_arrythmia_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_glucose_intolerance = models.CharField('Glucose intolerance', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_glucose_intolerance_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_diabetes = models.CharField('Diabetes', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_diabetes_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_hypothyroidism = models.CharField('Hypothyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_hypothyroidism_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_hypoparathyroidism = models.CharField('Hypoparathyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_hypoparathyroidism_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_hypogonadism = models.CharField('Hypogonadism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_hypogonadism_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_iron_overload_liver = models.CharField('Iron overload liver', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_iron_overload_liver_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_others = models.CharField('Others (Thromboembolism, cancers,...)', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # clinical_data_others_date = models.DateField('Date of occurrence',null=True,blank=True)
    # clinical_data_pregnancy_id = models.ForeignKey(Pregnancy)
    # assessment_of_iron_load_serrum_one= models.CharField('Measurement 1', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_serrum_one_date= models.DateField('Date of occurrence',null=True,blank=True)
    # assessment_of_iron_load_serrum_two= models.CharField('Measurement 2', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_serrum_two_date= models.DateField('Date of occurrence',null=True,blank=True)
    # assessment_of_iron_load_serrum_three= models.CharField('Measurement 3', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_serrum_three_date= models.DateField('Date of occurrence',null=True,blank=True)
    # assessment_of_iron_load_liver_mri= models.CharField('Liver MRI', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_liver_mri_date= models.DateField('Date of occurrence',null=True,blank=True)
    # assessment_of_iron_load_fibroscan= models.CharField('Fibroscan', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_fibroscan_date= models.DateField('Date of occurrence',null=True,blank=True)
    # assessment_of_iron_load_intra_hepatic_iron= models.CharField('Intra hepatic iron', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_method_mri= models.CharField('MRI', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_method_cardiac_iron= models.CharField('Cardiac iron/IRM', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_ti_bassal_hb_rate= models.CharField('Bassal Hb rate', max_length=10,null=True,blank=True)
    # assessment_of_iron_load_ti_bassal_per_hbf= models.CharField('Bassal % HbF rate', max_length=10,null=True,blank=True)
    # serological_data_option = (
    #     ('','Please select'),
    #     ('+','+'),
    #     ('-','-'),
    #     ('not done', 'not done')
    # )
    # serolocigal_data_HCV = models.CharField('HCV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    # serolocigal_data_HCV_PCR = models.CharField('HCV PCR', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    # serolocigal_data_HBV = models.CharField('HBV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    # serolocigal_data_HIV = models.CharField('HIV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    # current_treatment_transfusion_regime_option= (
    #     ('', 'Please select'),
    #     ('8 transfusions per year or more','8 transfusions per year or more' ),
    #     ('Occational','Occational'),
    #     ('Absent','Absent')
    # )
    # current_treatment_transfusion_regime = models.CharField('Transfusion regime', max_length=30,null=True,blank=True, choices=current_treatment_transfusion_regime_option, default=current_treatment_transfusion_regime_option[0][0])
    # current_treatment_chelation =  models.CharField('Chelation', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_chelation_start=models.DateField('Start of chelation therapy (year only)',null=True,blank=True)
    # current_treatment_chelation_drug= models.CharField('Current Chelator drug',max_length=15, null=True, blank=True)
    # current_treatment_bone_marrow =  models.CharField('Bone-marrow treatment',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_bone_marrow_date = models.DateField('Date of occurrence',null=True,blank=True)
    # current_treatment_bone_marrow_success =  models.CharField('Success',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_replacement_ther =  models.CharField('Replacement therapy: by thyroid stimulating Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_sex_horm =  models.CharField('By sexual Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_insulin =  models.CharField('By insulin',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_thyroid =  models.CharField('For parathyroid deficiency',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_hepatitis_option= (
    #     ('', 'Please select'),
    #     ('No','No' ),
    #     ('Current treatment','Current treatment'),
    #     ('Treatment in the past','Treatment in the past')
    # )
    # current_treatment_hepatitis_treatment_c =  models.CharField('Hepatitis treatment',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    # current_treatment_hepatitis_treatment_b =  models.CharField('Hepatitis treatment',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    # current_treatment_by_hydroxyurea = models.CharField('Treatment by Hydroxyurea',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    # current_treatment_by_hydroxyurea_with_epo = models.CharField('With EPO',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])

    def __str__(self):
        return str(self.patient)


class Clinical_data(models.Model):

    #clinical_data_id = models.IntegerField(unique=True ,primary_key=True)
    patient = models.ForeignKey(Demographic)
    clinical_data_date_of_examination= models.DateField('Date of examination',null=True,blank=True)
    clinical_data_weight = models.IntegerField('Weight', null=True,blank=True)
    clinical_data_height = models.IntegerField('Height', null=True,blank=True)
    clinical_data_spleen_size = models.IntegerField('Spleen size', null=True,blank=True)
    clinical_data_liver_size =  models.IntegerField('Liver size', null=True,blank=True)
    clinical_data_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    clinical_data_cholelithiasis = models.CharField('Cholelithiasis', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_cholelithiasis_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_cholecystectomy = models.CharField('Cholecystectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_cholecystectomy_date = models.DateField('Date of operation',null=True,blank=True)
    clinical_data_splenectomy = models.CharField('Splenectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_splenectomy_date = models.DateField('Date of operation',null=True,blank=True)
    clinical_data_iron_overload_heart = models.CharField('Iron overload heart', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_iron_overload_heart_date = models.DateField('Date measured',null=True,blank=True)
    clinical_data_heart_failure = models.CharField('Heart failure', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_heart_failure_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_cardiac_arrythmia = models.CharField('Cardiac arrythmia', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_cardiac_arrythmia_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_glucose_intolerance = models.CharField('Glucose intolerance', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_glucose_intolerance_date = models.DateField('Date measured',null=True,blank=True)
    clinical_data_diabetes = models.CharField('Diabetes', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_diabetes_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_hypothyroidism = models.CharField('Hypothyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_hypothyroidism_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_hypoparathyroidism = models.CharField('Hypoparathyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_hypoparathyroidism_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_hypogonadism = models.CharField('Hypogonadism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_hypogonadism_date = models.DateField('Date of diagnosis',null=True,blank=True)
    clinical_data_iron_overload_liver = models.CharField('Iron overload liver', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    clinical_data_iron_overload_liver_date = models.DateField('Date measured',null=True,blank=True)
    clinical_data_others = models.CharField('Others (Thromboembolism, cancers,...)', max_length=30, null=True, blank=True)
    clinical_data_others_date = models.DateField('Date of diagnosis',null=True,blank=True)
    #clinical_data_pregnancy_id = models.ForeignKey(Pregnancy)
    assessment_of_iron_load_serrum_one= models.CharField('Serrum ferritin 1', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_one_date= models.DateField('Date measured',null=True,blank=True)
    assessment_of_iron_load_serrum_two= models.CharField('Serrum ferritin 2', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_two_date= models.DateField('Date measured',null=True,blank=True)
    assessment_of_iron_load_serrum_three= models.CharField('Serrum ferritin 3', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_three_date= models.DateField('Date measured',null=True,blank=True)
    assessment_of_iron_load_liver_mri= models.CharField('Liver MRI', max_length=10,null=True,blank=True)
    assessment_of_iron_load_liver_mri_date= models.DateField('Date measured',null=True,blank=True)
    assessment_of_iron_load_fibroscan= models.CharField('Fibroscan', max_length=10,null=True,blank=True)
    assessment_of_iron_load_fibroscan_date= models.DateField('Date measured',null=True,blank=True)
    assessment_of_iron_load_intra_hepatic_iron= models.CharField('Liver biopsy', max_length=10,null=True,blank=True)
    assessment_of_iron_load_method_mri= models.DateField('Date measured', max_length=10,null=True,blank=True)
    assessment_of_iron_load_method_cardiac_iron= models.CharField('Cardiac iron T2<sup>*</sup>', max_length=10,null=True,blank=True)
    assessment_of_iron_load_ti_bassal_hb_rate= models.CharField('Bassal Hb rate', max_length=10,null=True,blank=True)

    serological_data_option = (
        ('','Please select'),
        ('+','+'),
        ('-','-'),
        ('not done', 'not done')
    )
    serological_data_date = models.DateField('Date positive', max_length=10,null=True,blank=True)
    serolocigal_data_HCV = models.CharField('HCV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HCV_PCR = models.CharField('HCV PCR', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HBV = models.CharField('HBV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HIV = models.CharField('HIV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    current_treatment_transfusion_regime_option= (
        ('', 'Please select'),
        ('8 transfusions per year or more','8 transfusions per year or more' ),
        ('Occational','Occational'),
        ('None','None')
    )
    current_treatment_transfusion_regime = models.CharField('Transfusion regime', max_length=150,null=True,blank=True)
    current_treatment_chelation =  models.CharField('Chelation', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    current_treatment_chelation_start=models.DateField('Start of chelation therapy (year only)',null=True,blank=True)

    current_treatment_chelation_drug= models.CharField('Current Chelator regime',max_length=25, null=True, blank=True)
    current_treatment_bone_marrow =  models.CharField('HSCT transplant',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_bone_marrow_date = models.DateField('Date measured',null=True,blank=True)
    current_treatment_bone_marrow_success =  models.CharField('HSCT outcome',max_length=15, null=True, blank=True)
    current_treatment_replacement_ther =  models.CharField('By thyroid stimulating Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_sex_horm =  models.CharField('By sexual Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_insulin =  models.CharField('By insulin',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_thyroid =  models.CharField('For parathyroid deficiency',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_hepatitis_option= (
        ('', 'Please select'),
        ('No','No' ),
        ('Current treatment','Current treatment'),
        ('Treatment in the past','Treatment in the past')
    )
    current_treatment_hepatitis_treatment_c =  models.CharField('Hepatitis C',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    current_treatment_hepatitis_treatment_b =  models.CharField('Hepatitis B',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    current_treatment_by_hydroxyurea = models.CharField('Treatment by Hydroxyurea',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_by_hydroxyurea_with_epo = models.CharField('With EPO',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_other =  models.CharField('Other',max_length=45, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    mortality_date_of_death = models.DateField('Date of death',null=True,blank=True)
    mortality_cause_of_death = models.CharField('Cause of death',max_length=100, null=True, blank=True)
    age_of_first_transfusion = models.IntegerField(null=True,blank=True)
    yesno_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    blood_group= models.CharField('Extended red cell antigens',max_length=25,null=True,blank=True)
    transfusion_depentent_anaemia= models.CharField('Transfusion dependent anaemia',max_length=100, null=True, blank=True, choices=yesno_option, default=yesno_option[0][0])
    date_of_transition_from_irregular_to_regular_tranfusions= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)



    def __str__(self):
        return str(self.patient)

class Clinical_data_two(models.Model):

    #clinical_data_id = models.IntegerField(unique=True ,primary_key=True)
    patient = models.ForeignKey(Demographic)
    clinical_data_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    prophylactic_measures_antibiotic_prophylaxis_penicillin = models.CharField('Penicillin', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    prophylactic_measures_antibiotic_prophylaxis_penicillin_date = models.DateField('Date started',null=True,blank=True)
    prophylactic_measures_antibiotic_prophylaxis_other = models.CharField('Other', max_length=30,null=True, blank=True)
    prophylactic_measures_antibiotic_prophylaxis_other_date = models.DateField('Date Started',null=True,blank=True)
    prophylactic_measures_vaccinations_pneumococcal_OCV = models.CharField('Pneumococcal OCV', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0],null=True, blank=True)
    prophylactic_measures_vaccinations_pneumococcal_OCV_date = models.DateField('Date given',null=True,blank=True)
    prophylactic_measures_vaccination_other = models.CharField('Other', max_length=30,null=True, blank=True)
    clinical_data_normal = (
        ('','Please select'),
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal')
    )
    monitoring_tests_annual_liver_profile = models.CharField('Liver profile', max_length=10, choices=clinical_data_normal,default=clinical_data_normal[0][0],null=True, blank=True)
    monitoring_tests_annual_liver_profile_date = models.DateField('Date abnormal',null=True,blank=True)
    monitoring_tests_annual_renal_profile_blood_urea = models.CharField('Blood urea Nitrogen', max_length=30,null=True, blank=True)
    monitoring_tests_annual_renal_profile_blood_urea_date = models.DateField('Date abnormal',null=True,blank=True)
    monitoring_tests_annual_renal_profile_creatine = models.CharField('Creatine', max_length=30,null=True, blank=True)
    monitoring_tests_annual_renal_profile_creatine_date = models.DateField('Date abnormal',null=True,blank=True)
    monitoring_tests_annual_renal_profile_proteiuria = models.CharField('Proteiuria (microalbuminuria)', max_length=30,null=True, blank=True)
    monitoring_tests_annual_renal_profile_proteiuria_date = models.DateField('Date detected',null=True,blank=True)
    monitoring_tests_annual_serum_ferritin = models.CharField('Serum Ferritin', max_length=50,null=True,blank=True)
    monitoring_tests_annual_calcium_metabolism_serum_calcium = models.CharField('Serum calcium', max_length=30,null=True, blank=True)
    monitoring_tests_annual_calcium_metabolism_vitamin_D_level = models.CharField('Vitamin D level', max_length=30,null=True, blank=True)
    monitoring_tests_annual_calcium_metabolism_parathormone_level = models.CharField('Parathormone level', max_length=30,null=True, blank=True)
    clinical_data_positive = (
        ('','Please select'),
        ('Positive', 'Positive'),
        ('Negative', 'Negative')
    )
    monitoring_tests_annual_parvovirus_serology = models.CharField('Parvovirus serology', max_length=10, choices=clinical_data_positive,default=clinical_data_positive[0][0], null=True, blank=True)
    monitoring_tests_annual_parvovirus_serology_date = models.DateField('Date found positive',null=True,blank=True)
    monitoring_tests_annual_pulmonary_function = models.CharField('Pulmonary function', max_length=10, choices=clinical_data_normal,default=clinical_data_normal[0][0], null=True, blank=True)
    monitoring_tests_annual_pulmonary_function_date = models.DateField('Date abnormal',null=True,blank=True)
    monitoring_tests_annual_hepatic_ultrasound = models.CharField('Hepatic ultrasound', max_length=50, null=True, blank=True)
    monitoring_tests_annual_hip_radiology = models.CharField('Hip radiology (after 6 years)', max_length=50, null=True, blank=True)
    monitoring_tests_annual_hip_radiology_date = models.DateField('Date abnormal',null=True,blank=True)
    monitoring_tests_annual_ophthalmic_evaluation = models.CharField('Ophthalmic evaluation', max_length=50, null=True, blank=True)
    complications_dactylitis = models.IntegerField('Age', null=True, blank=True)
    complications_dactylitis_date = models.DateField('Date',null=True,blank=True)
    complications_stroke = models.IntegerField('Age', null=True, blank=True)
    complications_stroke_date = models.DateField('Date',null=True,blank=True)
    complications_splenic_sequestration = models.IntegerField('Age', null=True, blank=True)
    complications_splenic_sequestration_date = models.DateField('Date',null=True,blank=True)
    complications_aplastic_crisis = models.IntegerField('Age', null=True, blank=True)
    complications_aplastic_crisis_date = models.DateField('Date',null=True,blank=True)
    complications_acute_chest_syndrome = models.IntegerField('Age', null=True, blank=True)
    complications_acute_chest_syndrome_date = models.DateField('Date',null=True,blank=True)
    complications_multi_organ_failure_syndrome = models.IntegerField('Age', null=True, blank=True)
    complications_multi_organ_failure_syndrome_date = models.DateField('Date',null=True,blank=True)
    complications_priapism = models.IntegerField('Age', null=True, blank=True)
    complications_priapism_date = models.DateField('Date',null=True,blank=True)
    complications_heart_failure = models.IntegerField('Age',null=True, blank=True)
    complications_heart_failure_date = models.DateField('Date',null=True,blank=True)
    complications_pulmonary_hypertension = models.IntegerField('Age', null=True, blank=True)
    complications_pulmonary_hypertension_date = models.DateField('Date',null=True,blank=True)
    complications_allo_immunation = models.IntegerField('Age', null=True, blank=True)
    complications_allo_immunation_date = models.DateField('Date',null=True,blank=True)
    complications_iron_overload = models.IntegerField('Age',null=True, blank=True)
    complications_iron_overload_date = models.DateField('Date',null=True,blank=True)
    complications_serious_infection = models.IntegerField('Age', null=True, blank=True)
    complications_serious_infection_date = models.DateField('Date',null=True,blank=True)
    complications_azoospermia = models.IntegerField('Age', null=True, blank=True)
    complications_azoospermia_date = models.DateField('Date',null=True,blank=True)
    treatment_modalities_regular_transfusions_date = models.DateField('Date started',null=True,blank=True)
    treatment_modalities_hydroxyurea_date = models.DateField('Date started',null=True,blank=True)
    treatment_modalities_hsct_date = models.DateField('Date performed',null=True,blank=True)
    treatment_modalities_hsct_outcome = models.CharField('Date performed',max_length=50,null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)

class A_b_sickle_thal (models.Model):
    patient= models.ForeignKey(Demographic)
    thal_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    plus_minus_option = (
        ('','Please select'),
        ('+','+'),
        ('-','-')
    )

    hb = models.IntegerField('Hb', null=True, blank=True)
    mcv = models.IntegerField('MCV', null=True, blank=True)
    mch = models.IntegerField('MCH', null=True, blank=True)


    nrbc  = models.CharField('NRBC', max_length=3, null=True, blank=True)
    reticulocytes = models.CharField('Reticulocytes', max_length=3, null=True, blank=True)
    red_cell_morphology  = models.CharField('Red cell morphology', max_length=20, null=True, blank=True)

    cell_acetate_electr  = models.CharField('Performed',max_length=3, choices =thal_option,null=True, blank=True)
    cell_acetate_electr_comment = models.CharField('Comment',max_length=25, null=True, blank=True)
    acid_agarose_citrate  = models.CharField('Performed',max_length=3, choices =thal_option,null=True, blank=True)
    acid_agarose_citrate_comment= models.CharField('Comment',max_length=25, null=True, blank=True)
    isoelect_foc  = models.CharField('Performed', max_length=3, choices =thal_option,null=True, blank=True)
    isoelect_foc_comment= models.CharField('Comment',max_length=25, null=True, blank=True)
    hlpc_cap_elect = models.CharField('Performed',max_length=3, choices =thal_option,null=True, blank=True)
    hlpc_cap_elect_comment= models.CharField('Comment',max_length=25, null=True, blank=True)

    quant_hba2  = models.IntegerField('HbA<sub>2</sub>',  null=True, blank=True)
    quant_hbh  = models.IntegerField('HbH', null=True, blank=True)
    quant_hbf  = models.IntegerField('HbF', null=True, blank=True)
    quant_other_var  = models.CharField('Other variant',max_length=15, null=True, blank=True)
    quantity = models.CharField('Quantity',max_length=3, null=True, blank=True)
    conf_pres_hbs  = models.CharField('Confirm the presence of an HbS by sickling test or a solubility test',max_length=3,null=True, blank=True, choices= thal_option, default= thal_option[0][0])
    conf_pres_hbe  = models.CharField('Confirm the presence of an HbE by the DCIP test',max_length=3,null=True, blank=True, choices= thal_option, default= thal_option[0][0])
    conf_pres_un_haemo_isoprop_option  = models.CharField('Isopropanol test',choices=thal_option,max_length=3, null=True, blank=True)
    conf_pres_un_haemo_isoprop  = models.CharField('Comment',max_length=25, null=True, blank=True)
    conf_pres_un_haemo_heat_option = models.CharField('Heat test', max_length=3, null=True, blank=True,choices= thal_option, default= thal_option[0][0])
    conf_pres_un_haemo_heat = models.CharField('Comment', max_length=25, null=True, blank=True)
    conf_pres_un_haemo_ex_ir_transf_sat  = models.CharField('Transferrin saturation/iron binding capacity',max_length=25, null=True, blank=True)
    conf_pres_un_haemo_ex_ir_transf_serum = models.CharField('Serrum ferritin', max_length=25, null=True, blank=True)
    conf_pres_un_haemo_ex_ir_transf_zinc  = models.CharField('Zinc protoporphyrin', max_length=25, null=True, blank=True)
    mol_diag_a_thal_gap_pcr = models.CharField('Gap-PCR (for deletion mutations)', max_length=3, null=True, blank=True)
    mol_diag_a_thal_gap_mpla = models.CharField('MPLA (for deletion mutations)', max_length=3, null=True, blank=True)
    mol_diag_a_thal_gap_seq = models.CharField('Sequence analysis (for non-deletion mutations',max_length=3, null=True, blank=True)
    mol_diag_b_thal_aso = models.CharField('Allele specific oligonucleotides (ASO)',max_length=25, null=True, blank=True)
    mol_diag_b_thal_reverse_dot_blot = models.CharField('Reverse dot blot analysis',max_length=25, null=True, blank=True)
    mol_diag_b_thal_oligonucl = models.CharField('Oligonucleotide microarrays',max_length=25, null=True, blank=True)
    mol_diag_b_thal_arms = models.CharField('Amplification Refractory mutation system (ARMS)',max_length=25, null=True, blank=True)
    mol_diag_b_thal_real_time_pcr = models.CharField('Real time PCR (for point mutations)',max_length=25, null=True, blank=True)
    mol_diag_b_thal_dgge = models.CharField('Denaturing Gradient Gel Electrophoresis (DGGE) for unknown mutations',max_length=25, null=True, blank=True)
    mol_diag_b_thal_gap_pcr = models.CharField('Gap PCR (for deletion mutations)',max_length=25, null=True, blank=True)
    mol_diag_b_thal_mpla = models.CharField('MPLA (for deletion and unknown mutations', max_length=25, null=True, blank=True)
    mol_diag_b_thal_seq_anal_a_gene = models.CharField(' a gene: allele 1/allele 2',max_length=25, null=True, blank=True)
    mol_diag_b_thal_seq_anal_b_gene = models.CharField(' β gene: allele 1/allele 2',max_length=25, null=True, blank=True)
    mol_diag_b_thal_seq_anal_g_gene  = models.CharField(' γ gene: allele 1/allele 2',max_length=25, null=True, blank=True)
    snp_gene  = models.CharField('Gene/Region',max_length=10, null=True, blank=True)
    snp_code = models.CharField('SNP (rs code)', max_length=10, null=True, blank=True)
    snp_allele_option=  (
        ('','Please select'),
        ('maternal','maternal'),
        ('paternal','paternal'),
        ('unknown', 'unknown')
    )
    snp_allele1 = models.CharField('Allele 1', max_length=10, null=True, blank=True)
    snp_allele1_type  = models.CharField('Allele 1 type', max_length=10, null=True, blank=True, choices=snp_allele_option, default=snp_allele_option[0][0])
    snp_allele2  = models.CharField('Allele 2',max_length=10, null=True, blank=True)
    snp_allele2_type = models.CharField('Allele 2 type',max_length=10, null=True, blank=True, choices=snp_allele_option, default=snp_allele_option[0][0])
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)


class Redcell_enzyme_dis (models.Model):
    patient = models.ForeignKey(Demographic)
    plus_minus_option = (
        ('','Please select'),
        ('Done','Done'),
        ('Not done','Not done')
    )
    #enzymes_of_glycol_option = models.CharField('Enzymes of glycolysis',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    #enzymes_of_glycol = models.CharField(max_length=45, null=True, blank=True)
    hk_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    hk = models.CharField('Comment',max_length=45, null=True, blank=True)
    gpi_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gpi = models.CharField('Comment',max_length=45, null=True, blank=True)
    pfk_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pfk = models.CharField('Comment',max_length=45, null=True, blank=True)
    g3ph_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    g3ph = models.CharField('Comment',max_length=45, null=True, blank=True)
    pgk_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pgk = models.CharField('Comment',max_length=45, null=True, blank=True)
    pk_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pk_v = models.CharField('Comment',max_length=45, null=True, blank=True)
    tpi_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    tpi = models.CharField('Comment',max_length=45, null=True, blank=True)
    ldh_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    ldh = models.CharField('Comment',max_length=45, null=True, blank=True)
    adolase_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    adolase = models.CharField('Comment',max_length=45, null=True, blank=True)
    enolase_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    enolase = models.CharField('Comment',max_length=45, null=True, blank=True)
    bpgm_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    bpgm = models.CharField('Comment',max_length=45, null=True, blank=True)
    mpgm_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    mpgm = models.CharField('Comment',max_length=45, null=True, blank=True)
    pgm_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pgm = models.CharField('Comment',max_length=45, null=True, blank=True)
    #enz_hexose_option = models.CharField('Enzymes of hexose-monophosphate shunt and glutathione metabolism',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    #enz_hexose = models.CharField(max_length=45, null=True, blank=True)
    cerumen_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    cerumen = models.CharField('Comment',max_length=45, null=True, blank=True)
    g6pd_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    g6pd = models.CharField('Comment',max_length=45, null=True, blank=True)
    no6pgd_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    no6pgd = models.CharField('Comment',max_length=45, null=True, blank=True)
    gcs_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gcs = models.CharField('Comment',max_length=45, null=True, blank=True)
    gshs_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gshs = models.CharField('Comment',max_length=45, null=True, blank=True)
    gr_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gr = models.CharField('Comment',max_length=45, null=True, blank=True)
    gshpx_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gshpx = models.CharField('Comment',max_length=45, null=True, blank=True)
    gst_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gst = models.CharField('Comment',max_length=45, null=True, blank=True)
    #enz_nuc_meta_option = models.CharField(max_length=3, null=True, blank=True)
    #enz_nuc_meta = models.CharField(max_length=45, null=True, blank=True)
    ak_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    ak = models.CharField('Comment',max_length=45, null=True, blank=True)
    pyr5nuc_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pyr5nuc = models.CharField('Comment',max_length=45, null=True, blank=True)
    pur_pyr_ratio_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pur_pur_ratio = models.CharField('Comment',max_length=45, null=True, blank=True)
    #other_rbce_act_option = models.CharField(max_length=3, null=True, blank=True)
    #other_rbce_act = models.CharField(max_length=45, null=True, blank=True)
    nadh_dia_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    nadh_dia = models.CharField('Comment',max_length=45, null=True, blank=True)
    nadph_dia_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    nadph_dia_act = models.CharField('Comment',max_length=45, null=True, blank=True)
    sod_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    sod_act = models.CharField('Comment',max_length=45, null=True, blank=True)
    catalase_option = models.CharField('Performed', max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    catalase = models.CharField('Comment',max_length=45, null=True, blank=True)
    other_option = models.CharField('Performed',max_length=13, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    other = models.CharField('Comment',max_length=45, null=True, blank=True)
    #glycol_interm_option = models.CharField(max_length=3, null=True, blank=True)
    #glycol_interm = models.CharField(max_length=45, null=True, blank=True)
    #g6p_option = models.CharField(max_length=3, null=True, blank=True)
    g6p = models.CharField('Glucose-6-phosphate (GP6)',max_length=45, null=True, blank=True)
    #f6p_option = models.CharField(max_length=3, null=True, blank=True)
    f6p = models.CharField('Fructose-6-phosphate (F6P)',max_length=45, null=True, blank=True)
    #fbp_option = models.CharField(max_length=3, null=True, blank=True)
    fbp = models.CharField('Fructose-bi-phosphate (FBP)',max_length=45, null=True, blank=True)
    #dhap_option = models.CharField(max_length=3, null=True, blank=True)
    dhap = models.CharField('Dihydroxyacetone-phosphate (DHAP)',max_length=45, null=True, blank=True)
    #ap_option = models.CharField(max_length=3, null=True, blank=True)
    gap = models.CharField('Glyceraldehyde-3-phosphate (GAP)',max_length=45, null=True, blank=True)
    #no2_3dpg_option = models.CharField(max_length=3, null=True, blank=True)
    no2_3dpg = models.CharField('2.3-diphosphoglycerate (2.3 DPG)',max_length=45, null=True, blank=True)
    #no3pga_option = models.CharField(max_length=3, null=True, blank=True)
    no3pga = models.CharField('3-phosphoglyceric acid (3PGA)',max_length=45, null=True, blank=True)
    #no2pga_option = models.CharField(max_length=3, null=True, blank=True)
    no2pga = models.CharField('2-phosphoglyceric acid (3PGA)',max_length=45, null=True, blank=True)
    #pep_option = models.CharField(max_length=3, null=True, blank=True)
    pep = models.CharField('Phosphornolpyruvate (PEP)',max_length=45, null=True, blank=True)
    #amp_option = models.CharField(max_length=3, null=True, blank=True)
    amp = models.CharField('Adenosinemonophosphosphate (AMP)',max_length=45, null=True, blank=True)
    #ab_option = models.CharField(max_length=3, null=True, blank=True)
    ab = models.CharField('Adenosine biphosphate (AB)',max_length=45, null=True, blank=True)
    #atp_option = models.CharField(max_length=3, null=True, blank=True)
    atp = models.CharField('Adenosnetriphosphate (ATP)',max_length=45, null=True, blank=True)
    #gssg_gsh_option = models.CharField(max_length=3, null=True, blank=True)
    gssg_gsp = models.CharField('Total glutathione (GSSG+GSH)',max_length=45, null=True, blank=True)
    #pyr_option = models.CharField(max_length=3, null=True, blank=True)
    pyr = models.CharField('Pyruvate (PYR)',max_length=45, null=True, blank=True)
    #lact_option = models.CharField(max_length=3, null=True, blank=True)
    lact = models.CharField('Lactate (LACT)',max_length=45, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)

class Redcell_membrane_dis(models.Model):
    patient =  models.ForeignKey(Demographic)
    yesno_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    plus_minus_option = (
        ('','Please select'),
        ('+','+'),
        ('-','-')
    )
    red_cell_morph_sm = models.CharField('Red cell morphology on peripheral blood smears',max_length=3, null=True, blank=True, choices=yesno_option, default=yesno_option[0][0])
    osm_fr_fresh_blood = models.CharField('On fresh blood', max_length=3, null=True, blank=True, choices=yesno_option, default=yesno_option[0][0])
    osm_fr_pre_incu_blood = models.CharField('On pre-incubated (37'+u'\u2103) blood',max_length=3, null=True, blank=True, choices=yesno_option, default=yesno_option[0][0])
    osm_fr_two_dif_nacl = models.CharField('Two different NaCl concentrations',max_length=3, null=True, blank=True)
    osm_fr_curve_str = models.CharField('Curve (no of different NaCl concentrations',max_length=45, null=True, blank=True)
    osm_fr_curve = models.CharField(max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0] )
    glt = models.CharField('Clycerol Lysis test (GLT)',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    aglt = models.CharField('Acidified Glycerol Lysis test (AGLT)',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    cryohemolysis_tst = models.CharField('Cryohemolysis tests',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    pink_tst = models.CharField('Pink test',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    flow_commercial_tst = models.CharField('Flow commercial tests',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    sds_page_rbc_proteins = models.CharField('SDS-PAGE of red blood cell membrane proteins',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    ektacytometer = models.CharField('Ektacytometer',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    lorrca = models.CharField('Laser-assisted Optical Rotational Cell Analyzer (LORRCA)',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    rbc_retic_auto_prm = models.CharField('RBC/Reticulocytes automated parameters (MCV, MCHC, IRF, ...)',max_length=3, null=True, blank=True,choices=yesno_option, default=yesno_option[0][0])
    molec_char_rna_dna_level = models.CharField('Molecular characterization at the DNA/RNA level',max_length=45, null=True, blank=True)
    method_best_sensi_speci = models.CharField('Method with best specificity and sensitivity in your experience',max_length=45, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)

class Cong_dyseryth_anaemia(models.Model):
    patient =  models.ForeignKey(Demographic)
    complt_blood_cnt = models.IntegerField('Complete blood count', null=True, blank=True)
    abs_reticulo_cnt = models.IntegerField('Absolute reticulocyte count', null=True, blank=True)
    soluble_transf_recept = models.IntegerField('Soluble transferring receptor', null=True, blank=True)
    bone_marrow_recept = models.IntegerField('Bone marrow receptor', null=True, blank=True)
    plus_minus_option = (
        ('','Please select'),
        ('Done','Done'),
        ('Not done','Not done')
    )
    sds_page = models.CharField('SDS-PAGE (sodium dodecyl sulphate - polyacrylamide gel electrophoresis)',max_length=15, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    moleculare_analysis = models.CharField('Performed',max_length=5, null=True, blank=True,choices=plus_minus_option, default=plus_minus_option[0][0])
    moleculare_analysis_comment = models.CharField('Comment',max_length=45, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)

    def __str__(self):
        return str(self.patient)


class Ext_centers(models.Model):
    center_id = models.AutoField(primary_key=True)
    center_loc_option = (
        ('','Please select'),
        ('National','National'),
        ('Regional','Regional'),
        ('Hospital','Hospital')
    )
    location_of_center = models.CharField('Locale',max_length=45, null=True, blank=True, choices=center_loc_option, default=center_loc_option[0][0])
    name_of_center = models.CharField('Name',max_length=45, null=True, blank=True)
    center_type_option = (
        ('','Please select'),
        ('Center for adults','Center for adults'),
        ('Center for children','Center for children'),
        ('Center manages all ages','Center manages all ages')
    )
    type_of_center = models.CharField('Type',max_length=45, null=True, blank=True, choices=center_type_option, default=center_type_option[0][0])
    center_address  = models.CharField('Address',max_length=45, null=True, blank=True)
    center_city  = models.CharField('City',max_length=45, null=True, blank=True)
    center_country  = models.CharField('Country',max_length=45, null=True, blank=True)
    center_name_of_medical_director  = models.CharField('Name of medical director',max_length=45, null=True, blank=True)
    center_name_of_respondent  = models.CharField('Name of respondent',max_length=45, null=True, blank=True)
    center_status_of_respondent  = models.CharField('Status of respondent',max_length=45, null=True, blank=True)
    center_telephone = models.IntegerField('Telephone', null=True,blank=True)
    center_email = models.EmailField('E-mail',null=True,blank=True)
    center_fax = models.IntegerField('Fax',null=True,blank=True)
    center_website = models.CharField('Website',max_length=45, null=True, blank=True)


    diagn_categ_b_thal_major_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_b_thal_major_distribution = models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_non_transfusion_dep_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_non_transfusion_dep_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_hbh_disease_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_hbh_disease_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_sickle_ss_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_sickle_ss_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_sickle_sc_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_sickle_sc_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_scd_s_b_thal_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_scd_s_b_thal_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_other_scd_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_other_scd_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_hered_sphero_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_hered_sphero_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_hered_ellipto_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_hered_ellipto_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pyropoikilc_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pyropoikilc_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_stomatoc_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_stomatoc_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_south_asian_oval_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_south_asian_oval_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_cda_type_i_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_cda_type_i_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_cda_type_ii_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_cda_type_ii_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_cda_type_iii_no_patient = models.IntegerField('No of patients',null=True,blank=True)
    diagn_categ_cda_type_iii_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_g6pd_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_g6pd_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pyruvate_k_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pyruvate_k_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_hexokinase_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_hexokinase_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gpi_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gpi_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pfk_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pfk_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pgk_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pgk_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_tpi_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_tpi_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_ldh_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_ldh_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_aldolase_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_aldolase_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_enolase_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_enolase_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_bpgm_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_bpgm_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_mpgm_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_mpgm_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pgm_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pgm_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_6pgd_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_6pgd_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gcs_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gcs_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gsh_s_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gsh_s_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gr_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gr_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gsh_px_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gsh_px_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_gst_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_gst_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_ak_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_ak_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_p5_nuc_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_p5_nuc_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_nadh_dia_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_nadh_dia_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_nadph_dia_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_nadph_dia_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_sod_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_sod_def_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_catalas_def_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_catalas_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_diamond_blackfan_anae_no_patient = models.IntegerField('No of patients',null=True,blank=True)
    diagn_categ_diamond_blackfan_anae_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_fanconi_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_fanconi_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_here_congenit_side_anaemia_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_here_congenit_side_anaemia_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_aceruloplasm_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_aceruloplasm_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_atransfer_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_atransfer_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_dmt1_def_no_patient = models.IntegerField('No of patients',null=True,blank=True)
    diagn_categ_dmt1_def_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_irida_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_irida_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    diagn_categ_pnh_no_patient = models.IntegerField('No of patients', null=True,blank=True)
    diagn_categ_pnh_distribution= models.CharField('Age distribution',max_length=45, null=True, blank=True)

    outcomes_year2010_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2010_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2010_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    outcomes_year2011_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2011_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2011_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    outcomes_year2012_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2012_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2012_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    outcomes_year2013_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2013_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2013_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    outcomes_year2014_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2014_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2014_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    outcomes_year2015_thal = models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    outcomes_year2015_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    outcomes_year2015_rare= models.IntegerField('Rare anaemias', null=True,blank=True)

    anaemia_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    anaemia_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    anaemia_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    cardiac_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    cardiac_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    cardiac_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    infection_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    infection_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    infection_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    hepatic_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    hepatic_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    hepatic_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    malignancy_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    malignancy_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    malignancy_rare= models.IntegerField('Rare anaemias', null=True,blank=True)
    other_thal= models.IntegerField('Thalassaemia syndromes', null=True,blank=True)
    other_sickle= models.IntegerField('Sickle cell syndromes', null=True,blank=True)
    other_rare= models.IntegerField('Rare anaemias', null=True,blank=True)

    out_patients_married= models.IntegerField('Married patients', null=True,blank=True)
    out_patients_divorced= models.IntegerField('Divorced patients', null=True,blank=True)
    out_patients_single= models.IntegerField('Single patients', null=True,blank=True)
    out_patients_cohabiting= models.IntegerField('Cohabiting patients', null=True,blank=True)
    out_patients_parented_children = models.IntegerField('Patient have parented children', null=True,blank=True)
    out_thal_women_preg = models.IntegerField('Thalassaemic women have had pregnancies', null=True,blank=True)
    out_patients_splene= models.IntegerField('Splenectomised patients', null=True,blank=True)

    choleitithiasis_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    choleitithiasis_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    choleitithiasis_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    choleitithiasis_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5, max_length=5, null=True,blank=True)
    heart_f_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    heart_f_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    heart_f_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    heart_f_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    arryth_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    arryth_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    arryth_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    arryth_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    pulm_hyp_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    pulm_hyp_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    pulm_hyp_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    pulm_hyp_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    gluc_int_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    gluc_int_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    gluc_int_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    gluc_int_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    diab_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    diab_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    diab_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    diab_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypogon_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hypogon_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hypogon_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypogon_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypothyr_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hypothyr_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hypothyr_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypothyr_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypoparath_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hypoparath_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hypoparath_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypoparath_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    liver_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    liver_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    liver_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    liver_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hcv_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hcv_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hcv_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hcv_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypatoc_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hypatoc_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hypatoc_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hypatoc_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    other_mal_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    other_mal_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    other_mal_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    other_mal_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    osteopor_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    osteopor_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    osteopor_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    osteopor_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    osteomye_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    osteomye_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    osteomye_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    osteomye_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    thrombo_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    thrombo_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    thrombo_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    thrombo_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    dact_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    dact_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    dact_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    dact_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    splenic_seq_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    splenic_seq_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    splenic_seq_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    splenic_seq_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    liver_seq_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    liver_seq_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    liver_seq_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    liver_seq_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    mes_synd_hb= models.IntegerField('No Hb disorders',null=True,blank=True)
    mes_synd_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    mes_synd_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    mes_synd_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    aplas_cris_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    aplas_cris_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    aplas_cris_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    aplas_cris_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hyperhae_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    hyperhae_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    hyperhae_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    hyperhae_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    stroke_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    stroke_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    stroke_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    stroke_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    sil_inf_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    sil_inf_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    sil_inf_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    sil_inf_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    ac_chest_synd_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    ac_chest_synd_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    ac_chest_synd_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    ac_chest_synd_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    priap_hb= models.IntegerField('No Hb disorders',null=True,blank=True)
    priap_ra= models.IntegerField('No RAs disorders',null=True,blank=True)
    priap_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    priap_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    ava_nec_fem_hd_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    ava_nec_fem_hd_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    ava_nec_fem_hd_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    ava_nec_fem_hd_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    retin_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    retin_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    retin_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    retin_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    kid_dis_hb= models.IntegerField('No Hb disorders', null=True,blank=True)
    kid_dis_ra= models.IntegerField('No RAs disorders', null=True,blank=True)
    kid_dis_per_hb= models.DecimalField('Percentage of total Hb disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    kid_dis_per_ra= models.DecimalField('Percentage of total RAs disorders',decimal_places=2, max_digits=5,max_length=5, null=True,blank=True)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    author = models.ForeignKey(User)


    def __str__(self):
        return self.name_of_center