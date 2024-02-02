from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from patient.models import Patient
from .models import Visit
from .forms import VisitForm

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
    
    context = {
        "patient": patient,
        "visit": visit,
        "title": "Patient visit details"
    }
    
    #Discharge or readmit patient  
    if request.method == "POST":
        if request.POST.get("action") == "discharge":
            patient.visit.is_discharged = True
            patient.visit.discharged_on = timezone.now()
            patient.save()
        elif request.POST.get("action") == "readmit":
            patient.visit.is_discharged = False
            patient.visit.discharged_on = None
            patient.save()
            
        # Redirect to the same detail page after processing discharge/readmission
        return HttpResponseRedirect(reverse("visit:detail", args=[patient.id, visit.id]))
    
    return render(request, "visit_detail.html", context)