from django.db.models import (
    Count,
    Max,
    Case,
    When,
    Value,
    IntegerField,
    Exists,
    OuterRef,
    F,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, DeleteView
from .models import Patient
from .forms import PatientForm
from department.models import Hospitalization


@login_required(login_url="/login/")
def index(request):
    patients = Patient.objects.annotate(
        ongoing_admissions=Exists(
            Hospitalization.objects.filter(patient=OuterRef("pk"), is_discharged=False)
        ),
        discharged_admissions=Count(
            Case(
                When(hospitalizations__is_discharged=True, then=1),
                default=Value(0),
                output_field=IntegerField(),
            )
        ),
        total_admissions=Count("hospitalizations"),
        latest_discharge_date=Max(
            Case(
                When(
                    hospitalizations__is_discharged=True,
                    then="hospitalizations__discharged_on",
                ),
                default=None,
            )
        ),
    ).order_by(
        F("ongoing_admissions").desc(),
        F("discharged_admissions").desc(),
        F("latest_discharge_date").desc(nulls_last=True),
    )

    context = {
        "patients": patients,
        "title": "Patients list",
    }
    return render(request, "patient_list.html", context)


@login_required(login_url="/login/")
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalizations = patient.hospitalizations.all()
    ongoing_admission = hospitalizations.filter(is_discharged=False).first()
    back_url = request.META.get("HTTP_REFERER", reverse("patient:index"))
    context = {
        "patient": patient,
        "hospitalizations": hospitalizations,
        "ongoing_admission": ongoing_admission,
        "title": "Patient details",
        "back_url": back_url,
    }

    return render(request, "patient_detail.html", context)


@login_required(login_url="/login/")
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
        "title": "Add Patient",
        "form": form,
    }

    return render(request, "patient_form.html", context)


@login_required(login_url="/login/")
def patient_update(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient:detail", patient.id)
    else:
        form = PatientForm(instance=patient)
    back_url = reverse("patient:detail", args=[patient.id])
    context = {
        "title": "Edit Patient",
        "form": form,
        "url" : back_url
    }
    return render(request, "patient_form.html", context)

@login_required(login_url="/login/")
def patient_delete(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    name = f"{patient.first_name} {patient.last_name}"
    if request.method == "POST":
        patient.delete()
        return redirect("patient:index")
    back_url = reverse("patient:detail", args=[patient.id])
    context= {
        "title": "Delete Patient",
        "name" : name,
        "url" : back_url,
        
    }
    return render(request, "confirm_delete.html", context)



