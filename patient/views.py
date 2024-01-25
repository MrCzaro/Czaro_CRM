from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.utils import timezone

from .models import Patient , PatientObservation
from .forms import PatientForm, PatientObservationForm

@login_required
def index(request):
    admitted_patients = Patient.objects.filter(is_discharged=False).order_by("-admitted_on")
    discharged_patients = Patient.objects.filter(is_discharged=True).order_by("-discharged_on")
    context = {
        "admitted_patients": admitted_patients,
        "discharged_patients" : discharged_patients,
        "title" : "Patients list"
        
    }
    return render(request, "patient_list.html", context)

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    context = {
        "patient": patient,
        "title": "Patient details"
    }
    
    #Discharge or readmit patient  
    if request.method == "POST":
        if request.POST.get("action") == "discharge":
            patient.is_discharged = True
            patient.discharged_on = timezone.now()
            patient.save()
        elif request.POST.get("action") == "readmit":
            patient.is_discharged = False
            patient.discharged_on = None
            patient.save()
            
        # Redirect to the same detail page after processing discharge/readmission
        return HttpResponseRedirect(reverse("patient:detail", args=[patient.id]))
    
    return render(request, "patient_detail.html", context)

@login_required   
def patient_page(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    observations = patient.observations.all()
    context = {
        "patient" : patient,
        "title" : "Patient Page",
        "observations": observations,
    }
    
    return render(request, "patient_page.html", context)

@login_required
def add_patient_observation(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    
    if request.method == "POST":
        form = PatientObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.created_by = request.user
            observation.patient = patient
            observation.save()
            return redirect("patient:page", pk=patient.id)
    else:
        
        form = PatientObservationForm()
        
    context = {
        "form" : form, 
        "title" : "Add Patient Observation",
        "patient_id" : patient.id,
    }
    
    return render(request,"patient_observation_form.html", context)

@login_required
def edit_patient_observation(request, patient_id, observation_id):
    patient = get_object_or_404(Patient, id = patient_id)
    observation = get_object_or_404(PatientObservation, id=observation_id, patient=patient)
    
    if request.method == "POST":
        form = PatientObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            return redirect("patient:page", pk=patient.id)
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