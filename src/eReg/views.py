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
from models import Demographic, Diagnosis, A_b_sickle_thal,Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, Clinical_data, Clinical_data_two, Ext_centers,Patient_reported_outcome, DiagnosisOption
from django.core import serializers
import json
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import unicodedata
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import auth
from django.contrib.auth import logout
import autocomplete_light
autocomplete_light.autodiscover()
from django.core.cache import cache
from datetime import date
from django.utils import formats
import collections
from chartit import PivotDataPool, PivotChart
import ast
from django.db.models import Q
import collections

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
        response = redirect('home')
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
            my_demographics_object.save()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.author = request.user
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()

            for x in xrange(0, len(dig_opt_list)):
                my_diagnosis_object.diagnosis_option.add(dig_opt_list[x])




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

    #if ret is None:
    #    ret = render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_out_mes': my_out_mes, 'frm_life_ev': my_life_ev,}, context)
    #    cache.set('input-rendered', ret)

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
                patient = Demographic.objects.filter(patient_id__icontains=id, author=request.user)
                print patient
                print patient.count()
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
                patient = Demographic.objects.get(patient_id=myid, author=request.user)
            except Demographic.DoesNotExist:
                patient = None
            if patient == None:
                my_alert = "1"
                return render_to_response('search.html',{'my_alert':my_alert}, context)

            diag_patient = Diagnosis.objects.get(patient=myid, author=request.user)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid, author=request.user)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid, author=request.user)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid, author=request.user)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid, author=request.user)
            cln_dt_patient= Clinical_data.objects.get(patient=myid, author=request.user)
            cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid, author=request.user)
            patient_reported_outcomes_patient = Patient_reported_outcome.objects.get(patient=myid, author=request.user)





        if ('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) :
            diag_option = 1
        elif ('Rare cell enzyme disorders' in diag_val.all()):
            diag_option = 2
        elif ('Rare cell membrane disorders' in diag_val.all()):
            diag_option = 3
        elif ('Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 4
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Rare cell enzyme disorders' in diag_val.all()):
            diag_option = 12
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Rare cell membrane disorders' in diag_val.all()):
            diag_option = 13
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 14
        elif('Rare cell enzyme disorders' in diag_val.all() and 'Rare cell membrane disorders' in diag_val.all()):
            diag_option = 23
        elif('Rare cell enzyme disorders' in diag_val.all() and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 24
        elif('Rare cell membrane disorders' in diag_val.all() and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 34

        my_demographics = DemographicForm(request.POST or None, prefix="demo", instance=patient)
        my_diagnosis = DiagnosisForm(request.POST or None,prefix='diag', instance=diag_patient)
        my_diagnosis.diagnosis_option = diag_val
        print "VALUE=", diag_val
        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
        my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
        my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)
        my_patient_reported_outcomes = Patient_Reported_outcomeForm(request.POST or None, prefix='pat_rep_out', instance=patient_reported_outcomes_patient)

        for formfield in my_diagnosis:
            if formfield.name == 'diagnosis_option':
                dig_opt_list =  formfield.value()
        #print "dig_opt_list"
        #print dig_opt_list


        #print "HERE FIRST IF"
        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_a_b_sickle.is_valid and my_redcell_enzyme.is_valid() and my_redcell_membrane.is_valid() and my_cong_dys.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid() and my_patient_reported_outcomes.is_valid():


            #print "HERE SECOND IF"

            my_demographics_object = my_demographics.save(commit=False)
            my_demographics_object.author = request.user
            my_demographics_object.save()

            mylist = my_diagnosis.diagnosis_option.all()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.author = request.user
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()


            x = mylist.values('id')
            db_diag_values = [int(y['id']) for y in x]
            dig_opt_list_values=[]
            for d in xrange (0, len(dig_opt_list)):
                dig_opt_list_values.append(int(dig_opt_list[d]))
            #print "db_diag_values"
            print db_diag_values


            #If a new diagnosis option in not in DB for user, add it
            for x in xrange(0, len(dig_opt_list_values)):
                if int(dig_opt_list_values[x]) not in db_diag_values:
                    my_diagnosis_object.diagnosis_option.add(dig_opt_list_values[x])

            #If remove a diagnosis, remove it from DB
            for y in xrange(0, len(db_diag_values)):
                if db_diag_values[y] not in dig_opt_list_values:
                    my_diagnosis_object.diagnosis_option.remove(db_diag_values[y])





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
                patient = Demographic.objects.get(patient_id=myid, author=request.user)
            except Demographic.DoesNotExist:
                patient = None
            if patient == None:
                my_alert = "1"
                response = redirect('search')
                response.set_cookie('no_patient', 'True')
                return response

            diag_patient = Diagnosis.objects.get(patient=myid, author=request.user)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid, author=request.user)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid,author=request.user)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid, author=request.user)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid, author=request.user)
            cln_dt_patient= Clinical_data.objects.get(patient=myid, author=request.user)
            cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid)
            patient_reported_outcomes_patient = Patient_reported_outcome.objects.get(patient=myid,author=request.user)

            # print "diag_val"
            # for diag_opt in diag_val.all():
            #     print diag_opt


        if ('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) :
            diag_option = 1
        elif ('Rare cell enzyme disorders' in diag_val.all()):
            diag_option = 2
        elif ('Rare cell membrane disorders' in diag_val.all()):
            diag_option = 3
        elif ('Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 4
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Rare cell enzyme disorders' in diag_val.all()):
            diag_option = 12
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Rare cell membrane disorders' in diag_val.all()):
            diag_option = 13
        elif(('b-thalassaemia syndromes' in diag_val.all() or 'a-thalassaemia syndromes' in diag_val.all() or 'Sickle cell syndromes' in diag_val.all() or 'Other haemoglobin variants' in diag_val.all()) and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 14
        elif('Rare cell enzyme disorders' in diag_val.all() and 'Rare cell membrane disorders' in diag_val.all()):
            diag_option = 23
        elif('Rare cell enzyme disorders' in diag_val.all() and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 24
        elif('Rare cell membrane disorders' in diag_val.all() and 'Congenital desyrythropoietic anaemias' in diag_val.all()):
            diag_option = 34

        print "diag_option=", diag_option
        my_demographics = DemographicForm(prefix="demo",instance=patient)
        # my_demographics = DemographicForm(initial=form_data,)

        # my_demographics = DemographicForm(prefix='demo')

        my_diagnosis = DiagnosisForm(prefix='diag', instance=diag_patient)
        my_diagnosis.diagnosis_option = diag_val
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
    print "FREQ:", freq_age_dist

    print 'total count', total_num.count()
    print 'females', females.count()
    print 'males', males.count()
    print 'birthdays', age_dist
    print "COUNT:", Count(age_dist)

    age_dict={}
    for i in freq_age_dist:
        age_dict[str(i)+'i']=freq_age_dist[i]
    print "DICT", age_dict

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
                                                            tot_diag_sck_age1, tot_diag_other_age1, tot_diag_mem_age1, tot_diag_enz_age1, tot_diag_cong_age1,
                                                            pvcht, pvcht_age ]},
                              context)

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
    return response