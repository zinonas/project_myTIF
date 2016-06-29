from __future__ import division
from django.db.models import Sum, Count
from django.contrib.auth.models import Group
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, get_object_or_404, redirect
import django.http
from .forms import DemographicForm, DiagnosisForm, A_b_sickle_thalForm, Redcell_enzyme_disForm, Redcell_membrane_disForm,Cong_dyseryth_anaemiaForm, UserCreationForm, ClinicalDataForm, ClinicalDataTwo, ExternalCentersForm,ExternalCentersDiagnosticForm,ExternalCentersOutcomesForm, ExternalCentersOutcomes2Form,Patient_Reported_outcomeForm
from django.template import RequestContext
from collections import OrderedDict
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
import json
from django.contrib import messages
import traceback
from django.forms.models import formset_factory
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from models import Demographic, Diagnosis, A_b_sickle_thal,Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, orphaCodes, Clinical_data, Clinical_data_two, Ext_centers,Patient_reported_outcome, DiagnosisOption, Institution
from django.core import serializers
import json
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import unicodedata
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import auth
from django.contrib.auth import logout
from dal import autocomplete
from django.core.cache import cache
from datetime import date
from django.utils import formats
import collections
from chartit import PivotDataPool, PivotChart
import ast
from django.db.models import Q
import collections
from itertools import chain
from collections import Counter



def password_change_done(request, template_name="registration/password_change_done.html"):
    return render_to_response(template_name,(),context_instance= RequestContext(request))

def about(request):
    return render(request,'index.html')

@login_required(login_url='/login')
def home(request):
    groups = Group.objects.all()

    return render(request,'index.html', {'groups':groups},context_instance= RequestContext(request))

@login_required(login_url='/login')
def modules(request):
    #groups = Group.objects.all()

    if request.method == 'POST':
        response = redirect('input')
        mod2=request.POST.get('module_id_2', False)
        if mod2 != False:
            #print mod2
            response.set_cookie('module_2', '2')
        else:
            response.delete_cookie('module_2')

        mod3=request.POST.get('module_id_3', False)
        if mod3 != False:
            #print mod3
            response.set_cookie('module_3', '3')
        else:
            response.delete_cookie('module_3')

        mod4=request.POST.get('module_id_4', False)
        if mod4 != False:
            #print mod4
            response.set_cookie('module_4', '4')
        else:
            response.delete_cookie('module_4')

        mod5=request.POST.get('module_id_5', False)
        if mod5 != False:
            #print mod5
            response.set_cookie('module_5', '5')
        else:
            response.delete_cookie('module_5')

        mod6=request.POST.get('module_id_6', False)
        if mod6 != False:
            #print mod5
            response.set_cookie('module_6', '6')
        else:
            response.delete_cookie('module_6')


        return response



    return render(request,'module_selection.html',context_instance= RequestContext(request))

@login_required(login_url='/login')

def input(request):

    context = RequestContext(request)
    print context
    ret = cache.get('input-rendered')

    #diagnosis option for saving purposes. In order to save only specific tables in db.
    diag_option = 0

    if request.method == 'POST':

        my_demographics = DemographicForm(request.POST, prefix="demo")
        my_diagnosis = DiagnosisForm(request.POST, prefix='diag')
        my_a_b_sickle= A_b_sickle_thalForm(request.POST,prefix='a_b_s')
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST, prefix='rc_enz')
        my_redcell_membrane= Redcell_membrane_disForm(request.POST, prefix='rc_mbr')
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST, prefix='cong_dys')
        my_cln_dt = ClinicalDataForm(request.POST, prefix='cln_dt')
        my_cln_dt_two = ClinicalDataTwo(request.POST, prefix='cln_dt_two')
        my_patient_reported_outcomes = Patient_Reported_outcomeForm(request.POST, prefix='ptn_rep_out')



        # if (my_demographics.is_valid() and my_diagnosis.is_valid()):
        #     print "dem and diag validation"
        #     my_demographics_object = my_demographics.save(commit=False)
        #     my_demographics_object.author = request.user
        #     my_demographics_object.save()
        #     #my_diagnosis = DiagnosisForm(request.POST, prefix='diag', initial={'patient':my_demographics_object.patient_id} )
        #
        #     print "my dem id"
        #     print my_demographics_object.patient_id
        #
        #     my_diagnosis_object=my_diagnosis.save(commit=False)
        #     my_diagnosis_object.patient = my_demographics_object
        #     my_diagnosis_object.author = request.user
        #     my_diagnosis_object.save()


        print "POST"


        print "my demographics"
        print my_demographics.errors
        print "my diagnosis"
        print my_diagnosis.errors
        print "a_b_sickle"
        print my_a_b_sickle.errors
        print my_redcell_membrane.errors
        print my_redcell_enzyme.errors
        print my_cong_dys.errors
        print my_cln_dt.errors
        print my_cln_dt_two.errors
        print my_patient_reported_outcomes.errors

        print my_demographics.is_valid()
        print my_diagnosis.is_valid()
        print my_a_b_sickle.is_valid()
        print my_redcell_enzyme.is_valid()
        print my_redcell_membrane.is_valid()
        print my_cong_dys.is_valid()
        print my_cln_dt.is_valid()
        print my_cln_dt_two.is_valid()
        print my_patient_reported_outcomes.is_valid

        if request.is_ajax() and 'code' in request.POST:
            with transaction.atomic():
                code = request.POST['code']
                print 'code =', code
                data = icd_10.objects.get(id=code).icd_10_code
                print 'data =', data
                return HttpResponse(data)

        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_a_b_sickle.is_valid and my_redcell_enzyme.is_valid() and my_redcell_membrane.is_valid() and my_cong_dys.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid() and my_patient_reported_outcomes.is_valid():

            entry = '"{Demographic":['
            for formfield in my_demographics:
                #print formfield.field.__class__.__name__
                de_id= formfield.name
                #print de_id
                entry+='{"fieldName":"'+ str(de_id) + '",'
                de_val= formfield.value()
                #print type(de_val)
                entry+='"fieldValue":"'+str(de_val) + '"},'
            entry = entry[:-1]


            entry +='],"Diagnosis":['
            #print entry

            for formfield in my_diagnosis:
                dia_id = formfield.name
                if formfield.name == 'diagnosis_option':
                    dig_opt_list =  formfield.value()
                if formfield.name == 'icd_10_desc':
                    icd_10_opt_list =  formfield.value()
                if formfield.name == 'orpha_code':
                    orpha_opt_list =  formfield.value()
                #print formfield.id_for_label
                entry+='{"fieldName":"'+ str(dia_id) + '",'
                print "HERE I HAVE dia_val=", formfield.value()
                print formfield.name
                dia_val= str(formfield.value())
                if (dia_val == 'b-thalassaemia syndromes' or dia_val=='a-thalassaemia syndromes' or dia_val=='Sickle cell syndromes' or dia_val=='Other haemoglobin variants'):
                    diag_option = 1
                elif (dia_val == 'Rare cell enzyme disorders'):
                    diag_option = 2
                elif (dia_val == 'Rare cell membrane disorders'):
                    diag_option = 3
                elif (dia_val == 'Congenital desyrythropoietic anaemias'):
                    diag_option = 4
                elif(('b-thalassaemia syndromes' in dia_val or 'a-thalassaemia syndromes' in dia_val or 'Sickle cell syndromes' in dia_val or 'Other haemoglobin variants' in dia_val) and 'Rare cell enzyme disorders' in dia_val):
                    diag_option = 12
                elif(('b-thalassaemia syndromes' in dia_val or 'a-thalassaemia syndromes' in dia_val or 'Sickle cell syndromes' in dia_val or 'Other haemoglobin variants' in dia_val) and 'Rare cell membrane disorders' in dia_val):
                    diag_option = 13
                elif(('b-thalassaemia syndromes' in dia_val or 'a-thalassaemia syndromes' in dia_val or 'Sickle cell syndromes' in dia_val or 'Other haemoglobin variants' in dia_val) and 'Congenital desyrythropoietic anaemias' in dia_val):
                    diag_option = 14
                elif('Rare cell enzyme disorders' in dia_val and 'Rare cell membrane disorders' in dia_val):
                    diag_option = 23
                elif('Rare cell enzyme disorders' in dia_val and 'Congenital desyrythropoietic anaemias' in dia_val):
                    diag_option = 24
                elif('Rare cell membrane disorders' in dia_val and 'Congenital desyrythropoietic anaemias' in dia_val):
                    diag_option = 34
                #print type(de_val)
                entry+='"fieldValue":"'+str(dia_val) + '"},'
            entry = entry[:-1]
            #entry +='],'
            #print entry
            print "diagnosis option=", diag_option
            #
            # if (diag_option == 1):
            #     entry +='],"A_b_sickle_thal":['
            #     for formfield in my_a_b_sickle:
            #         #print formfield.field.__class__.__name__
            #         abs_id= formfield.name
            #         #print de_id
            #         entry+='{"fieldName":"'+ str(abs_id) + '",'
            #         abs_val= formfield.value()
            #         #print type(de_val)
            #         entry+='"fieldValue":"'+str(abs_val) + '"},'
            #     entry = entry[:-1]
            #     entry +=']}'
            #
            # elif (diag_option == 2):
            #     entry +='],"Rare cell enzyme disorders":['
            #     for formfield in my_redcell_enzyme:
            #         #print formfield.field.__class__.__name__
            #         rce_id= formfield.name
            #         #print de_id
            #         entry+='{"fieldName":"'+ str(rce_id) + '",'
            #         rce_val= formfield.value()
            #         #print type(de_val)
            #         entry+='"fieldValue":"'+str(rce_val) + '"},'
            #     entry = entry[:-1]
            #     entry +=']}'
            #
            # elif (diag_option == 3):
            #     entry +='],"Rare cell membrane disorders":['
            #     for formfield in my_redcell_membrane:
            #         #print formfield.field.__class__.__name__
            #         rcm_id= formfield.name
            #         #print de_id
            #         entry+='{"fieldName":"'+ str(rcm_id) + '",'
            #         rcm_val= formfield.value()
            #         #print type(de_val)
            #         entry+='"fieldValue":"'+str(rcm_val) + '"},'
            #     entry = entry[:-1]
            #     entry +=']}'
            #
            # elif (diag_option == 4):
            #     entry +='],"Congenital desyrythropoietic anaemias":['
            #     for formfield in my_cong_dys:
            #         #print formfield.field.__class__.__name__
            #         cong_dys_id= formfield.name
            #         #print de_id
            #         entry+='{"fieldName":"'+ str(cong_dys_id) + '",'
            #         cong_dys_val= formfield.value()
            #         #print type(de_val)
            #         entry+='"fieldValue":"'+str(cong_dys_val) + '"},'
            #     entry = entry[:-1]
            #     entry +=']}'
            #
            # s= json.dumps(entry)
            # print s





            #my_demographics_object = my_demographics.save()
            my_demographics_object = my_demographics.save(commit=False)
            my_demographics_object.author = request.user
            surname = my_demographics_object.surname
            initial_letter = "".join(item[0].upper() for item in surname.split())
            count_initial_letter = Demographic.objects.filter(surname__startswith=initial_letter)
            length_count_initial_letter = len(count_initial_letter)
            new_anonymization = initial_letter + str(length_count_initial_letter+1)
            my_demographics_object.anonymisation_code = new_anonymization

            my_demographics_object.save()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.author = request.user
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()

            for x in xrange(0, len(dig_opt_list)):
                my_diagnosis_object.diagnosis_option.add(dig_opt_list[x])

            for x in xrange(0, len(icd_10_opt_list)):
                my_diagnosis_object.icd_10_desc.add(icd_10_opt_list[x])
                #print "icd"
                #print icd_10_opt_list[x]

            for x in xrange(0, len(orpha_opt_list)):
                my_diagnosis_object.orpha_code.add(orpha_opt_list[x])
                #print "orpha"
                #print orpha_opt_list[x]




            #my_diagnosis_object.set_all()


            #my_diagnosis_object.diagnosis_options.add(id=my_diagnosis_object.id,name= "test")

            my_a_b_sickle_object = my_a_b_sickle.save(commit=False)
            my_a_b_sickle_object.author = request.user
            my_a_b_sickle_object.patient = my_demographics_object
            my_a_b_sickle_object.save()

            my_redcell_enzyme_object = my_redcell_enzyme.save(commit=False)
            my_redcell_enzyme_object.author = request.user
            my_redcell_enzyme_object.patient = my_demographics_object
            my_redcell_enzyme_object.save()

            my_redcell_membrane_object = my_redcell_membrane.save(commit=False)
            my_redcell_membrane_object.author = request.user
            my_redcell_membrane_object.patient = my_demographics_object
            my_redcell_membrane_object.save()

            my_cong_dys_object = my_cong_dys.save(commit=False)
            my_cong_dys_object.author = request.user
            my_cong_dys_object.patient = my_demographics_object
            my_cong_dys_object.save()

            my_cln_dt_object = my_cln_dt.save(commit=False)
            my_cln_dt_object.author = request.user
            my_cln_dt_object.patient = my_demographics_object
            my_cln_dt_object.save()

            my_cln_dt_two_object = my_cln_dt_two.save(commit=False)
            my_cln_dt_two_object.author = request.user
            my_cln_dt_two_object.patient = my_demographics_object
            my_cln_dt_two_object.save()

            my_patient_reported_outcomes_object = my_patient_reported_outcomes.save(commit=False)
            my_patient_reported_outcomes_object.author = request.user
            my_patient_reported_outcomes_object.patient = my_demographics_object
            my_patient_reported_outcomes_object.save()


        # submitted = request.POST.get('form_id', '')
        # print submitted
        # my_demographics = DemographicForm(request.POST)
        # my_diagnosis = DiagnosisForm(request.POST or None)
        # my_a_b_sickle= A_b_sickle_thalForm(request.POST or None)
        #
        #
        #
        # if submitted == 'demographics':
        #     # Get the Form1 instance
        #     my_demographics = DemographicForm(request.POST)
        #     #my_diagnosis = DiagnosisForm()
        #
        #     if my_demographics.is_valid():
        #         for k, v in my_demographics.cleaned_data.iteritems():
        #             request.session[k] = v
        #         my_demographics_object= my_demographics.save()
        #         patient = my_demographics.cleaned_data['patient_id']
        #         #my_demographics=DemographicForm(my_demographics_object)
        #         my_diagnosis = DiagnosisForm({'patient': patient, 'diagnosis_option': 'b-thalassaemia syndromes'})
        #         my_a_b_sickle = A_b_sickle_thalForm({'patient': my_demographics_object.patient_id})
        #     else:
        #         my_diagnosis=DiagnosisForm()
        #         my_a_b_sickle = A_b_sickle_thalForm()
        #
        #
        # elif submitted == 'diagnosis':
        #     my_diagnosis = DiagnosisForm(request.POST)
        #
        #     my_demographics = DemographicForm()
        #     my_a_b_sickle = A_b_sickle_thalForm()
        #     if my_diagnosis.is_valid():
        #         my_diagnosis_object=my_diagnosis.save()
        #         my_a_b_sickle =A_b_sickle_thalForm({'patient': my_diagnosis_object.patient})
        #
        #     else:
        #         my_demographics = DemographicForm()
        #         my_a_b_sickle = A_b_sickle_thalForm()
        #
        # elif submitted == 'a_b_sickle':
        #     my_a_b_sickle = A_b_sickle_thalForm(request.POST)
        #     my_demographics = DemographicForm()
        #     my_diagnosis = DiagnosisForm()
        #
        #     if my_a_b_sickle.is_valid():
        #         my_a_b_sickle.save()

        else:
            print "No valid"
        #     raise ValueError('No form specified !')
    else:
        diag_option=0
        my_demographics = DemographicForm(prefix='demo')
        my_diagnosis = DiagnosisForm(prefix='diag')
        my_a_b_sickle= A_b_sickle_thalForm(prefix='a_b_s')
        my_redcell_enzyme = Redcell_enzyme_disForm(prefix='rc_enz')
        my_redcell_membrane= Redcell_membrane_disForm(prefix='rc_mbr')
        my_cong_dys = Cong_dyseryth_anaemiaForm(prefix='cong_dys')
        my_cln_dt= ClinicalDataForm(prefix='cln_dt')
        my_cln_dt_two= ClinicalDataTwo(prefix='cln_dt_two')
        my_patient_reported_outcomes = Patient_Reported_outcomeForm(prefix='ptn_rep_out')

    if ret is None:
        ret = render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_cln_dt_two': my_cln_dt_two, 'ptn_rep_out':my_patient_reported_outcomes}, context)
        cache.set('input-rendered', ret)
    if ret is not None and request.method != 'POST':
        return ret
    else:
        return render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_cln_dt_two': my_cln_dt_two, 'ptn_rep_out':my_patient_reported_outcomes}, context)
        # submitted = request.POST.get('form_id', '')
        #
        # if submitted == 'demographics':
        #     # Get the Form1 instance
        #     my_demographics = DemographicForm(request.POST)
        #     if my_demographics.is_valid():
        #         my_demographics_object= my_demographics.save()
        #         my_diagnosis=DiagnosisForm({'patient': my_demographics_object.patient_id})
        #
        #
        # elif submitted == 'diagnosis':
        #     # Get the Form2 instance
        #     my_diagnosis = DiagnosisForm(request.POST)
        #     if my_diagnosis.is_valid():
        #         my_diagnosis.save()
        #
        # else:
        #     raise ValueError('No form specified !')



    # if request.method == 'POST':
    #     my_demographics = DemographicForm(request.POST)
    #     #my_diagnosis = DiagnosisForm(request.POST or None)
    #
    #     if my_demographics.is_valid():
    #         my_demographics_object = my_demographics.save()
    #         my_diagnosis = DiagnosisForm({'patient': my_demographics_object.patient_id})
    #
    #
    #     elif my_diagnosis.is_valid():
    #         my_diagnosis.save()
@login_required(login_url='/login')
def search(request):
    context = RequestContext(request)

    value=0
    my_alert_option=request.COOKIES.get('no_patient', False)
    if my_alert_option == "True":
        my_alert="1"
    else:
        my_alert="0"
    print "my_alert"
    print my_alert
    if request.method == "POST":
        value = 1
        my_demographics = DemographicForm(request.POST, prefix="demo")
        my_diagnosis = DiagnosisForm(request.POST, prefix='diag')
        my_a_b_sickle= A_b_sickle_thalForm(request.POST,prefix='a_b_s')
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST, prefix='rc_enz')
        my_redcell_membrane= Redcell_membrane_disForm(request.POST, prefix='rc_mbr')
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST, prefix='cong_dys')
        my_cln_dt= ClinicalDataForm(request.POST, prefix='cln_dt')

        if 'id' in request.POST and request.POST['id']:
            with transaction.atomic():
                id = request.POST['id']
                department = Institution.objects.filter(user=request.user).first().department
                #print "dep"
                #print department
                patient = Demographic.objects.filter(patient_id__icontains=id, author__institution__department=department)
                #print patient
                #print patient.count()
                # books = Book.objects.filter(title__icontains=q)
                response =  render_to_response( 'search.html', {'patient': patient, 'query': id, 'option':value},context)
                response.delete_cookie('no_patient')
                return response


        response =  redirect('results.html', {'frm':my_demographics, 'option': value, 'my_alert':my_alert}, context)
        response.delete_cookie('no_patient')
        return response
    else:
        response =  render_to_response('search.html', {'option': value, 'my_alert':my_alert}, context)
        response.delete_cookie('no_patient')
        return response

@login_required(login_url='/login')
def results(request):

    context = RequestContext(request)
    myid = request.GET.get('id', '')
    #diagnosis option for saving purposes. In order to save only specific tables in db.
    diag_option = 0
    print "my id", myid
    if request.method == 'POST':
        with transaction.atomic():
            print "HERE ELSE"
            try:
                department = Institution.objects.filter(user=request.user).first().department
                patient = Demographic.objects.get(patient_id=myid, author__institution__department=department)
            except Demographic.DoesNotExist:
                patient = None
            if patient == None:
                my_alert = "1"
                return render_to_response('search.html',{'my_alert':my_alert}, context)

            diag_patient = Diagnosis.objects.get(patient=myid, author__institution__department=department)
            #diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid, author__institution__department=department)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid, author__institution__department=department)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid, author__institution__department=department)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid, author__institution__department=department)
            cln_dt_patient= Clinical_data.objects.get(patient=myid, author__institution__department=department)
            cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid, author__institution__department=department)
            patient_reported_outcomes_patient = Patient_reported_outcome.objects.get(patient=myid, author__institution__department=department)






        my_demographics = DemographicForm(request.POST or None, prefix="demo", instance=patient)
        my_diagnosis = DiagnosisForm(request.POST,prefix='diag', instance=diag_patient)

        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
        my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
        my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)
        my_patient_reported_outcomes = Patient_Reported_outcomeForm(request.POST or None, prefix='pat_rep_out', instance=patient_reported_outcomes_patient)

        for formfield in my_diagnosis:
            print formfield.name
            if formfield.name == 'diagnosis_option':
                dig_opt_list =  formfield.value()
                print "it has"
                print dig_opt_list
            if formfield.name == 'icd_10_desc':
                icd_10_opt_list =  formfield.value()
            if formfield.name == 'orpha_code':
                orpha_opt_list =  formfield.value()
        #print "dig_opt_list"
        #print dig_opt_list


        #print "HERE FIRST IF"
        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_a_b_sickle.is_valid and my_redcell_enzyme.is_valid() and my_redcell_membrane.is_valid() and my_cong_dys.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid() and my_patient_reported_outcomes.is_valid():


            #print "HERE SECOND IF"

            my_demographics_object = my_demographics.save(commit=False)
            my_demographics_object.author = request.user
            my_demographics_object.save()

            mylist = diag_patient.diagnosis_option.all()
            #print "mylist"
            #print mylist
            mylist_icd_10 = diag_patient.icd_10_desc.all()
            mylist_orpha =   diag_patient.orpha_code.all()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.author = request.user
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()


            x = mylist.values('id')
            w = mylist_icd_10.values('id')
            e =  mylist_orpha.values('id')

            db_diag_values = [int(y['id']) for y in x]
            db_icd10_values =  [int(y['id']) for y in w]
            db_orpha_values =  [int(y['id']) for y in e]

            dig_opt_list_values=[]
            icd_10_opt_list_values=[]
            orpha_opt_list_values=[]

            for d in xrange (0, len(dig_opt_list)):
                dig_opt_list_values.append(int(dig_opt_list[d]))

            for d in xrange (0, len(icd_10_opt_list)):
                icd_10_opt_list_values.append(int(icd_10_opt_list[d]))

            for d in xrange (0, len(orpha_opt_list)):
                orpha_opt_list_values.append(int(orpha_opt_list[d]))

            #print "icd1 10 opt list"
            #print icd_10_opt_list_values


            #If a new diagnosis option in not in DB for user, add it
            for x in xrange(0, len(dig_opt_list_values)):
                if int(dig_opt_list_values[x]) not in db_diag_values:
                    my_diagnosis_object.diagnosis_option.add(dig_opt_list_values[x])

            for x in xrange(0, len(icd_10_opt_list_values)):
                if int(icd_10_opt_list_values[x]) not in db_icd10_values:
                    my_diagnosis_object.icd_10_desc.add(icd_10_opt_list_values[x])

            for x in xrange(0, len(orpha_opt_list_values)):
                if int(orpha_opt_list_values[x]) not in db_orpha_values:
                    my_diagnosis_object.orpha_code.add(orpha_opt_list_values[x])

            #If remove a diagnosis, remove it from DB
            for y in xrange(0, len(db_diag_values)):
                if db_diag_values[y] not in dig_opt_list_values:
                    my_diagnosis_object.diagnosis_option.remove(db_diag_values[y])

            for y in xrange(0, len(db_icd10_values)):
                if db_icd10_values[y] not in icd_10_opt_list_values:
                    my_diagnosis_object.icd_10_desc.remove(db_icd10_values[y])

            for y in xrange(0, len(db_orpha_values)):
                if db_orpha_values[y] not in orpha_opt_list_values:
                    my_diagnosis_object.orpha_code.remove(db_orpha_values[y])





            #my_diagnosis_object.set_all()


            #my_diagnosis_object.diagnosis_options.add(id=my_diagnosis_object.id,name= "test")

            my_a_b_sickle_object = my_a_b_sickle.save(commit=False)
            my_a_b_sickle_object.author = request.user
            my_a_b_sickle_object.patient = my_demographics_object
            my_a_b_sickle_object.save()

            my_redcell_enzyme_object = my_redcell_enzyme.save(commit=False)
            my_redcell_enzyme_object.author = request.user
            my_redcell_enzyme_object.patient = my_demographics_object
            my_redcell_enzyme_object.save()

            my_redcell_membrane_object = my_redcell_membrane.save(commit=False)
            my_redcell_membrane_object.author = request.user
            my_redcell_membrane_object.patient = my_demographics_object
            my_redcell_membrane_object.save()

            my_cong_dys_object = my_cong_dys.save(commit=False)
            my_cong_dys_object.author = request.user
            my_cong_dys_object.patient = my_demographics_object
            my_cong_dys_object.save()

            my_cln_dt_object = my_cln_dt.save(commit=False)
            my_cln_dt_object.author = request.user
            my_cln_dt_object.patient = my_demographics_object
            my_cln_dt_object.save()

            my_cln_dt_two_object = my_cln_dt_two.save(commit=False)
            my_cln_dt_two_object.author = request.user
            my_cln_dt_two_object.patient = my_demographics_object
            my_cln_dt_two_object.save()

            my_patient_reported_outcomes_object = my_patient_reported_outcomes.save(commit=False)
            my_patient_reported_outcomes_object.author = request.user
            my_patient_reported_outcomes_object.patient = my_demographics_object
            my_patient_reported_outcomes_object.save()




    else:
        diag_option=0
        with transaction.atomic():
            print "HERE ELSE ELSE"
            try:
                department = Institution.objects.filter(user=request.user).first().department
                patient = Demographic.objects.get(patient_id=myid, author__institution__department=department)
            except Demographic.DoesNotExist:
                patient = None
            if patient == None:
                my_alert = "1"
                response = redirect('search')
                response.set_cookie('no_patient', 'True')
                return response

            diag_patient = Diagnosis.objects.get(patient=myid, author__institution__department=department)
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid, author__institution__department=department)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid,author__institution__department=department)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid, author__institution__department=department)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid, author__institution__department=department)
            cln_dt_patient= Clinical_data.objects.get(patient=myid, author__institution__department=department)
            cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid,author__institution__department=department)
            patient_reported_outcomes_patient = Patient_reported_outcome.objects.get(patient=myid,author__institution__department=department)

            # print "diag_val"
            # for diag_opt in diag_val.all():
            #     print diag_opt




        #print "diag_option=", diag_option
        my_demographics = DemographicForm(request.POST or None,prefix="demo",instance=patient)
        # my_demographics = DemographicForm(initial=form_data,)

        # my_demographics = DemographicForm(prefix='demo')

        my_diagnosis = DiagnosisForm(request.POST or None,prefix='diag', instance=diag_patient)

        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
        my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
        my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)
        my_patient_reported_outcomes = Patient_Reported_outcomeForm(request.POST or None, prefix='pat_rep_out', instance=patient_reported_outcomes_patient)


    return render_to_response('results.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt':my_cln_dt,'frm_cln_dt_two': my_cln_dt_two, 'ptn_rep_out':my_patient_reported_outcomes}, context)


# @login_required(login_url='/login')
# def search_patient_card(request):
#     context = RequestContext(request)
#     value=0
#     if request.method == "POST":
#         value = 1
#         my_demographics = DemographicForm(request.POST, prefix="demo")
#         my_diagnosis = DiagnosisForm(request.POST, prefix='diag')
#         my_a_b_sickle= A_b_sickle_thalForm(request.POST,prefix='a_b_s')
#         my_redcell_enzyme = Redcell_enzyme_disForm(request.POST, prefix='rc_enz')
#         my_redcell_membrane= Redcell_membrane_disForm(request.POST, prefix='rc_mbr')
#         my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST, prefix='cong_dys')
#         my_cln_dt= ClinicalDataForm(request.POST, prefix='cln_dt')
#
#         if 'id' in request.POST and request.POST['id']:
#             with transaction.atomic():
#                 id = request.POST['id']
#                 patient = Demographic.objects.filter(patient_id__icontains=id)
#                 print patient
#                 print patient.count()
#                 # books = Book.objects.filter(title__icontains=q)
#                 return render(request, 'search_patient_card.html',
#                     {'patient': patient, 'query': id, 'option':value})
#
#     # if request.is_ajax() and request.method == "POST":
#     #     myid= request.POST.get("sentence","")
#     #     #response_data=fil(sentence)
#     #     print myid
#     #     patient = Demographic.objects.select_for_update().filter(patient_id = myid)
#     #     data = serializers.serialize('json', patient)
#     #     json_data = json.loads(data)[0]
#     #     form_data = json_data['fields']
#     #     print form_data
#     #     my_demographics = DemographicForm(initial=form_data)
#     #     print my_demographics
#     #     # new_d = serializers.deserialize("json", data)
#     #     # print new_d
#     #     # myp = Demographic.objects.raw('SELECT * from `eReg_demographic`')
#     #     # for p in myp:
#     #     #     print p
#     #     # my_data = json.loads(data)
#     #
#     #     for pat in patient:
#     #         print pat.given_name
#
#         return redirect('results_patient_card.html', {'frm':my_demographics, 'option': value}, context)
#     else:
#         return render_to_response('search_patient_card.html', {'option': value}, context)
#
#
# @login_required(login_url='/login')
# def results_patient_card(request):
#
#     context = RequestContext(request)
#     myid = request.GET.get('id', '')
#     #diagnosis option for saving purposes. In order to save only specific tables in db.
#     diag_option = ''
#     print "my id", myid
#     if request.method == 'POST':
#         with transaction.atomic():
#             print "HERE ELSE"
#             patient = Demographic.objects.get(patient_id=myid)
#             diag_patient = Diagnosis.objects.get(patient=myid)
#             diag_val = diag_patient.diagnosis_option
#             a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
#             r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
#             r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
#             c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
#             cln_dt_patient= Clinical_data.objects.get(patient=myid)
#             cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid)
#
#         # if (diag_val == 'b-thalassaemia syndromes' or diag_val == 'a-thalassaemia syndromes' or diag_val == 'Sickle cell syndromes' or diag_val == 'Other haemoglobin variants'):
#         #     diag_option = ='1'
#         # elif (diag_val == 'Rare cell enzyme disorders'):
#         #     diag_option = 2
#         # elif (diag_val == 'Rare cell membrane disorders'):
#         #     diag_option = 3
#         # elif (diag_val == 'Congenital desyrythropoietic anaemias'):
#         #     diag_option = 4
#         if(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val)):
#             diag_option = diag_option +'1'
#         if('Rare cell enzyme disorders' in diag_val):
#             diag_option = diag_option +'2'
#         if('Rare cell membrane' in diag_val):
#             diag_option = diag_option +'3'
#         if('Congenital desyrythropoietic anaemias' in diag_val):
#             diag_option = diag_option +'4'
#
#
#         my_demographics = DemographicForm(request.POST or None, prefix="demo", instance=patient)
#         my_diagnosis = DiagnosisForm(request.POST or None,prefix='diag', instance=diag_patient)
#         my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
#         my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
#         my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
#         my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
#         my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
#         my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)
#
#         print "HERE FIRST IF"
#         if my_demographics.is_valid() and my_diagnosis.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid()  and (my_a_b_sickle.is_valid or my_redcell_enzyme.is_valid() or my_redcell_membrane.is_valid() or my_cong_dys.is_valid()):
#             print "HERE SECOND IF"
#             print my_demographics.given_name
#             my_demographics_object = my_demographics.save()
#
#             my_diagnosis_object = my_diagnosis.save(commit=False)
#             my_diagnosis_object.patient = my_demographics_object
#             my_diagnosis_object.save()
#
#             my_a_b_sickle_object = my_a_b_sickle.save(commit=False)
#             my_a_b_sickle_object.patient = my_demographics_object
#             my_a_b_sickle_object.save()
#
#             my_redcell_enzyme_object = my_redcell_enzyme.save(commit=False)
#             my_redcell_enzyme_object.patient = my_demographics_object
#             my_redcell_enzyme_object.save()
#
#             my_redcell_membrane_object = my_redcell_membrane.save(commit=False)
#             my_redcell_membrane_object.patient = my_demographics_object
#             my_redcell_membrane_object.save()
#
#             my_cong_dys_object = my_cong_dys.save(commit=False)
#             my_cong_dys_object.patient = my_demographics_object
#             my_cong_dys_object.save()
#
#             my_cln_dt_object = my_cln_dt.save(commit=False)
#             my_cln_dt_object.patient = my_demographics_object
#             my_cln_dt_object.save()
#
#
#
#     else:
#         diag_option=''
#         with transaction.atomic():
#             print "HERE ELSE"
#             patient = Demographic.objects.get(patient_id=myid)
#             diag_patient = Diagnosis.objects.get(patient=myid)
#             diag_val = diag_patient.diagnosis_option
#             a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
#             r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
#             r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
#             c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
#             cln_dt_patient=Clinical_data.objects.get(patient=myid)
#             cln_dt_two_patient=Clinical_data_two.objects.get(patient=myid)
#
#             sum_card_one=OrderedDict()
#             sum_card_one['Demographics']= 'title'
#             sum_card_one[patient._meta.get_field('given_name').verbose_name.title()]= patient.given_name
#             sum_card_one[patient._meta.get_field('surname').verbose_name.title()]= patient.surname
#             sum_card_one[patient._meta.get_field('patient_id').verbose_name.title()]=patient.patient_id
#             sum_card_one[patient._meta.get_field('national_health_care_pat_id').verbose_name.title()]=patient.national_health_care_pat_id
#             sum_card_one[patient._meta.get_field('date_of_birth').verbose_name.title()]=patient.date_of_birth
#             #sum_card_one[patient._meta.get_field('blood_group').verbose_name.title()]= patient.blood_group
#             sum_card_one['Diagnosis']= 'title'
#             #sum_card_one[diag_patient._meta.get_field('diagnosis_option').verbose_name.title()]= diag_patient.diagnosis_option
#
#
#             str_diag_val =ast.literal_eval(diag_val)
#
#             for x in range(0, len(str_diag_val)):
#                 #print "diagnosis value=", str_diag_val[x]
#                 new_string = 'Diagnosis option ' + str(x+1)
#                 sum_card_one[new_string]= str_diag_val[x]
#             print sum_card_one['Diagnosis option 1']
#             if "thal" in diag_patient.diagnosis_option:
#                 sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_a_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_a_gene
#                 sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_b_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_b_gene
#                 sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_g_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_g_gene
#             sum_card_one[diag_patient._meta.get_field('diagnosis_circumstances').verbose_name.title()]=diag_patient.diagnosis_circumstances
#             sum_card_one[diag_patient._meta.get_field('diagnosis_circumstances_date').verbose_name.title()]=diag_patient.diagnosis_circumstances_date
#
#             # sum_card_one = { patient._meta.get_field('given_name').verbose_name.title():patient.given_name,
#             #                  patient._meta.get_field('surname').verbose_name.title():patient.surname,
#             #                  patient._meta.get_field('national_health_care_pat_id').verbose_name.title():patient.national_health_care_pat_id,
#             #                  patient._meta.get_field('patient_id').verbose_name.title():patient.patient_id,
#             #                  patient._meta.get_field('date_of_birth').verbose_name.title():patient.date_of_birth,
#             #                  diag_patient._meta.get_field('diagnosis_option').verbose_name.title(): diag_patient.diagnosis_option
#             # }
#
#             print type(sum_card_one)
#             formOne = UserCreationForm(request.POST or None, extra=sum_card_one, initial=sum_card_one)
#         #     data = serializers.serialize('json', patient)
#         #     diag_data = serializers.serialize('json', diag_patient)
#         #
#         #     json_data = json.loads(data)[0]
#         #     json_diag_data = json.loads(diag_data)[0]
#         #
#         #     # print "here", json_data
#         #     form_data = json_data['fields']
#         #     form_diag_data = json_diag_data['fields']
#         #     diag_val= form_diag_data['diagnosis_option']
#         #     form_data['patient_id'] = myid
#         # # print form_data
#         # #
#         if(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val)):
#             diag_option = diag_option +'1'
#         if('Rare cell enzyme disorders' in diag_val):
#             diag_option = diag_option +'2'
#         if('Rare cell membrane' in diag_val):
#             diag_option = diag_option +'3'
#         if('Congenital desyrythropoietic anaemias' in diag_val):
#             diag_option = diag_option +'4'
#         my_demographics = DemographicForm(prefix="demo",instance=patient)
#         # my_demographics = DemographicForm(initial=form_data,)
#
#         # my_demographics = DemographicForm(prefix='demo')
#         my_diagnosis = DiagnosisForm(prefix='diag', instance=diag_patient)
#         my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
#         my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
#         my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
#         my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
#         my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
#         my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)
#
#
#     return render_to_response('results_patient_card.html', {'frm':formOne, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_cln_dt_two': my_cln_dt_two}, context)



def test(request):
    return render_to_response('test.html')

@login_required(login_url='/login')
def statistics(request):
    context = RequestContext(request)
    today = date.today()
    days_in_year = 365.2425

    total_num = Demographic.objects.all()

    for e in total_num:
        t = Demographic.objects.get(patient_id=e.patient_id)
        t.age = ((date.today() - e.date_of_birth).days / days_in_year)
        t.save()

    #print "COUNTER:", total_num._meta.get_field('gender')
    females = Demographic.objects.filter(gender__startswith='F')
    males = Demographic.objects.filter(gender__startswith='M')
    date_of_birth = Demographic.objects.all().values_list('date_of_birth')



    #PATIENT CONSENT
    signed_by_pat = Demographic.objects.filter(data_entered_by='Patient').count()
    signed_by_oth =  Demographic.objects.filter(data_entered_by='Other').count()
    signed_data_storage = Demographic.objects.filter(patient_consent_for_data_storage='I agree').count()
    signed_data_reusage = Demographic.objects.filter(patient_consent_for_data_reusage='I agree').count()
    signed_data_both = Demographic.objects.filter(patient_consent_for_data_storage='I agree', patient_consent_for_data_reusage='I agree').count()
    signed_other_clas = Demographic.objects.exclude(data_entered_by_relationship__isnull=True).exclude(data_entered_by_relationship="")
    #signed_other_clas = Demographic.objects.filter(data_entered_by_relationship__isnull=True).exclude(alias="")
    #print signed_other_clas


    #signed_by_relationship = Demographic.objects.values('data_entered_by_relationship').annotate(cnt=Count('data_entered_by_relationship'))
    #for q in signed_by_relationship:
    #    print(q['data_entered_by_relationship'], q['cnt'])

    #print date_of_birth[0][0]
    x = date_of_birth.count()
    months_in_year = 12
    age_dist=[]
    for i in range(0,x):
        age = ((date.today() - date_of_birth[i][0]).days / days_in_year)
        age_dist.append(int(age))
        #print age
        #years
        if age > 1:
            print date_of_birth[i][0]
            print 'age', int(age), 'years'

        #months
        elif age > 0.0833 :
            print date_of_birth[i][0]
            print 'age', int(((date.today() - date_of_birth[i][0]).days / days_in_year)*12), 'months'
        else:
            print date_of_birth[i][0]
            print 'age', (date.today() - date_of_birth[i][0]).days, 'days'

    age_dist=sorted(age_dist)
    #Find frequencies of elements
    freq_age_dist = collections.Counter(age_dist)
    #print "FREQ:", freq_age_dist

    #print 'total count', total_num.count()
    #print 'females', females.count()
    #print 'males', males.count()
    #print 'birthdays', age_dist
    #print "COUNT:", Count(age_dist)

    age_dict={}
    for i in freq_age_dist:
        age_dict[str(i)+'i']=freq_age_dist[i]
    #print "DICT", age_dict

    signed_by_c = PivotDataPool(
        series=[
            {'options': {
                'source':Demographic.objects.all(),
                'categories':['data_entered_by'] },
                'terms':{
                    'signed_count':Count('data_entered_by'),

                    }
            }
        ]
    )

    signed_by_c1 = PivotChart(
        datasource=signed_by_c,
        series_options =
              [{'options':{
                'type': 'column',
                #'stacking': True
                },
                'terms':[
                'signed_count']}],
         chart_options =
              {'title': {
                   'text': 'Signed by patient vs signed by other'},
               'xAxis': {
                    'title': {
                       'text': 'Signed by'}}}
    )

    signed_by_rel = PivotDataPool(
        series=[
            {'options': {
                'source':signed_other_clas,
                'categories':['data_entered_by_relationship'] },
                'terms':{
                    'signed_rel_count':Count('data_entered_by_relationship'),

                    }
            }
        ]
    )

    signed_by_rel1 = PivotChart(
        datasource=signed_by_rel,
        series_options =
              [{'options':{
                'type': 'column',
                #'stacking': True
                },
                'terms':[
                'signed_rel_count']}],
         chart_options =
              {'title': {
                   'text': '"Other" classification'},
               'xAxis': {
                    'title': {
                       'text': 'Signed by'}}}
    )

    #TOTALS
    #1
    tot_diag = PivotDataPool(
        series=[
            {'options': {
                'source':DiagnosisOption.objects.all(),
                'categories':'diag_option' },
                'terms':{
                    'Number_of_patients':Count('diagnosis'),

                    }
            }
        ]
    )

    tot_diag1 = PivotChart(
        datasource=tot_diag,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Total number of patients per diagnosis'},
               'xAxis': {
                    'title': {
                       'text': 'Diagnosis'}}}
    )

    #2
    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='1')

    tot_diag_thalb = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thalb1 = PivotChart(
        datasource=tot_diag_thalb,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'b-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='2')

    tot_diag_thala = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thala1 = PivotChart(
        datasource=tot_diag_thala,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'a-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='3')

    tot_diag_sck = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_sck1 = PivotChart(
        datasource=tot_diag_sck,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Sickle cell syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='4')

    tot_diag_other = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_other1 = PivotChart(
        datasource=tot_diag_other,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Other haemoglobin variants'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='5')

    tot_diag_mem = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_mem1 = PivotChart(
        datasource=tot_diag_mem,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell membrane disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='6')

    tot_diag_enz = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_enz1 = PivotChart(
        datasource=tot_diag_enz,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell enzyme disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='7')

    tot_diag_cong = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['address_country'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_cong1 = PivotChart(
        datasource=tot_diag_cong,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Congenital dyserythropoietic anaemias'},
               'xAxis': {
                    'title': {
                       'text': 'By country of residence'}}}
    )


    #3
    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='1')

    tot_diag_thalb_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thalb_con_or1 = PivotChart(
        datasource=tot_diag_thalb_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'b-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='2')

    tot_diag_thala_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thala_con_or1 = PivotChart(
        datasource=tot_diag_thala_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'a-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='3')

    tot_diag_sck_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_sck_con_or1 = PivotChart(
        datasource=tot_diag_sck_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Sickle cell syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='4')

    tot_diag_other_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_other_con_or1 = PivotChart(
        datasource=tot_diag_other_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Other haemoglobin variants'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='5')

    tot_diag_mem_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_mem_con_or1 = PivotChart(
        datasource=tot_diag_mem_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell membrane disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='6')

    tot_diag_enz_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_enz_con_or1 = PivotChart(
        datasource=tot_diag_enz_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell enzyme disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='7')

    tot_diag_cong_con_or = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['country_of_birth'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_cong_con_or1 = PivotChart(
        datasource=tot_diag_cong_con_or,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Congenital dyserythropoietic anaemias'},
               'xAxis': {
                    'title': {
                       'text': 'By country of origin'}}}
    )


    #4
    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='1')

    tot_diag_thalb_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thalb_race1 = PivotChart(
        datasource=tot_diag_thalb_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'b-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='2')

    tot_diag_thala_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thala_race1 = PivotChart(
        datasource=tot_diag_thala_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'a-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='3')

    tot_diag_sck_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_sck_race1 = PivotChart(
        datasource=tot_diag_sck_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Sickle cell syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='4')

    tot_diag_other_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_other_race1 = PivotChart(
        datasource=tot_diag_other_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Other haemoglobin variants'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='5')

    tot_diag_mem_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_mem_race1 = PivotChart(
        datasource=tot_diag_mem_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell membrane disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='6')

    tot_diag_enz_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_enz_race1 = PivotChart(
        datasource=tot_diag_enz_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell enzyme disorders'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='7')

    tot_diag_cong_race = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['race'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_cong_race1 = PivotChart(
        datasource=tot_diag_cong_race,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Congenital dyserythropoietic anaemias'},
               'xAxis': {
                    'title': {
                       'text': 'By ethnic origin'}}}
    )




    #BY DATE OF BIRTH (AGE) AND FOR EACH DIAGNOSIS
    #1
    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='1')

    tot_diag_thalb_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thalb_age1 = PivotChart(
        datasource=tot_diag_thalb_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'b-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='2')

    tot_diag_thala_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_thala_age1 = PivotChart(
        datasource=tot_diag_thala_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'a-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='3')

    tot_diag_sck_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_sck_age1 = PivotChart(
        datasource=tot_diag_sck_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Sickle cell syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='4')

    tot_diag_other_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_other_age1 = PivotChart(
        datasource=tot_diag_other_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Other haemoglobin variants'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='5')

    tot_diag_mem_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_mem_age1 = PivotChart(
        datasource=tot_diag_mem_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell membrane disorders'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='6')

    tot_diag_enz_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_enz_age1 = PivotChart(
        datasource=tot_diag_enz_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Rare cell enzyme disorders'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    Diag_opt = Demographic.objects.filter(diagnosis__diagnosis_option='7')

    tot_diag_cong_age = PivotDataPool(
        series=[
            {'options': {
                'source':Diag_opt,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('diagnosis__diagnosis_option'),

                    }
            }
        ]
    )

    tot_diag_cong_age1 = PivotChart(
        datasource=tot_diag_cong_age,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Congenital dyserythropoietic anaemias'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #2 Age by educational level
    edu_level = Demographic.objects.filter(education='Primary')

    edu_by_age_prim = PivotDataPool(
        series=[
            {'options': {
                'source':edu_level,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('education'),

                    }
            }
        ]
    )

    edu_by_age_prim1 = PivotChart(
        datasource=edu_by_age_prim,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Primary'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    edu_level = Demographic.objects.filter(education='Secondary')

    edu_by_age_sec = PivotDataPool(
        series=[
            {'options': {
                'source':edu_level,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('education'),

                    }
            }
        ]
    )

    edu_by_age_sec1 = PivotChart(
        datasource=edu_by_age_sec,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Secondary'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    edu_level = Demographic.objects.filter(education='University')

    edu_by_age_uni = PivotDataPool(
        series=[
            {'options': {
                'source':edu_level,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('education'),

                    }
            }
        ]
    )

    edu_by_age_uni1 = PivotChart(
        datasource=edu_by_age_uni,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'University'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    edu_level = Demographic.objects.filter(education='Other')

    edu_by_age_oth = PivotDataPool(
        series=[
            {'options': {
                'source':edu_level,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('education'),

                    }
            }
        ]
    )

    edu_by_age_oth1 = PivotChart(
        datasource=edu_by_age_oth,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Other'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )
    #3
    employ_age = Demographic.objects.filter(Q(profession='Full time') | Q(profession="Part time"))

    employ_age_dist = PivotDataPool(
        series=[
            {'options': {
                'source':employ_age,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('profession'),

                    }
            }
        ]
    )

    employ_age_dist1 = PivotChart(
        datasource=employ_age_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Employment'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    unemploy_age = Demographic.objects.filter(profession='Unemployed')

    unemploy_age_dist = PivotDataPool(
        series=[
            {'options': {
                'source':unemploy_age,
                'categories':['age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('profession'),

                    }
            }
        ]
    )

    unemploy_age_dist1 = PivotChart(
        datasource=unemploy_age_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Unemployment'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #4 Age by marriage
    adults_all = Demographic.objects.filter(Q(age__gte=18)).count()

    #Use this to catch ZeroDivisionError
    if adults_all == 0:
        adults_all=1

    adults_married = Demographic.objects.filter(Q(age__gte=18) &  Q(family_situation="married")).count()
    prop_married = '{:2.0f}'.format((adults_married/adults_all)*100)
    #print ("adults")
    #print (prop_married)

    #5 Proportion of adult patients who are parents
    adults_parents = Demographic.objects.filter(Q(age__gte=18) &  Q(no_of_children__gt="0")).count()
    prop_parents = '{:2.0f}'.format((adults_parents/adults_all)*100)
    #print prop_parents

    #6 Age starting penicilin prophylaxis

    total_pat_penic = Clinical_data_two.objects.filter(prophylactic_measures_antibiotic_prophylaxis_penicillin_date__isnull = False)

    for penic in total_pat_penic:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = penic.patient.patient_id
        dob = penic.patient.date_of_birth
        penic_date = penic.prophylactic_measures_antibiotic_prophylaxis_penicillin_date
        if (t.prophylactic_measures_antibiotic_prophylaxis_penicillin_age is None):
            t.prophylactic_measures_antibiotic_prophylaxis_penicillin_age = ((penic_date-dob).days / days_in_year)
            t.save()


    penic_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_penic,
                'categories':['prophylactic_measures_antibiotic_prophylaxis_penicillin_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('prophylactic_measures_antibiotic_prophylaxis_penicillin_age'),

                    }
            }
        ]
    )

    penic_dist1 = PivotChart(
        datasource=penic_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age starting penicillin prophylaxis/other antibiotic prophylaxis'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )


    #7 Age vaccinated
    total_pat_vacc = Clinical_data_two.objects.filter(prophylactic_measures_vaccinations_pneumococcal_OCV_date__isnull = False)

    for vacc in total_pat_vacc:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = vacc.patient.date_of_birth
        vacc_date = vacc.prophylactic_measures_vaccinations_pneumococcal_OCV_date
        if (t.prophylactic_measures_vaccinations_pneumococcal_OCV_age is None):
            t.prophylactic_measures_vaccinations_pneumococcal_OCV_age = ((vacc_date-dob).days / days_in_year)
            t.save()


    vacc_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_vacc,
                'categories':['prophylactic_measures_vaccinations_pneumococcal_OCV_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('prophylactic_measures_vaccinations_pneumococcal_OCV_age'),

                    }
            }
        ]
    )

    vacc_dist1 = PivotChart(
        datasource=vacc_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age vaccinated for pneumococcus/meningococcus/haemiphilus'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #8 Age when liver functions tests became abnormal
    total_pat_liver = Clinical_data_two.objects.filter(monitoring_tests_annual_liver_profile__contains = 'Abnormal')

    for liver in total_pat_liver:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = liver.patient.date_of_birth
        liver_date = liver.monitoring_tests_annual_liver_profile_date
        if (t.monitoring_tests_annual_liver_profile_age is None):
            t.monitoring_tests_annual_liver_profile_age = ((liver_date-dob).days / days_in_year)
            t.save()


    liver_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_vacc,
                'categories':['monitoring_tests_annual_liver_profile_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_liver_profile_age'),

                    }
            }
        ]
    )

    liver_dist1 = PivotChart(
        datasource=liver_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when liver functions tests became abnormal'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )


    #9 Age when blood urea and creatine became abnormal
    total_pat_urea = Clinical_data_two.objects.filter(monitoring_tests_annual_renal_profile_blood_urea_date__isnull = False)
    total_pat_creat = Clinical_data_two.objects.filter(monitoring_tests_annual_renal_profile_creatine_date__isnull = False)

    for urea in total_pat_urea:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = urea.patient.date_of_birth
        urea_date = urea.monitoring_tests_annual_renal_profile_blood_urea_date
        if (t.monitoring_tests_annual_renal_profile_blood_urea_age is None):
            t.monitoring_tests_annual_renal_profile_blood_urea_age = ((urea_date-dob).days / days_in_year)
            t.save()

    for creat in total_pat_creat:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = creat.patient.date_of_birth
        creat_date = creat.monitoring_tests_annual_renal_profile_creatine_date
        if (t.monitoring_tests_annual_renal_profile_creatine_age is None):
            t.monitoring_tests_annual_renal_profile_creatine_age = ((creat_date-dob).days / days_in_year)
            t.save()


    urea_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_urea,
                'categories':['monitoring_tests_annual_renal_profile_blood_urea_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_renal_profile_blood_urea_age'),

                    }
            }
        ]
    )

    urea_dist1 = PivotChart(
        datasource=urea_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when blood urea and creatine became abnormal'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    creat_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_creat,
                'categories':['monitoring_tests_annual_renal_profile_creatine_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_renal_profile_creatine_age'),

                    }
            }
        ]
    )

    creat_dist1 = PivotChart(
        datasource=creat_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when creatine became abnormal'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #10 Age of appearance of proteinuria
    total_pat_proturea = Clinical_data_two.objects.filter(monitoring_tests_annual_renal_profile_proteiuria_date__isnull = False)

    for proturea in total_pat_urea:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = proturea.patient.date_of_birth
        proturea_date = proturea.monitoring_tests_annual_renal_profile_proteiuria_date
        if (t.monitoring_tests_annual_renal_profile_proteiuria_age is None):
            t.monitoring_tests_annual_renal_profile_proteiuria_age = ((proturea_date-dob).days / days_in_year)
            t.save()


    proturea_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_proturea,
                'categories':['monitoring_tests_annual_renal_profile_proteiuria_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_renal_profile_proteiuria_age'),

                    }
            }
        ]
    )

    proturea_dist1 = PivotChart(
        datasource=proturea_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of appearance of proteinuria'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )


    #11 Age when calcium metabolism became abnormal
    total_pat_calc = Clinical_data_two.objects.filter( monitoring_tests_annual_calcium_metabolism_serum_calcium_date__isnull = False)

    for calc in total_pat_calc:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = calc.patient.date_of_birth
        calc_date = calc. monitoring_tests_annual_calcium_metabolism_serum_calcium_date
        if (t.monitoring_tests_annual_calcium_metabolism_serum_calcium_age is None):
            t.monitoring_tests_annual_calcium_metabolism_serum_calcium_age = ((calc_date-dob).days / days_in_year)
            t.save()


    calc_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_calc,
                'categories':['monitoring_tests_annual_calcium_metabolism_serum_calcium_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_calcium_metabolism_serum_calcium_age'),

                    }
            }
        ]
    )

    calc_dist1 = PivotChart(
        datasource=calc_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when calcium metabolism became abnormal'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #12 Age of parvovirus positivity
    total_pat_parv = Clinical_data_two.objects.filter(monitoring_tests_annual_parvovirus_serology_date__isnull = False)

    for parv in total_pat_parv:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = parv.patient.date_of_birth
        parv_date = parv.monitoring_tests_annual_parvovirus_serology_date
        if (t.monitoring_tests_annual_parvovirus_serology_age is None):
            t.monitoring_tests_annual_parvovirus_serology_age = ((parv_date-dob).days / days_in_year)
            t.save()


    parv_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_parv,
                'categories':['monitoring_tests_annual_parvovirus_serology_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_parvovirus_serology_age'),

                    }
            }
        ]
    )

    parv_dist1 = PivotChart(
        datasource=parv_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of parvovirus positivity'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )


    #13 Age when pulmonary function became abnormal
    total_pat_pulm = Clinical_data_two.objects.filter(monitoring_tests_annual_pulmonary_function_date__isnull = False)

    for pulm in total_pat_pulm:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = parv.patient.date_of_birth
        pulm_date = pulm.monitoring_tests_annual_pulmonary_function_date
        if (t.monitoring_tests_annual_pulmonary_function_age is None):
            t.monitoring_tests_annual_pulmonary_function_age = ((pulm_date-dob).days / days_in_year)
            t.save()


    pulm_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_pulm,
                'categories':['monitoring_tests_annual_pulmonary_function_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_pulmonary_function_age'),

                    }
            }
        ]
    )

    pulm_dist1 = PivotChart(
        datasource=pulm_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when pulmonary function became abnormal'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #14 Age when hip complications appeared
    total_pat_hip = Clinical_data_two.objects.filter(monitoring_tests_annual_hip_radiology_date__isnull = False)

    for hip in total_pat_hip:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hip.patient.date_of_birth
        hip_date = hip.monitoring_tests_annual_hip_radiology_date
        if (t.monitoring_tests_annual_hip_radiology_age is None):
            t.monitoring_tests_annual_hip_radiology_age = ((hip_date-dob).days / days_in_year)
            t.save()


    hip_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hip,
                'categories':['monitoring_tests_annual_hip_radiology_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('monitoring_tests_annual_hip_radiology_age'),

                    }
            }
        ]
    )

    hip_dist1 = PivotChart(
        datasource=hip_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age when hip complications appeared (necrosis of femoral head'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #15 Age of onset of ophtalmic changes
    total_pat_oph = Clinical_data_two.objects.filter(monitoring_tests_annual_ophthalmic_evaluation_date__isnull = False)

    for oph in total_pat_oph:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = oph.patient.date_of_birth
        oph_date = oph.monitoring_tests_annual_ophthalmic_evaluation_date
        if (t.onitoring_tests_annual_ophthalmic_evaluation_age is None):
            t.onitoring_tests_annual_ophthalmic_evaluation_age = ((oph_date-dob).days / days_in_year)
            t.save()


    oph_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_oph,
                'categories':['onitoring_tests_annual_ophthalmic_evaluation_age'] ,
                },
                'terms':{
                    'Number_of_patients':Count('onitoring_tests_annual_ophthalmic_evaluation_age'),

                    }
            }
        ]
    )

    oph_dist1 = PivotChart(
        datasource=oph_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of onset of ophthalmic changes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #16 Age of dactylitis in SCD
    total_pat_dac = Clinical_data_two.objects.filter(complications_dactylitis_date__isnull = False)

    for dac in total_pat_dac:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = dac.patient.date_of_birth
        dac_date = dac.complications_dactylitis_date
        if (t.complications_dactylitis is None):
            t.complications_dactylitis = ((dac_date-dob).days / days_in_year)
            t.save()


    dac_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_dac,
                'categories':['complications_dactylitis'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_dactylitis'),

                    }
            }
        ]
    )

    dac_dist1 = PivotChart(
        datasource=dac_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of dactylitis in SCD'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #17 Age of first stroke
    total_pat_stroke = Clinical_data_two.objects.filter(complications_stroke_date__isnull = False)

    for stroke in total_pat_stroke:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = stroke.patient.date_of_birth
        stroke_date = stroke.complications_dactylitis_date
        if (t.complications_stroke is None):
            t.complications_stroke = ((stroke_date-dob).days / days_in_year)
            t.save()


    stroke_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_stroke,
                'categories':['complications_stroke'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_stroke'),

                    }
            }
        ]
    )

    stroke_dist1 = PivotChart(
        datasource=stroke_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of first stroke: silent/overt in thalassaemia (IN TDT and NTDT) and SCD'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #18 Age of splenic sequestration
    total_pat_splen = Clinical_data_two.objects.filter(complications_splenic_sequestration_date__isnull = False)

    for splen in total_pat_splen:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = splen.patient.date_of_birth
        splen_date = splen.complications_splenic_sequestration_date
        if (t.complications_splenic_sequestration is None):
            t.complications_splenic_sequestration = ((splen_date-dob).days / days_in_year)
            t.save()


    splen_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_splen,
                'categories':['complications_splenic_sequestration'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_splenic_sequestration'),

                    }
            }
        ]
    )

    splen_dist1 = PivotChart(
        datasource=splen_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of splenic sequestration'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #19 Age of aplastic crisis
    total_pat_aplastic = Clinical_data_two.objects.filter(complications_aplastic_crisis_date__isnull = False)

    for aplastic in total_pat_aplastic:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = aplastic.patient.date_of_birth
        aplastic_date = aplastic.complications_aplastic_crisis_date
        if (t.complications_aplastic_crisis is None):
            t.complications_aplastic_crisis = ((aplastic_date-dob).days / days_in_year)
            t.save()


    aplastic_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_aplastic,
                'categories':['complications_aplastic_crisis'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_aplastic_crisis'),

                    }
            }
        ]
    )

    aplastic_dist1 = PivotChart(
        datasource=aplastic_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of aplastic crisis'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #20 Age acute chest syndrome
    total_pat_chest = Clinical_data_two.objects.filter(complications_acute_chest_syndrome_date__isnull = False)

    for chest in total_pat_chest:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = chest.patient.date_of_birth
        chest_date = chest.complications_acute_chest_syndrome_date
        if (t.complications_acute_chest_syndrome is None):
            t.complications_acute_chest_syndrome = ((chest_date-dob).days / days_in_year)
            t.save()


    chest_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_chest,
                'categories':['complications_acute_chest_syndrome'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_acute_chest_syndrome'),

                    }
            }
        ]
    )

    chest_dist1 = PivotChart(
        datasource=chest_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of acute chest syndrome'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #21 Age of multi-organ failure syndrome
    total_pat_mulorg = Clinical_data_two.objects.filter(complications_multi_organ_failure_syndrome_date__isnull = False)

    for mulorg in total_pat_mulorg:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = mulorg.patient.date_of_birth
        mulorg_date = mulorg.complications_multi_organ_failure_syndrome_date
        if (t.complications_multi_organ_failure_syndrome is None):
            t.complications_multi_organ_failure_syndrome = ((mulorg_date-dob).days / days_in_year)
            t.save()


    mulorg_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_mulorg,
                'categories':['complications_multi_organ_failure_syndrome'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_multi_organ_failure_syndrome'),

                    }
            }
        ]
    )

    mulorg_dist1 = PivotChart(
        datasource=mulorg_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of multi-organ failure'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #22 Age of priapism
    total_pat_priap = Clinical_data_two.objects.filter(complications_priapism_date__isnull = False)

    for priap in total_pat_priap:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = priap.patient.date_of_birth
        priap_date = priap.complications_priapism_date
        if (t.complications_priapism is None):
            t.complications_priapism = ((priap_date-dob).days / days_in_year)
            t.save()


    priap_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_mulorg,
                'categories':['complications_priapism'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_priapism'),

                    }
            }
        ]
    )

    priap_dist1 = PivotChart(
        datasource=priap_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of priapism in SCD/NTDT'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #23 Age of heart failure
    #In b-thalassaemia
    total_pat_hf_beta = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='1')

    for hf_beta in total_pat_hf_beta:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_beta_date = hf_beta.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_beta_date-dob).days / days_in_year)
            t.save()


    hf_beta_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_beta,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_beta_dist1 = PivotChart(
        datasource=hf_beta_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in b-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In a-thalassaemia
    total_pat_hf_aplha = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='2')

    for hf_aplha in total_pat_hf_aplha:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_aplha_date = hf_aplha.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_aplha_date-dob).days / days_in_year)
            t.save()


    hf_aplha_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_aplha,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_aplha_dist1 = PivotChart(
        datasource=hf_aplha_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in a-thalassaemia syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In SCD
    total_pat_hf_sickle = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='3')

    for hf_sickle in total_pat_hf_sickle:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_sickle_date = hf_sickle.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_sickle_date-dob).days / days_in_year)
            t.save()


    hf_sickle_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_sickle,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_sickle_dist1 = PivotChart(
        datasource=hf_sickle_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in Sickle cell syndromes'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In Other haemoglobin variants
    total_pat_hf_other = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='4')

    for hf_other in total_pat_hf_other:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_other_date = hf_other.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_other_date-dob).days / days_in_year)
            t.save()


    hf_other_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_other,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_other_dist1 = PivotChart(
        datasource=hf_other_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in Other haemoglobin variants'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In membrane disorters
    total_pat_hf_membrane = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='5')

    for hf_membrane in total_pat_hf_membrane:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_membrane_date = hf_membrane.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_membrane_date-dob).days / days_in_year)
            t.save()


    hf_membrane_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_membrane,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_membrane_dist1 = PivotChart(
        datasource=hf_membrane_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in Rare cell membrane disorders'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In enzyme disorters
    total_pat_hf_enzyme = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='6')

    for hf_enzyme in total_pat_hf_enzyme:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_enzyme_date = hf_enzyme.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_enzyme_date-dob).days / days_in_year)
            t.save()


    hf_enzyme_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_enzyme,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_enzyme_dist1 = PivotChart(
        datasource=hf_enzyme_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in Rare cell enzyme disorders'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )

    #In congenital anaemias
    total_pat_hf_cong = Clinical_data_two.objects.filter(complications_heart_failure_date__isnull = False, patient__diagnosis__diagnosis_option='7')

    for hf_cong in total_pat_hf_cong:
        t = Clinical_data_two.objects.get(patient=penic.patient.patient_id)
        #id = vacc.patient.patient_id
        dob = hf_beta.patient.date_of_birth
        hf_cong_date = hf_cong.complications_heart_failure_date
        if (t.complications_heart_failure is None):
            t.complications_heart_failure = ((hf_cong_date-dob).days / days_in_year)
            t.save()


    hf_cong_dist = PivotDataPool(
        series=[
            {'options': {
                'source':total_pat_hf_cong,
                'categories':['complications_heart_failure'] ,
                },
                'terms':{
                    'Number_of_patients':Count('complications_heart_failure'),

                    }
            }
        ]
    )

    hf_cong_dist1 = PivotChart(
        datasource=hf_cong_dist,
        series_options =
              [{'options':{
                'type': 'column',
                'stacking': True
                },
                'terms':['Number_of_patients']
               }],
         chart_options =
              {'title': {
                   'text': 'Age of heart failure in Congenital dyserythropoietic anaemias'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )
    ##########
    ds = PivotDataPool(
        series=[
            {'options': {
                'source':Demographic.objects.all(),
                'categories':['gender'] },
                'terms':{
                    'sex_count':Count('gender'),

                    }
            }
        ]
    )

    pvcht = PivotChart(
        datasource=ds,
        series_options =
              [{'options':{
                'type': 'column',
                #'stacking': True
                },
                'terms':[
                'sex_count']}],
         chart_options =
              {'title': {
                   'text': 'Sex distribution'},
               'xAxis': {
                    'title': {
                       'text': 'Sex'}}}
    )

    ds_age = PivotDataPool(
        series=[
            {'options': {
                'source':Demographic.objects.all(),
                'categories':['age'] },
                'terms':{
                    'age_count': Count('age'),
                    }
            }
        ],

    )

    pvcht_age = PivotChart(
        datasource=ds_age,
        series_options =
              [{'options':{
                'type': 'column',
                #'stacking': True
                },
                'terms':[
                'age_count']}],
         chart_options =
              {'title': {
                   'text': 'Age distribution'},
               'xAxis': {
                    'title': {
                       'text': 'Age distribution'}}}
    )
    value=0
    if request.method == "POST":
        value = 1

        #my_diagnosis = DiagnosisForm(request.POST, prefix='diag')
        #my_a_b_sickle= A_b_sickle_thalForm(request.POST,prefix='a_b_s')
        #my_redcell_enzyme = Redcell_enzyme_disForm(request.POST, prefix='rc_enz')
        #my_redcell_membrane= Redcell_membrane_disForm(request.POST, prefix='rc_mbr')
        #my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST, prefix='cong_dys')
        #my_cln_dt= ClinicalDataForm(request.POST, prefix='cln_dt')

        # if 'id' in request.POST and request.POST['id']:
        #     with transaction.atomic():
        #         id = request.POST['id']
        #         patient = Demographic.objects.filter(patient_id__icontains=id)
        #         print patient
        #         print patient.count()
        #         # books = Book.objects.filter(title__icontains=q)
        #         return render(request, 'search.html',
        #             {'patient': patient, 'query': id, 'option':value})

    return render_to_response('statistics.html', {'total_num': total_num.count(),'data_storage':signed_data_storage,
                                                  #'total_patients_country_res':total_patients_country_res,
                                                  #'total_patients_country_orig':total_patients_country_orig,'total_patients_country_ethnic_orig':total_patients_country_ethnic_orig,
                                                  'data_reuse':signed_data_reusage,'data_both':signed_data_both,
                                                  'prop_married':prop_married, 'prop_parents':prop_parents,
                                                  # 'age_dist_per_diag':age_dist_per_diag,
                                                  #'total_patients_beta':total_patients_beta, 'total_patients_alpha':total_patients_alpha,
                                                  #'total_patients_sickle':total_patients_sickle,'total_patients_other_haem':total_patients_other_haem,
                                                  #'total_patients_meb_dis':total_patients_meb_dis,'total_patients_enz_dis':total_patients_enz_dis,
                                                  #'total_patients_cong':total_patients_cong,

                                                  'females': females.count(), 'males': males.count(),
                                                  'age_values': freq_age_dist.keys(),'age_freq':freq_age_dist.values(),
                                                  'charts':[signed_by_c1,signed_by_rel1, tot_diag1 ,tot_diag_thalb1, tot_diag_thala1, tot_diag_sck1, tot_diag_other1, tot_diag_mem1,
                                                            tot_diag_enz1, tot_diag_cong1,tot_diag_thalb_con_or1, tot_diag_thala_con_or1, tot_diag_sck_con_or1, tot_diag_other_con_or1,
                                                            tot_diag_mem_con_or1, tot_diag_enz_con_or1, tot_diag_cong_con_or1 , tot_diag_thalb_race1, tot_diag_thala_race1, tot_diag_sck_race1,
                                                            tot_diag_other_race1, tot_diag_mem_race1, tot_diag_enz_race1, tot_diag_cong_race1, tot_diag_thalb_age1, tot_diag_thala_age1,
                                                            tot_diag_sck_age1, tot_diag_other_age1, tot_diag_mem_age1, tot_diag_enz_age1, tot_diag_cong_age1, edu_by_age_prim1, edu_by_age_sec1,
                                                            edu_by_age_uni1, edu_by_age_oth1, employ_age_dist1, unemploy_age_dist1, penic_dist1, vacc_dist1, liver_dist1, urea_dist1, creat_dist1,
                                                            proturea_dist1,calc_dist1, parv_dist1, pulm_dist1, hip_dist1, oph_dist1, dac_dist1, stroke_dist1, splen_dist1, aplastic_dist1,
                                                            chest_dist1, mulorg_dist1, priap_dist1, hf_beta_dist1, hf_aplha_dist1, hf_sickle_dist1, hf_other_dist1, hf_membrane_dist1, hf_enzyme_dist1,
                                                            hf_cong_dist1,
                                                            pvcht, pvcht_age ]},
                              context_instance=context)

@login_required(login_url='/login')
def external_centers(request):
    context = RequestContext(request)

    if request.method == 'POST':

        #TO DO: STORE
        return render(request, 'external_centers.html')
    else:
        ext_cent = ExternalCentersForm(prefix='extcent')
        ext_cent_diagnostic = ExternalCentersDiagnosticForm(prefix='extcentDiagn')
        ext_cent_outcomes = ExternalCentersOutcomesForm(prefix='extcentOutcomes')
        ext_cent_outcomes2 = ExternalCentersOutcomes2Form(prefix='extcentOutcomesTwo')

        return render(request, 'external_centers.html', {'ext_centres': ext_cent, 'ext_centres_diag':ext_cent_diagnostic, 'ext_centres_out':ext_cent_outcomes, 'ext_centres_out2':ext_cent_outcomes2 })

def login(request):
    context = RequestContext(request)
    username = request.POST.get('username', '')
    print 'username=', username
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)
    print 'user=', user

    if user is not None:
        auth.login(request, user)
        #user = User.objects.get(username=username)
        print 'login'
        return redirect('eReg.views.modules')

    else:
        print 'no login'
        # return HttpResponseRedirect('/accounts/invalid')
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('module_2')
    response.delete_cookie('module_3')
    response.delete_cookie('module_4')
    response.delete_cookie('module_5')
    response.delete_cookie('module_6')
    return response


class IcdTenAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        #Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return icd_10.objects.none()

        qs = icd_10.objects.all()
        #
        if self.q:
             qs = qs.filter(icd_10_desc__icontains=self.q)
        #
        return qs

class OrphaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        #Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return orphaCodes.objects.none()

        qs = orphaCodes.objects.all()
        #
        if self.q:
             qs = qs.filter(orpha_desc__icontains=self.q)
        #
        return qs