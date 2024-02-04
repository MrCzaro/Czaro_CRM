from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from patient.models import Patient
from .models import Visit, Observation
from .forms import VisitForm, ObservationForm

@login_required(login_url = "/login/")
def create_visit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            return redirect("patient:detail", patient_id=patient.id)
    else:
        form = VisitForm()
        
    context = {
        "patient" : patient,
        "form" : form,
        "title" : "Add Visit",
    }
    
    return render(request, "visit_form.html", context)

@login_required(login_url = "/login/")
def update_visit(request, patient_id, visit_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    
    if request.method =="POST":
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect("patient:detail", patient_id=patient.id)
    else:
        form = VisitForm(instance=visit)
            
    context = {
        "patient" : patient,
        "form" : form,
        "title" : "Edit Visit",
    }
            
    return render(request, "visit_form.html", context)

@login_required(login_url = "/login/")
def visit_detail(request, patient_id, visit_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
   
    observations = visit.observations.all()
    norton_scales = visit.norton.all()
    glasgow_scales = visit.glasgow.all()
    news_scales = visit.news.all()
    
    context = {
        "patient": patient,
        "visit": visit,
        "title": "Patient visit details",
        "observations": observations,
        "norton_scales": norton_scales,
        "glasgow_scales": glasgow_scales,
        "news_scales": news_scales,
    }
    # Discharge or readmit patient  
    if request.method == "POST":
        if request.POST.get("action") == "discharge":
            visit.is_discharged = True
            visit.discharged_on = timezone.now()
            visit.save()
        elif request.POST.get("action") == "readmit":
            visit.is_discharged = False
            visit.discharged_on = None
            visit.save()
            
        # Redirect to the same detail page after processing discharge/readmission
        return HttpResponseRedirect(reverse("visit:detail", args=[patient.id, visit.id]))
    
    return render(request, "visit_detail.html", context)

@login_required(login_url = "/login/")
def add_patient_observation(request, patient_id, visit_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")
    
    
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    
    if request.method == "POST":
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.created_by = request.user
            observation.visit = visit
            observation.save()
            return redirect("patient:page", patient_id=patient.id)
    else:
        
        form = ObservationForm()
        
    context = {
        "form" : form, 
        "title" : "Add Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request,"patient_observation_form.html", context)

@login_required(login_url = "/login/")
def edit_patient_observation(request, patient_id, visit_id, observation_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")
    
    patient = get_object_or_404(Patient, id = patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    observation = get_object_or_404(Observation, id=observation_id, visit=visit)
    
    if request.method == "POST":
        form = ObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            return redirect("patient:page", patient_id=patient.id)
    else:
        form = ObservationForm(instance=observation)
        
    context = {
        "form": form,
        "title" : "Edit Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request, "patient_observation_form.html", context)