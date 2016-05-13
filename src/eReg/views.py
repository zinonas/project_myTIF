from django.db.models import Sum, Count
from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, get_object_or_404, redirect
import django.http
from .forms import DemographicForm, DiagnosisForm, A_b_sickle_thalForm, Redcell_enzyme_disForm, Redcell_membrane_disForm,Cong_dyseryth_anaemiaForm, UserCreationForm, ClinicalDataForm, ClinicalDataTwo, ExternalCentersForm,ExternalCentersDiagnosticForm,ExternalCentersOutcomesForm, ExternalCentersOutcomes2Form
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
from models import Demographic, Diagnosis, A_b_sickle_thal,Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10, Clinical_data, Clinical_data_two, Ext_centers
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


@login_required(login_url='/login')
def home(request):
    return render(request,'index.html')

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

        print my_demographics.is_valid()
        print my_diagnosis.is_valid()
        print my_a_b_sickle.is_valid()
        print my_redcell_enzyme.is_valid()
        print my_redcell_membrane.is_valid()
        print my_cong_dys.is_valid()
        print my_cln_dt.is_valid()
        print my_cln_dt_two.is_valid()

        if request.is_ajax() and 'code' in request.POST:
            with transaction.atomic():
                code = request.POST['code']
                print 'code =', code
                data = icd_10.objects.get(id=code).icd_10_code
                print 'data =', data
                return HttpResponse(data)

        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_a_b_sickle.is_valid and my_redcell_enzyme.is_valid() and my_redcell_membrane.is_valid() and my_cong_dys.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid():

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
                #print formfield.id_for_label
                entry+='{"fieldName":"'+ str(dia_id) + '",'
                print "HERE I HAVE dia_val=", formfield.value()
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

    #if ret is None:
    #    ret = render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_out_mes': my_out_mes, 'frm_life_ev': my_life_ev,}, context)
    #    cache.set('input-rendered', ret)

    return render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_cln_dt_two': my_cln_dt_two}, context)
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
                return render(request, 'search.html',
                    {'patient': patient, 'query': id, 'option':value})

    # if request.is_ajax() and request.method == "POST":
    #     myid= request.POST.get("sentence","")
    #     #response_data=fil(sentence)
    #     print myid
    #     patient = Demographic.objects.select_for_update().filter(patient_id = myid)
    #     data = serializers.serialize('json', patient)
    #     json_data = json.loads(data)[0]
    #     form_data = json_data['fields']
    #     print form_data
    #     my_demographics = DemographicForm(initial=form_data)
    #     print my_demographics
    #     # new_d = serializers.deserialize("json", data)
    #     # print new_d
    #     # myp = Demographic.objects.raw('SELECT * from `eReg_demographic`')
    #     # for p in myp:
    #     #     print p
    #     # my_data = json.loads(data)
    #
    #     for pat in patient:
    #         print pat.given_name

        return redirect('results.html', {'frm':my_demographics, 'option': value}, context)
    else:
        return render_to_response('search.html', {'option': value}, context)

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
            patient = Demographic.objects.get(patient_id=myid)
            diag_patient = Diagnosis.objects.get(patient=myid)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
            cln_dt_patient= Clinical_data.objects.get(patient=myid)



        if (diag_val == 'b-thalassaemia syndromes' or diag_val == 'a-thalassaemia syndromes' or diag_val == 'Sickle cell syndromes' or diag_val == 'Other haemoglobin variants'):
            diag_option = 1
        elif (diag_val == 'Rare cell enzyme disorders'):
            diag_option = 2
        elif (diag_val == 'Rare cell membrane disorders'):
            diag_option = 3
        elif (diag_val == 'Congenital desyrythropoietic anaemias'):
            diag_option = 4
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Rare cell enzyme disorders' in diag_val):
            diag_option = 12
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Rare cell membrane disorders' in diag_val):
            diag_option = 13
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = 14
        elif('Rare cell enzyme disorders' in diag_val and 'Rare cell membrane disorders' in diag_val):
            diag_option = 23
        elif('Rare cell enzyme disorders' in diag_val and 'Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = 24
        elif('Rare cell membrane disorders' in diag_val and 'Congenital desyrythropoietic anaemias' in diag_val):
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


        print "HERE FIRST IF"
        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_cln_dt.is_valid() and (my_a_b_sickle.is_valid or my_redcell_enzyme.is_valid() or my_redcell_membrane.is_valid() or my_cong_dys.is_valid()):
            print "HERE SECOND IF"

            my_demographics_object = my_demographics.save()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()

            my_a_b_sickle_object = my_a_b_sickle.save(commit=False)
            my_a_b_sickle_object.patient = my_demographics_object
            my_a_b_sickle_object.save()

            my_redcell_enzyme_object = my_redcell_enzyme.save(commit=False)
            my_redcell_enzyme_object.patient = my_demographics_object
            my_redcell_enzyme_object.save()

            my_redcell_membrane_object = my_redcell_membrane.save(commit=False)
            my_redcell_membrane_object.patient = my_demographics_object
            my_redcell_membrane_object.save()

            my_cong_dys_object = my_cong_dys.save(commit=False)
            my_cong_dys_object.patient = my_demographics_object
            my_cong_dys_object.save()

            my_cln_dt_object = my_cln_dt.save(commit=False)
            my_cln_dt_object.patient = my_demographics_object
            my_cln_dt_object.save()




    else:
        diag_option=0
        with transaction.atomic():
            print "HERE ELSE"
            patient = Demographic.objects.get(patient_id=myid)
            diag_patient = Diagnosis.objects.get(patient=myid)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
            cln_dt_patient= Clinical_data.objects.get(patient=myid)


            str_diag_val =ast.literal_eval(diag_val)
            #print "diagnosis value=", str_diag_val[0], " ", str_diag_val[1]
        #     data = serializers.serialize('json', patient)
        #     diag_data = serializers.serialize('json', diag_patient)
        #
        #     json_data = json.loads(data)[0]
        #     json_diag_data = json.loads(diag_data)[0]
        #
        #     # print "here", json_data
        #     form_data = json_data['fields']
        #     form_diag_data = json_diag_data['fields']
        #     diag_val= form_diag_data['diagnosis_option']
        #     form_data['patient_id'] = myid
        # # print form_data
        # #
        if (diag_val == 'b-thalassaemia syndromes' or diag_val == 'a-thalassaemia syndromes' or diag_val == 'Sickle cell syndromes' or diag_val == 'Other haemoglobin variants'):
            diag_option = 1
        elif (diag_val == 'Rare cell enzyme disorders'):
            diag_option = 2
        elif (diag_val == 'Rare cell membrane disorders'):
            diag_option = 3
        elif (diag_val == 'Congenital desyrythropoietic anaemias'):
            diag_option = 4
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Rare cell enzyme disorders' in diag_val):
            diag_option = 12
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Rare cell membrane disorders' in diag_val):
            diag_option = 13
        elif(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val) and 'Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = 14
        elif('Rare cell enzyme disorders' in diag_val and 'Rare cell membrane disorders' in diag_val):
            diag_option = 23
        elif('Rare cell enzyme disorders' in diag_val and 'Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = 24
        elif('Rare cell membrane disorders' in diag_val and 'Congenital desyrythropoietic anaemias' in diag_val):
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


    return render_to_response('results.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt':my_cln_dt}, context)


@login_required(login_url='/login')
def search_patient_card(request):
    context = RequestContext(request)
    value=0
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
                patient = Demographic.objects.filter(patient_id__icontains=id)
                print patient
                print patient.count()
                # books = Book.objects.filter(title__icontains=q)
                return render(request, 'search_patient_card.html',
                    {'patient': patient, 'query': id, 'option':value})

    # if request.is_ajax() and request.method == "POST":
    #     myid= request.POST.get("sentence","")
    #     #response_data=fil(sentence)
    #     print myid
    #     patient = Demographic.objects.select_for_update().filter(patient_id = myid)
    #     data = serializers.serialize('json', patient)
    #     json_data = json.loads(data)[0]
    #     form_data = json_data['fields']
    #     print form_data
    #     my_demographics = DemographicForm(initial=form_data)
    #     print my_demographics
    #     # new_d = serializers.deserialize("json", data)
    #     # print new_d
    #     # myp = Demographic.objects.raw('SELECT * from `eReg_demographic`')
    #     # for p in myp:
    #     #     print p
    #     # my_data = json.loads(data)
    #
    #     for pat in patient:
    #         print pat.given_name

        return redirect('results_patient_card.html', {'frm':my_demographics, 'option': value}, context)
    else:
        return render_to_response('search_patient_card.html', {'option': value}, context)


@login_required(login_url='/login')
def results_patient_card(request):

    context = RequestContext(request)
    myid = request.GET.get('id', '')
    #diagnosis option for saving purposes. In order to save only specific tables in db.
    diag_option = ''
    print "my id", myid
    if request.method == 'POST':
        with transaction.atomic():
            print "HERE ELSE"
            patient = Demographic.objects.get(patient_id=myid)
            diag_patient = Diagnosis.objects.get(patient=myid)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
            cln_dt_patient= Clinical_data.objects.get(patient=myid)
            cln_dt_two_patient = Clinical_data_two.objects.get(patient=myid)

        # if (diag_val == 'b-thalassaemia syndromes' or diag_val == 'a-thalassaemia syndromes' or diag_val == 'Sickle cell syndromes' or diag_val == 'Other haemoglobin variants'):
        #     diag_option = ='1'
        # elif (diag_val == 'Rare cell enzyme disorders'):
        #     diag_option = 2
        # elif (diag_val == 'Rare cell membrane disorders'):
        #     diag_option = 3
        # elif (diag_val == 'Congenital desyrythropoietic anaemias'):
        #     diag_option = 4
        if(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val)):
            diag_option = diag_option +'1'
        if('Rare cell enzyme disorders' in diag_val):
            diag_option = diag_option +'2'
        if('Rare cell membrane' in diag_val):
            diag_option = diag_option +'3'
        if('Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = diag_option +'4'


        my_demographics = DemographicForm(request.POST or None, prefix="demo", instance=patient)
        my_diagnosis = DiagnosisForm(request.POST or None,prefix='diag', instance=diag_patient)
        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
        my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
        my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)

        print "HERE FIRST IF"
        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_cln_dt.is_valid() and my_cln_dt_two.is_valid()  and (my_a_b_sickle.is_valid or my_redcell_enzyme.is_valid() or my_redcell_membrane.is_valid() or my_cong_dys.is_valid()):
            print "HERE SECOND IF"
            print my_demographics.given_name
            my_demographics_object = my_demographics.save()

            my_diagnosis_object = my_diagnosis.save(commit=False)
            my_diagnosis_object.patient = my_demographics_object
            my_diagnosis_object.save()

            my_a_b_sickle_object = my_a_b_sickle.save(commit=False)
            my_a_b_sickle_object.patient = my_demographics_object
            my_a_b_sickle_object.save()

            my_redcell_enzyme_object = my_redcell_enzyme.save(commit=False)
            my_redcell_enzyme_object.patient = my_demographics_object
            my_redcell_enzyme_object.save()

            my_redcell_membrane_object = my_redcell_membrane.save(commit=False)
            my_redcell_membrane_object.patient = my_demographics_object
            my_redcell_membrane_object.save()

            my_cong_dys_object = my_cong_dys.save(commit=False)
            my_cong_dys_object.patient = my_demographics_object
            my_cong_dys_object.save()

            my_cln_dt_object = my_cln_dt.save(commit=False)
            my_cln_dt_object.patient = my_demographics_object
            my_cln_dt_object.save()



    else:
        diag_option=''
        with transaction.atomic():
            print "HERE ELSE"
            patient = Demographic.objects.get(patient_id=myid)
            diag_patient = Diagnosis.objects.get(patient=myid)
            diag_val = diag_patient.diagnosis_option
            a_b_s_patient = A_b_sickle_thal.objects.get(patient=myid)
            r_c_e_patient = Redcell_enzyme_dis.objects.get(patient=myid)
            r_c_m_patient = Redcell_membrane_dis.objects.get(patient=myid)
            c_d_a_patient = Cong_dyseryth_anaemia.objects.get(patient=myid)
            cln_dt_patient=Clinical_data.objects.get(patient=myid)
            cln_dt_two_patient=Clinical_data_two.objects.get(patient=myid)

            sum_card_one=OrderedDict()
            sum_card_one['Demographics']= 'title'
            sum_card_one[patient._meta.get_field('given_name').verbose_name.title()]= patient.given_name
            sum_card_one[patient._meta.get_field('surname').verbose_name.title()]= patient.surname
            sum_card_one[patient._meta.get_field('patient_id').verbose_name.title()]=patient.patient_id
            sum_card_one[patient._meta.get_field('national_health_care_pat_id').verbose_name.title()]=patient.national_health_care_pat_id
            sum_card_one[patient._meta.get_field('date_of_birth').verbose_name.title()]=patient.date_of_birth
            #sum_card_one[patient._meta.get_field('blood_group').verbose_name.title()]= patient.blood_group
            sum_card_one['Diagnosis']= 'title'
            #sum_card_one[diag_patient._meta.get_field('diagnosis_option').verbose_name.title()]= diag_patient.diagnosis_option


            str_diag_val =ast.literal_eval(diag_val)

            for x in range(0, len(str_diag_val)):
                #print "diagnosis value=", str_diag_val[x]
                new_string = 'Diagnosis option ' + str(x+1)
                sum_card_one[new_string]= str_diag_val[x]
            print sum_card_one['Diagnosis option 1']
            if "thal" in diag_patient.diagnosis_option:
                sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_a_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_a_gene
                sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_b_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_b_gene
                sum_card_one[a_b_s_patient._meta.get_field('mol_diag_b_thal_seq_anal_g_gene').verbose_name.title()]=a_b_s_patient.mol_diag_b_thal_seq_anal_g_gene
            sum_card_one[diag_patient._meta.get_field('diagnosis_circumstances').verbose_name.title()]=diag_patient.diagnosis_circumstances
            sum_card_one[diag_patient._meta.get_field('diagnosis_circumstances_date').verbose_name.title()]=diag_patient.diagnosis_circumstances_date

            # sum_card_one = { patient._meta.get_field('given_name').verbose_name.title():patient.given_name,
            #                  patient._meta.get_field('surname').verbose_name.title():patient.surname,
            #                  patient._meta.get_field('national_health_care_pat_id').verbose_name.title():patient.national_health_care_pat_id,
            #                  patient._meta.get_field('patient_id').verbose_name.title():patient.patient_id,
            #                  patient._meta.get_field('date_of_birth').verbose_name.title():patient.date_of_birth,
            #                  diag_patient._meta.get_field('diagnosis_option').verbose_name.title(): diag_patient.diagnosis_option
            # }

            print type(sum_card_one)
            formOne = UserCreationForm(request.POST or None, extra=sum_card_one, initial=sum_card_one)
        #     data = serializers.serialize('json', patient)
        #     diag_data = serializers.serialize('json', diag_patient)
        #
        #     json_data = json.loads(data)[0]
        #     json_diag_data = json.loads(diag_data)[0]
        #
        #     # print "here", json_data
        #     form_data = json_data['fields']
        #     form_diag_data = json_diag_data['fields']
        #     diag_val= form_diag_data['diagnosis_option']
        #     form_data['patient_id'] = myid
        # # print form_data
        # #
        if(('b-thalassaemia syndromes' in diag_val or 'a-thalassaemia syndromes' in diag_val or 'Sickle cell syndromes' in diag_val or 'Other haemoglobin variants' in diag_val)):
            diag_option = diag_option +'1'
        if('Rare cell enzyme disorders' in diag_val):
            diag_option = diag_option +'2'
        if('Rare cell membrane' in diag_val):
            diag_option = diag_option +'3'
        if('Congenital desyrythropoietic anaemias' in diag_val):
            diag_option = diag_option +'4'
        my_demographics = DemographicForm(prefix="demo",instance=patient)
        # my_demographics = DemographicForm(initial=form_data,)

        # my_demographics = DemographicForm(prefix='demo')
        my_diagnosis = DiagnosisForm(prefix='diag', instance=diag_patient)
        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)
        my_cln_dt = ClinicalDataForm(request.POST or None, prefix='cln_dt', instance=cln_dt_patient)
        my_cln_dt_two = ClinicalDataTwo(request.POST or None, prefix='cln_dt_two', instance=cln_dt_two_patient)


    return render_to_response('results_patient_card.html', {'frm':formOne, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option, 'frm_cln_dt': my_cln_dt, 'frm_cln_dt_two': my_cln_dt_two}, context)



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

    return render_to_response('statistics.html', {'total_num': total_num.count(),'females': females.count(), 'males': males.count(), 'age_values': freq_age_dist.keys(),'age_freq':freq_age_dist.values(),'charts':[pvcht, pvcht_age]}, context)

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
        return redirect('eReg.views.home')

    else:
        print 'no login'
        # return HttpResponseRedirect('/accounts/invalid')
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')