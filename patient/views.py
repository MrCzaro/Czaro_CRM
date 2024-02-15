

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse

from .models import Patient 
from .forms import PatientForm


@login_required(login_url = "/login/")
def index(request):
    #non_discharged_patients = Patient.objects.filter(visits__is_discharged=False).distinct().order_by("-admitted_on")
    #discharged_patients = Patient.objects.filter(visits__is_discharged=True).distinct().order_by("-discharged_on")
    patients = Patient.objects.all()
    context = {
        "patients": patients,
        #"discharged_patients" : discharged_patients,
        #"non_discharged_patients" : non_discharged_patients,
        "title" : "Patients list"
        
    }
    return render(request, "patient_list.html", context)

@login_required(login_url = "/login/")
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalizations = patient.hospitalizations.all()
    back_url = request.META.get('HTTP_REFERER', reverse("patient:index"))
    context = {
        "patient": patient,
        "hospitalizations" : hospitalizations,
        "title": "Patient details",
        "back_url" : back_url,
    }
    
    return render(request, "patient_detail.html", context)

@login_required(login_url = "/login/")
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient_form = form.save(commit=False)
            patient_form.created_by = request.user
            patient_form.save()
            return redirect("patient:index")
    else:
        form = PatientForm()
            
    context = {
        "title" : "Add Patient",
        "form": form,
    }

    return render(request, "patient_form_add.html", context)

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