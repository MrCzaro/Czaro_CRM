from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import reverse

from datetime import datetime

from .models import Department, Hospitalization, Observation, VitalSigns, Consultation
from .forms import (
    DepartmentForm,
    ObservationForm,
    HospitalizationForm,
    TransferPatientForm,
    DischargeForm,
    VitalSignsForm,
    ConsultationForm,
)
from patient.models import Patient
from scales.models import (
    BodyMassIndex,
    NortonScale,
    GlasgowComaScale,
    NewsScale,
    PainScale,
)


@login_required(login_url="/login/")
def hospitalization_detail(request, hospitalization_id):
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id)
    consultations = Consultation.objects.filter(hospitalization=hospitalization)
    bmis = BodyMassIndex.objects.filter(hospitalization=hospitalization)
    observations = Observation.objects.filter(hospitalization=hospitalization)
    norton_scales = NortonScale.objects.filter(hospitalization=hospitalization)
    glasgow_scales = GlasgowComaScale.objects.filter(hospitalization=hospitalization)
    news_scales = NewsScale.objects.filter(hospitalization=hospitalization)
    pain_scales = PainScale.objects.filter(hospitalization=hospitalization)
    vitals = VitalSigns.objects.filter(hospitalization=hospitalization)
    context = {
        "bmis": bmis,
        "consultations": consultations,
        "glasgow_scales": glasgow_scales,
        "hospitalization": hospitalization,
        "observations": observations,
        "news_scales": news_scales,
        "norton_scales": norton_scales,
        "pain_scales": pain_scales,
        "vitals": vitals,
        "title": "Hospitalization Detail",
        "back_url": reverse("patient:detail", args=[hospitalization.patient.id]),
    }

    return render(request, "hospitalization_detail.html", context)


@login_required(login_url="/login/")
def admit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":
        form = HospitalizationForm(request.POST)
        if form.is_valid():
            hospitalization = form.save(commit=False)
            department_id = request.POST.get("department_id")
            department = get_object_or_404(Department, id=department_id)
            hospitalization.patient = patient
            hospitalization.department = department
            hospitalization.save()
            return redirect("department:department_detail", department_id)
    else:
        form = HospitalizationForm()

    departments = Department.objects.all()

    context = {
        "departments": departments,
        "form": form,
        "title": f"Admit {patient.first_name} {patient.last_name}",
        "patient": patient,
    }

    return render(request, "admit_patient.html", context)


@login_required(login_url="/login/")
def edit_patient_symptoms(request, hospitalization_id, patient_id):
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient_id=patient_id
    )
    patient = hospitalization.patient

    department_id = (
        hospitalization.department.id if hospitalization.department else None
    )

    if request.method == "POST":
        print(request.method)
        form = HospitalizationForm(request.POST, instance=hospitalization)
        if form.is_valid():
            hospitalization = form.save(commit=False)
            hospitalization.department = hospitalization.department

            hospitalization.save()
            return redirect(
                "department:department_detail", hospitalization.department.id
            )
    else:
        form = HospitalizationForm(
            instance=hospitalization, initial={"department_id": department_id}
        )

    context = {
        "department_id": department_id,
        "form": form,
        "title": f"Edit Symptoms for {patient.first_name} {patient.last_name}",
        "patient": patient,
        "hospitalization_id": hospitalization.id,
    }

    return render(request, "edit_patient_admission.html", context)


@login_required(login_url="/login/")
def transfer_patient(request, patient_id, hospitalization_id):
    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = TransferPatientForm(request.POST)
        if form.is_valid():
            new_department = form.cleaned_data["department"]
            hospitalization.department = new_department
            hospitalization.save()
            return redirect("department:department_detail", new_department.id)
    else:
        form = TransferPatientForm()

    context = {
        "form": form,
        "title": "Transfer Patient",
        "patient": patient,
        "hospitalization": hospitalization,
        "departments": Department.objects.all(),
    }

    return render(request, "transfer_patient.html", context)


@login_required(login_url="/login/")
def discharge_patient(request, hospitalization_id):
    hospitalization = get_object_or_404(Hospitalization, id=hospitalization_id)

    if request.method == "POST":
        form = DischargeForm(request.POST)
        if form.is_valid():
            discharge_date = form.cleaned_data["discharge_date"]
            discharge_time = form.cleaned_data["discharge_time"]
            discharge_datetime = datetime.combine(discharge_date, discharge_time)
            hospitalization.dicharged_on = discharge_datetime
            hospitalization.is_discharged = True
            hospitalization.save()
            return redirect(
                "department:department_detail", hospitalization.department.id
            )
    else:

        # Set default values for date and time
        default_discharge_date = timezone.now().strftime("%Y-%m-%d")
        default_discharge_time = timezone.now().strftime("%H:%M")
        form = DischargeForm()
        context = {
            "form": form,
            "title": "Discharge Patient",
            "hospitalization": hospitalization,
            "default_discharge_date": default_discharge_date,
            "default_discharge_time": default_discharge_time,
        }

    return render(request, "discharge_patient.html", context)


@login_required(login_url="/login/")
def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    hospitalizations = Hospitalization.objects.filter(
        department__id=department_id, is_discharged=False
    )
    num_admitted_patients = hospitalizations.count()

    context = {
        "department": department,
        "hospitalizations": hospitalizations,
        "num_admitted_patients": num_admitted_patients,
        "title": "Department Detail",
    }

    return render(request, "department_detail.html", context)


@login_required(login_url="/login/")
def create_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect("department:department_list") 
    else:
        form = DepartmentForm()

    context = {
        "form": form,
        "title": "Create Department",
    }

    return render(request, "create_department.html", context)


@login_required(login_url="/login/")
def department_list(request):
    departments = Department.objects.all()
    # Count the total number of admitted patients
    total_admitted_patients = Hospitalization.objects.filter(
        is_discharged=False
    ).count()
    # Count the number of patients admitted in each department
    department_counts = (
        {}
    )  

    for department in departments:
        department_count = Hospitalization.objects.filter(
            department=department, is_discharged=False
        ).count()
        setattr(department, "count", department_count)

        department_counts[department.id] = department_count

    context = {
        "title": "Department List",
        "departments": departments,
        "department_counts": department_counts,
        "total_admitted_patients": total_admitted_patients,
    }
    return render(request, "department_list.html", context)


@login_required(login_url="/login/")
def create_patient_consultation(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession in ["secretaries", "nurses"]:
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.created_by = request.user
            consultation.hospitalization = hospitalization
            consultation.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = ConsultationForm()

    context = {
        "form": form,
        "title": "Add Patient Consultation",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "patient_consultation_form.html", context)


@login_required(login_url="/login/")
def update_patient_consultation(
    request, patient_id, hospitalization_id, consultation_id
):
    # Check if the user has the allowed profession
    if request.user.profession in ["secretaries", "nurses"]:
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    consultation = get_object_or_404(
        Consultation, id=consultation_id, hospitalization=hospitalization
    )

    if request.method == "POST":
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = ConsultationForm(instance=consultation)

    context = {
        "form": form,
        "title": "Edit Patient Consultation",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "patient_consultation_form.html", context)


@login_required(login_url="/login/")
def create_patient_observation(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.created_by = request.user
            observation.hospitalization = hospitalization
            observation.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:

        form = ObservationForm()

    context = {
        "form": form,
        "title": "Add Patient Observation",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "patient_observation_form.html", context)


@login_required(login_url="/login/")
def update_patient_observation(request, patient_id, hospitalization_id, observation_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    observation = get_object_or_404(
        Observation, id=observation_id, hospitalization=hospitalization
    )

    if request.method == "POST":
        form = ObservationForm(request.POST, instance=observation)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:
        form = ObservationForm(instance=observation)

    context = {
        "form": form,
        "title": "Edit Patient Observation",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "patient_observation_form.html", context)


@login_required(login_url="/login/")
def create_vital_signs(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.created_by = request.user
            vital.hospitalization = hospitalization
            vital.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:

        form = VitalSignsForm()

    context = {
        "form": form,
        "title": "Add Vital Signs",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_vital_signs(request, patient_id, hospitalization_id, vital_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    vital = get_object_or_404(VitalSigns, id=vital_id, hospitalization=hospitalization)

    if request.method == "POST":
        form = VitalSignsForm(request.POST, instance=vital)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization.id)
    else:
        form = VitalSignsForm(instance=vital)

    context = {
        "form": form,
        "title": "Edit Vital Signs",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)
