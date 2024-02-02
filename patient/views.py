from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.utils import timezone
from .models import Patient , PatientObservation
from .forms import PatientForm, PatientObservationForm
from visit.models import Visit

@login_required(login_url = "/login/")
def index(request):
    non_discharged_patients = Patient.objects.filter(visits__is_discharged=False).distinct().order_by("-admitted_on")
    discharged_patients = Patient.objects.filter(visits__is_discharged=True).distinct().order_by("-discharged_on")
    patients = Patient.all()
    context = {
        "patients": patients,
        "discharged_patients" : discharged_patients,
        "non_discharged_patients" : non_discharged_patients,
        "title" : "Patients list"
        
    }
    return render(request, "patient_list.html", context)

@login_required(login_url = "/login/")
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = patient.visit.all()
    context = {
        "patient": patient,
        "visits" : visits,
        "title": "Patient details"
    }
    
    return render(request, "patient_detail.html", context)



@login_required(login_url = "/login/")
def add_patient_observation(request, patient_id, visit_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")
    
    
    patient = get_object_or_404(Patient, id=patient_id)
    visit = get_object_or_404(Visit, id=visit_id, patient=patient)
    
    if request.method == "POST":
        form = PatientObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.created_by = request.user
            observation.visit = visit
            observation.save()
            return redirect("patient:page", patient_id=patient.id)
    else:
        
        form = PatientObservationForm()
        
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
    observation = get_object_or_404(PatientObservation, id=observation_id, visit=visit)
    
    if request.method == "POST":
        form = PatientObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            return redirect("patient:page", patient_id=patient.id)
    else:
        form = PatientObservationForm(instance=observation)
        
    context = {
        "form": form,
        "title" : "Edit Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request, "patient_observation_form.html", context)
            
            
    

    
class PatientCreateView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = Patient
    form_class = PatientForm
    template_name = "patient_form_add.html"
    success_url = reverse_lazy("patient:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Patient"
        return context 
    
class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient 
    form_class = PatientForm
    template_name = "patient_form_update.html"
    success_url = reverse_lazy("patient:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Patient"
        return context 
    
    
class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = "patient_confirm_delete.html"
    success_url = reverse_lazy("patient:index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Patient"
        return context 