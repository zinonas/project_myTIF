from django.shortcuts import render, render_to_response, RequestContext, HttpResponse, get_object_or_404, redirect
import django.http
from .forms import DemographicForm, DiagnosisForm, A_b_sickle_thalForm, Redcell_enzyme_disForm, Redcell_membrane_disForm,Cong_dyseryth_anaemiaForm
from django.template import RequestContext
from django.views.generic import TemplateView
import json
from django.contrib import messages
import traceback
from django.forms.models import formset_factory
from django.forms.models import inlineformset_factory
from models import Demographic, Diagnosis, A_b_sickle_thal,Redcell_enzyme_dis, Redcell_membrane_dis, Cong_dyseryth_anaemia, icd_10
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


@login_required(login_url='/login')
def home(request):
    return render(request,'index.html')

@login_required(login_url='/login')
def input(request):

    context = RequestContext(request)

    #diagnosis option for saving purposes. In order to save only specific tables in db.
    diag_option = 0

    if request.method == 'POST':
        my_demographics = DemographicForm(request.POST, prefix="demo")
        my_diagnosis = DiagnosisForm(request.POST, prefix='diag')
        my_a_b_sickle= A_b_sickle_thalForm(request.POST,prefix='a_b_s')
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST, prefix='rc_enz')
        my_redcell_membrane= Redcell_membrane_disForm(request.POST, prefix='rc_mbr')
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST, prefix='cong_dys')

        if request.is_ajax() and 'code' in request.POST:
            with transaction.atomic():
                code = request.POST['code']
                print 'code =', code
                data = icd_10.objects.get(id=code).icd_10_code
                print 'data =', data
                return HttpResponse(data)

        if my_demographics.is_valid() and my_diagnosis.is_valid() and my_a_b_sickle.is_valid and my_redcell_enzyme.is_valid() and my_redcell_membrane.is_valid() and my_cong_dys.is_valid():

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
                dia_val= str(formfield.value())
                if (dia_val == 'b-thalassaemia syndromes' or dia_val=='a-thalassaemia syndromes' or dia_val=='Sickle cell syndromes' or dia_val=='Other haemoglobin variants'):
                    diag_option = 1
                elif (dia_val == 'Rare cell enzyme disorders'):
                    diag_option = 2
                elif (dia_val == 'Rare cell membrane disorders'):
                    diag_option = 3
                elif (dia_val == 'Congenital desyrythropoietic anaemias'):
                    diag_option = 4
                #print type(de_val)
                entry+='"fieldValue":"'+str(dia_val) + '"},'
            entry = entry[:-1]
            #entry +='],'
            #print entry
            #print diag_option
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

        # else:
        #     raise ValueError('No form specified !')
    else:
        diag_option=0
        my_demographics = DemographicForm(prefix='demo')
        my_diagnosis = DiagnosisForm(prefix='diag')
        my_a_b_sickle= A_b_sickle_thalForm(prefix='a_b_s')
        my_redcell_enzyme = Redcell_enzyme_disForm(prefix='rc_enz')
        my_redcell_membrane= Redcell_membrane_disForm(prefix='rc_mbr')
        my_cong_dys = Cong_dyseryth_anaemiaForm(prefix='cong_dys')


    return render_to_response('input.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option}, context)
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

        if 'id' in request.POST and request.POST['id']:
            with transaction.atomic():
                id = request.POST['id']
                patient = Demographic.objects.filter(patient_id__icontains=id)
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

        if (diag_val == 'b-thalassaemia syndromes' or diag_val == 'a-thalassaemia syndromes' or diag_val == 'Sickle cell syndromes' or diag_val == 'Other haemoglobin variants'):
            diag_option = 1
        elif (diag_val == 'Rare cell enzyme disorders'):
            diag_option = 2
        elif (diag_val == 'Rare cell membrane disorders'):
            diag_option = 3
        elif (diag_val == 'Congenital desyrythropoietic anaemias'):
            diag_option = 4

        my_demographics = DemographicForm(request.POST or None, prefix="demo", instance=patient)
        my_diagnosis = DiagnosisForm(request.POST or None,prefix='diag', instance=diag_patient)
        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)

        print "HERE FIRST IF"
        if my_demographics.is_valid() and my_diagnosis.is_valid() and (my_a_b_sickle.is_valid or my_redcell_enzyme.is_valid() or my_redcell_membrane.is_valid() or my_cong_dys.is_valid()):
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

        my_demographics = DemographicForm(prefix="demo",instance=patient)
        # my_demographics = DemographicForm(initial=form_data,)

        # my_demographics = DemographicForm(prefix='demo')
        my_diagnosis = DiagnosisForm(prefix='diag', instance=diag_patient)
        my_a_b_sickle= A_b_sickle_thalForm(request.POST or None,prefix='a_b_s', instance=a_b_s_patient)
        my_redcell_enzyme = Redcell_enzyme_disForm(request.POST or None, prefix='rc_enz', instance=r_c_e_patient)
        my_redcell_membrane= Redcell_membrane_disForm(request.POST or None, prefix='rc_mbr',instance=r_c_m_patient)
        my_cong_dys = Cong_dyseryth_anaemiaForm(request.POST or None, prefix='cong_dys', instance=c_d_a_patient)


    return render_to_response('results.html', {'frm':my_demographics, 'frm_d': my_diagnosis, 'frm_a_b_s': my_a_b_sickle, 'frm_rc_enz': my_redcell_enzyme, 'frm_rc_mbr': my_redcell_membrane, 'frm_cong_dys': my_cong_dys, 'diag_option': diag_option}, context)



def test(request):
    return render_to_response('test.html')


def login(request):
    context = RequestContext(request)
    username = request.POST.get('username', '')
    print 'username=', username
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)
    print 'user=', user

    if user is not None:
        auth.login(request, user)
        print 'login'
        return render_to_response('index.html', context)

    else:
        print 'no login'
        # return HttpResponseRedirect('/accounts/invalid')
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return render(request, 'login.html')