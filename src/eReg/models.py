# -*- coding: utf-8 -*-

from django.db import models
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin import widgets
from django.utils.encoding import smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta
# Create Demographic models here



class Demographic(models.Model):
    anonymisation_code = models.IntegerField('Anonymisation code', null=True,blank=True)
    patient_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    patient_consent_for_data_storage= models.CharField('Data Storage', max_length=3,choices=patient_option, default=patient_option[0][0])
    patient_consent_for_data_reusage= models.CharField('Data Reuse',max_length=3,choices=patient_option, default=patient_option[0][0])
    creation_of_consent_form = models.DateField('Creation date')
    data_provider = (
        ('','Please select'),
        ('Provider','Provider'),
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
    race = models.CharField(max_length=30,null=True,blank=True)
    blood_group_option = (
        ('','Please select'),
        ('O-','O-'),
        ('O+','O+'),
        ('A-','A-'),
        ('A+','A+'),
        ('B-','B-'),
        ('B+','B+'),
        ('AB-','AB-'),
        ('AB+','AB+'),
    )
    blood_group= models.CharField(max_length=6,null=True,blank=True, choices=blood_group_option, default=blood_group_option[0][0])
    family = models.CharField('Family name',max_length=15,null=True,blank=True)
    address_street = models.CharField('Street',max_length=25,null=True,blank=True)
    address_no = models.IntegerField('Number',null=True,blank=True)
    address_city = models.CharField('City',max_length=25,null=True,blank=True)
    address_post_code = models.IntegerField('Post code',null=True,blank=True)
    address_state = models.CharField('State',max_length=25,null=True,blank=True)
    address_country = models.CharField('Country',max_length=25,null=True,blank=True)
    telephone = models.IntegerField(null=True,blank=True)
    email = models.EmailField('E-mail',null=True,blank=True)
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
        ('No','No'),
        ('Yes','Yes'),
        ('Full time','Full time'),
        ('Part time', 'Part time')
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
    paternity = models.CharField('Paternity', max_length=3, null=True,blank=True, choices=data_option, default=data_option[0][0])
    no_of_children = models.IntegerField('Number of children',null=True,blank=True)
    #year of birth of each child
    maternity = models.CharField('Maternity', max_length=3, null=True,blank=True, choices=data_option, default=data_option[0][0])


    def __str__(self):
        return str(self.patient_id)

class icd_10(models.Model):
    id = models.IntegerField(unique=True,primary_key=True,null=False,blank=False)
    icd_10_desc = models.CharField('ICD-10 description',max_length=80,null=True,blank=True)
    icd_10_code = models.CharField('ICD-10 code',max_length=10,null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.icd_10_desc)

class Pregnancy(models.Model):
    patient = models.ForeignKey(Demographic)
    #pregnancy_id = models.AutoField(unique=True ,primary_key=True)
    year = models.DateField('Pregnancy year',null=True,blank=True)
    outcome_birth = models.CharField('Outcome birth',max_length=100,null=True,blank=True)
    other = models.CharField('Other',max_length=50, null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)

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
    diagnosis_genotype = models.CharField('Diagnosis genotype', max_length=100, null=True, blank=True)
    diagnosis_circumstances_value = (
        ('','Please select Diagnosis circumstances'),
        ('Antenatal diagnosis','Antenatal diagnosis'),
        ('Neonatal diagnosis','Neonatal diagnosis'),
        ('By the presence of affected related','By the presence of affected related'),
        ('Clinical diagnosis', 'Clinical diagnosis'),
        ('Other','Other')

    )
    diagnosis_circumstances = models.CharField(max_length=45, choices = diagnosis_circumstances_value, default=diagnosis_circumstances_value[0][0])
    diagnosis_circumstances_date = models.DateField('Date of diagnosis',null=True,blank=True)
    date_of_input= models.DateField(null=True,blank=True)
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
    clinical_data_weight = models.IntegerField('Weight (kg)', null=True,blank=True)
    clinical_data_height = models.IntegerField('Height (cm)', null=True,blank=True)
    clinical_data_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    clinical_data_cholelithiasis = models.CharField('Cholelithiasis', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_cholelithiasis_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_cholecystectomy = models.CharField('Cholecystectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_cholecystectomy_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_splenectomy = models.CharField('Splenectomy', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_splenectomy_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_iron_overload_heart = models.CharField('Iron overload heart', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_iron_overload_heart_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_heart_failure = models.CharField('Heart failure', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_heart_failure_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_cardiac_arrythmia = models.CharField('And/or cardiac arrythmia', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_cardiac_arrythmia_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_glucose_intolerance = models.CharField('Glucose intolerance', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_glucose_intolerance_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_diabetes = models.CharField('Diabetes', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_diabetes_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_hypothyroidism = models.CharField('Hypothyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_hypothyroidism_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_hypoparathyroidism = models.CharField('Hypoparathyroidism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_hypoparathyroidism_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_hypogonadism = models.CharField('Hypogonadism', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_hypogonadism_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_iron_overload_liver = models.CharField('Iron overload liver', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_iron_overload_liver_date = models.DateField('Date of occurrence',null=True,blank=True)
    clinical_data_others = models.CharField('Others (Thromboembolism, cancers,...)', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    clinical_data_others_date = models.DateField('Date of occurrence',null=True,blank=True)
    #clinical_data_pregnancy_id = models.ForeignKey(Pregnancy)
    assessment_of_iron_load_serrum_one= models.CharField('Measurement 1', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_one_date= models.DateField('Date of occurrence',null=True,blank=True)
    assessment_of_iron_load_serrum_two= models.CharField('Measurement 2', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_two_date= models.DateField('Date of occurrence',null=True,blank=True)
    assessment_of_iron_load_serrum_three= models.CharField('Measurement 3', max_length=10,null=True,blank=True)
    assessment_of_iron_load_serrum_three_date= models.DateField('Date of occurrence',null=True,blank=True)
    assessment_of_iron_load_liver_mri= models.CharField('Liver MRI', max_length=10,null=True,blank=True)
    assessment_of_iron_load_liver_mri_date= models.DateField('Date of occurrence',null=True,blank=True)
    assessment_of_iron_load_fibroscan= models.CharField('Fibroscan', max_length=10,null=True,blank=True)
    assessment_of_iron_load_fibroscan_date= models.DateField('Date of occurrence',null=True,blank=True)
    assessment_of_iron_load_intra_hepatic_iron= models.CharField('Intra hepatic iron', max_length=10,null=True,blank=True)
    assessment_of_iron_load_method_mri= models.CharField('MRI', max_length=10,null=True,blank=True)
    assessment_of_iron_load_method_cardiac_iron= models.CharField('Cardiac iron/IRM', max_length=10,null=True,blank=True)
    assessment_of_iron_load_ti_bassal_hb_rate= models.CharField('Bassal Hb rate', max_length=10,null=True,blank=True)
    assessment_of_iron_load_ti_bassal_per_hbf= models.CharField('Bassal % HbF rate', max_length=10,null=True,blank=True)
    serological_data_option = (
        ('','Please select'),
        ('+','+'),
        ('-','-'),
        ('not done', 'not done')
    )
    serolocigal_data_HCV = models.CharField('HCV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HCV_PCR = models.CharField('HCV PCR', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HBV = models.CharField('HBV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    serolocigal_data_HIV = models.CharField('HIV', max_length=10,null=True,blank=True, choices=serological_data_option, default=serological_data_option[0][0])
    current_treatment_transfusion_regime_option= (
        ('', 'Please select'),
        ('8 transfusions per year or more','8 transfusions per year or more' ),
        ('Occational','Occational'),
        ('Absent','Absent')
    )
    current_treatment_transfusion_regime = models.CharField('Transfusion regime', max_length=30,null=True,blank=True, choices=current_treatment_transfusion_regime_option, default=current_treatment_transfusion_regime_option[0][0])
    current_treatment_chelation =  models.CharField('Chelation', max_length=3,choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_chelation_start=models.DateField('Start of chelation therapy (year only)',null=True,blank=True)
    current_treatment_chelation_drug= models.CharField('Current Chelator drug',max_length=15, null=True, blank=True)
    current_treatment_bone_marrow =  models.CharField('Bone-marrow treatment',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_bone_marrow_date = models.DateField('Date of occurrence',null=True,blank=True)
    current_treatment_bone_marrow_success =  models.CharField('Success',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_replacement_ther =  models.CharField('Replacement therapy: by thyroid stimulating Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_sex_horm =  models.CharField('By sexual Hormones',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_insulin =  models.CharField('By insulin',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_thyroid =  models.CharField('For parathyroid deficiency',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_hepatitis_option= (
        ('', 'Please select'),
        ('No','No' ),
        ('Current treatment','Current treatment'),
        ('Treatment in the past','Treatment in the past')
    )
    current_treatment_hepatitis_treatment_c =  models.CharField('Hepatitis treatment',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    current_treatment_hepatitis_treatment_b =  models.CharField('Hepatitis treatment',max_length=15, null=True, blank=True, choices=current_treatment_hepatitis_option, default=current_treatment_hepatitis_option[0][0])
    current_treatment_by_hydroxyurea = models.CharField('Treatment by Hydroxyurea',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    current_treatment_by_hydroxyurea_with_epo = models.CharField('With EPO',max_length=15, null=True, blank=True, choices=clinical_data_option, default=clinical_data_option[0][0])
    date_of_input= models.DateField(null=True,blank=True)

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
    cbc = models.CharField('CBC', max_length=3, choices =thal_option, null=True, blank=True)
    hb = models.CharField('Hb',max_length=3, choices =thal_option,null=True, blank=True)
    mcv = models.CharField('MCV (fl)',max_length=3, null=True, blank=True)
    mch = models.CharField('MCH (pg)',max_length=3, null=True, blank=True)
    hba2  = models.CharField('HbA<sub>2</sub>',max_length=3, choices =thal_option,null=True, blank=True)
    hbf  = models.CharField('HbF', max_length=3, choices =thal_option,null=True, blank=True)
    haemoglobin = models.CharField('Haemoglobin (g/dl)',max_length=3, choices =thal_option,null=True, blank=True)
    nrbc  = models.CharField('NRBC/100 WBC', max_length=3, null=True, blank=True)
    reticulocytes = models.CharField('Reticulocytes (%)', max_length=3, null=True, blank=True)
    red_cell_morphology  = models.CharField('Red cell morphology', max_length=20, null=True, blank=True)
    rare_anaemia  = models.CharField('Rare anaemia', max_length=25, null=True, blank=True)
    cell_acetate_electr  = models.CharField('Celluloce acetate electrophoresis, pH 8.6',max_length=3, choices =thal_option,null=True, blank=True)
    acid_agarose_citrate  = models.CharField('Acid Agarose or citrate agar pH 6.0',max_length=3, choices =thal_option,null=True, blank=True)
    isoelect_foc  = models.CharField('Isoelectric focusing', max_length=3, choices =thal_option,null=True, blank=True)
    hlpc_cap_elect = models.CharField('HPLC or Capillary Electrophoresis',max_length=3, choices =thal_option,null=True, blank=True)
    quant_hba2  = models.CharField('Quantization of HbA<sub>2</sub>', max_length=3, null=True, blank=True)
    quant_hbh  = models.CharField('Quantization of HbH',max_length=3, null=True, blank=True)
    quant_hbf  = models.CharField('Quantization of HbF',max_length=3, null=True, blank=True)
    quant_other_var  = models.CharField('Quantization of other variant',max_length=3, null=True, blank=True)
    conf_pres_hbs  = models.CharField('Confirm the presence of an HbS by sickling test or a solubility test',max_length=3, null=True, blank=True)
    conf_pres_hbe  = models.CharField('Confirm the presence of an HbE by the DCIP test',max_length=3, null=True, blank=True)
    conf_pres_un_haemo_isoprop_option  = models.CharField('Isopropanol test',choices=plus_minus_option,max_length=3, null=True, blank=True)
    conf_pres_un_haemo_isoprop  = models.CharField('Comment',max_length=25, null=True, blank=True)
    conf_pres_un_haemo_heat_option = models.CharField('Heat test', max_length=3, null=True, blank=True)
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

    def __str__(self):
        return str(self.patient)


class Redcell_enzyme_dis (models.Model):
    patient = models.ForeignKey(Demographic)
    plus_minus_option = (
        ('','Please select'),
        ('+','+'),
        ('-','-')
    )
    #enzymes_of_glycol_option = models.CharField('Enzymes of glycolysis',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    #enzymes_of_glycol = models.CharField(max_length=45, null=True, blank=True)
    hk_option = models.CharField('Hexokinase (HK)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    hk = models.CharField(max_length=45, null=True, blank=True)
    gpi_option = models.CharField('Glucosephosphate isomerase (GPI)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gpi = models.CharField(max_length=45, null=True, blank=True)
    pfk_option = models.CharField('Phosphofructokinase (PFK)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pfk = models.CharField(max_length=45, null=True, blank=True)
    g3ph_option = models.CharField('Glyceraldehyde-3-phosphate dehydrogenase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    g3ph = models.CharField(max_length=45, null=True, blank=True)
    pgk_option = models.CharField('Phosphoglycerate kinase (PGK)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pgk = models.CharField(max_length=45, null=True, blank=True)
    pk_option = models.CharField('Pyruvate kinase (PK)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pk_v = models.CharField(max_length=45, null=True, blank=True)
    tpi_option = models.CharField('Triosephorate isomerase (TPI)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    tpi = models.CharField(max_length=45, null=True, blank=True)
    ldh_option = models.CharField('Lactate dehydrogenase (LDH)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    ldh = models.CharField(max_length=45, null=True, blank=True)
    adolase_option = models.CharField('Aldolase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    adolase = models.CharField(max_length=45, null=True, blank=True)
    enolase_option = models.CharField('Enolase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    enolase = models.CharField(max_length=45, null=True, blank=True)
    bpgm_option = models.CharField('Biphosphoglycerate mutase (BPGM)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    bpgm = models.CharField(max_length=45, null=True, blank=True)
    mpgm_option = models.CharField('Monophosphoglycerate mutase (MPGM)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    mpgm = models.CharField(max_length=45, null=True, blank=True)
    pgm_option = models.CharField('Phosphocluconate mutase (PGM)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pgm = models.CharField(max_length=45, null=True, blank=True)
    #enz_hexose_option = models.CharField('Enzymes of hexose-monophosphate shunt and glutathione metabolism',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    #enz_hexose = models.CharField(max_length=45, null=True, blank=True)
    cerumen_option = models.CharField('Cerumen',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    cerumen = models.CharField(max_length=45, null=True, blank=True)
    g6pd_option = models.CharField('Glucose-6-phosphate dehydrogenase (G6PD)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    g6pd = models.CharField(max_length=45, null=True, blank=True)
    no6pgd_option = models.CharField('6-phosphogluconate dehydrogenase (6-PGD)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    no6pgd = models.CharField(max_length=45, null=True, blank=True)
    gcs_option = models.CharField('Gamma-glutamylcysteine synthetase (GCS)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gcs = models.CharField(max_length=45, null=True, blank=True)
    gshs_option = models.CharField('Glutathione synthetase (GSH-S)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gshs = models.CharField(max_length=45, null=True, blank=True)
    gr_option = models.CharField('Glutathione reductase (GR)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gr = models.CharField(max_length=45, null=True, blank=True)
    gshpx_option = models.CharField('Glutathione peroxidase (GSH-Px)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gshpx = models.CharField(max_length=45, null=True, blank=True)
    gst_option = models.CharField('Glutathione s-transferase (GST)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    gst = models.CharField(max_length=45, null=True, blank=True)
    #enz_nuc_meta_option = models.CharField(max_length=3, null=True, blank=True)
    #enz_nuc_meta = models.CharField(max_length=45, null=True, blank=True)
    ak_option = models.CharField('Adenylate kinase (AK)',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    ak = models.CharField(max_length=45, null=True, blank=True)
    pyr5nuc_option = models.CharField('Pyrimidine-5'' nucleotidase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pyr5nuc = models.CharField(max_length=45, null=True, blank=True)
    pur_pyr_ratio_option = models.CharField('Purine/pyrimidine nucleotides ratio',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    pur_pur_ratio = models.CharField(max_length=45, null=True, blank=True)
    #other_rbce_act_option = models.CharField(max_length=3, null=True, blank=True)
    #other_rbce_act = models.CharField(max_length=45, null=True, blank=True)
    nadh_dia_option = models.CharField('NADH diaphorase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    nadh_dia = models.CharField(max_length=45, null=True, blank=True)
    nadph_dia_option = models.CharField('NADPH diaphorase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    nadph_dia_act = models.CharField(max_length=45, null=True, blank=True)
    sod_option = models.CharField('Superoxide dismutase',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    sod_act = models.CharField(max_length=45, null=True, blank=True)
    catalase_option = models.CharField('Catalase', max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    catalase = models.CharField(max_length=45, null=True, blank=True)
    other_option = models.CharField('Other',max_length=3, null=True, blank=True, choices=plus_minus_option, default=plus_minus_option[0][0])
    other = models.CharField(max_length=45, null=True, blank=True)
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

    def __str__(self):
        return str(self.patient)

class Cong_dyseryth_anaemia(models.Model):
    patient =  models.ForeignKey(Demographic)
    complt_blood_cnt = models.CharField('Complete blood count',max_length=45, null=True, blank=True)
    abs_reticulo_cnt = models.CharField('Absolute reticulocyte count',max_length=45, null=True, blank=True)
    soluble_transf_recept = models.CharField('Soluble transferring receptor',max_length=45, null=True, blank=True)
    bone_marrow_recept = models.CharField('Bone marrow receptor',max_length=45, null=True, blank=True)
    sds_page = models.CharField('SDS-PAGE (sodium dodecyl sulphate - polyacrylamide gel electrophoresis)',max_length=45, null=True, blank=True)
    moleculare_analysis = models.CharField('Molecular analysis',max_length=45, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.patient)


class Outcome_measures(models.Model):
    patient =  models.ForeignKey(Demographic)
    mortality_date_of_death = models.DateField('Date of death',null=True,blank=True)
    mortality_cause_of_death = models.CharField('Cause of death',max_length=100, null=True, blank=True)
    age_of_first_transfusion = models.IntegerField(null=True,blank=True)
    yesno_option = (
        ('','Please select'),
        ('Yes','Yes'),
        ('No','No')
    )
    transfusion_depentent_anaemia= models.CharField('Transfusion dependent anaemia',max_length=100, null=True, blank=True, choices=yesno_option, default=yesno_option[0][0])
    date_of_transition_from_irregular_to_regular_tranfusions= models.DateField(null=True,blank=True)
    splenomegaly= models.CharField(max_length=30, null=True, blank=True)
    t2_of_heart = models.CharField('Annual result of T2* of heart',max_length=30, null=True, blank=True)
    r2_of_heart = models.CharField('Annual result R2 of liver',max_length=30, null=True, blank=True)
    pre_transfusion_hb_level_mid_year = models.CharField('Pre-transfusion Hb level',max_length=30, null=True, blank=True)
    pre_transfusion_hb_level_end_of_year = models.CharField('Pre-transfusion Hb level',max_length=30, null=True, blank=True)
    serum_ferritin = models.CharField('Annual serum ferritin',max_length=30, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.patient)


class Life_events(models.Model):
    patient = models.ForeignKey(Demographic)
    HSCT_date = models.DateField('Date',null=True,blank=True)
    HSCT_outcome = models.CharField('Outcome',max_length=100, null=True, blank=True)
    partaker_in_clinical_trial= models.CharField('Partaker in clinical trial',max_length=200, null=True, blank=True)
    date_of_input= models.DateField(null=True,blank=True)

    def __str__(self):
        return str(self.patient)