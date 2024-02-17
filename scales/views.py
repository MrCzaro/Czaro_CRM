from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BodyMassIndex, NortonScale, GlasgowComaScale, NewsScale, PainScale
from .forms import (
    BodyMassIndexForm,
    NortonScaleForm,
    GlasgowComaScaleForm,
    NewsScaleForm,
    PainScaleForm,
)
from patient.models import Patient
from department.models import Hospitalization


def access_denied(request):
    return render(request, "access_denied.html")


@login_required(login_url="/login/")
def create_patient_bmi(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = BodyMassIndexForm(request.POST)
        if form.is_valid():
            bmi = form.save(commit=False)
            bmi.created_by = request.user
            bmi.hospitalization = hospitalization
            bmi.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = BodyMassIndexForm()

    context = {
        "form": form,
        "title": "Add Body Mass Index",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_patient_bmi(request, patient_id, hospitalization_id, bmi_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    bmi = get_object_or_404(BodyMassIndex, id=bmi_id, hospitalization=hospitalization)

    if request.method == "POST":
        form = BodyMassIndexForm(request.POST, instance=bmi)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = BodyMassIndexForm(instance=bmi)

    context = {
        "form": form,
        "title": "Edit Body Mass Index",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def create_glasgow_scale(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = GlasgowComaScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.hospitalization = hospitalization
            scale.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = GlasgowComaScaleForm()

    context = {
        "form": form,
        "title": "Add Glasgow Coma Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_glasgow_scale(request, patient_id, hospitalization_id, glasgow_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    glasgow = get_object_or_404(
        GlasgowComaScale, id=glasgow_id, hospitalization=hospitalization
    )

    if request.method == "POST":
        form = GlasgowComaScaleForm(request.POST, instance=glasgow)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = GlasgowComaScaleForm(instance=glasgow)

    context = {
        "form": form,
        "title": "Edit Glasgow Coma Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def create_news_scale(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = NewsScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.hospitalization = hospitalization
            scale.save()
            return redirect("department:hospitalization", hospitalization_id)
        else:
            print(form.errors)
    else:
        form = NewsScaleForm()

    context = {
        "form": form,
        "title": "Add National Early Warning Score",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_news_scale(request, patient_id, hospitalization_id, news_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    news = get_object_or_404(NewsScale, id=news_id, hospitalization=hospitalization)

    if request.method == "POST":
        form = NewsScaleForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = NewsScaleForm(instance=news)

    context = {
        "form": form,
        "title": "Add National Early Warning Score",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def create_norton_scale(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = NortonScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.hospitalization = hospitalization
            scale.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = NortonScaleForm()

    context = {
        "form": form,
        "title": "Add Norton Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_norton_scale(request, patient_id, hospitalization_id, norton_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    norton = get_object_or_404(
        NortonScale, id=norton_id, hospitalization=hospitalization
    )

    if request.method == "POST":
        form = NortonScaleForm(request.POST, instance=norton)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = NortonScaleForm(instance=norton)

    context = {
        "form": form,
        "title": "Edit Norton Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def create_pain_scale(request, patient_id, hospitalization_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )

    if request.method == "POST":
        form = PainScaleForm(request.POST)
        if form.is_valid():
            scale = form.save(commit=False)
            scale.created_by = request.user
            scale.hospitalization = hospitalization
            scale.save()
            return redirect("department:hospitalization", hospitalization_id)
    else:
        form = PainScaleForm()

    context = {
        "form": form,
        "title": "Add Pain Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)


@login_required(login_url="/login/")
def update_pain_scale(request, patient_id, hospitalization_id, pain_id):
    # Check if the user has the allowed profession
    if request.user.profession == "secretaries":
        # Redirect or show an error message
        return redirect("access_denied")

    patient = get_object_or_404(Patient, id=patient_id)
    hospitalization = get_object_or_404(
        Hospitalization, id=hospitalization_id, patient=patient
    )
    pain = get_object_or_404(PainScale, id=pain_id, hospitalization=hospitalization)

    if request.method == "POST":
        form = PainScaleForm(request.POST, instance=pain)
        if form.is_valid():
            form.save()
            return redirect("department:hospitalization", hospitalization_id)

    else:
        form = PainScaleForm(instance=pain)

    context = {
        "form": form,
        "title": "Edit Pain Scale",
        "hospitalization_id": hospitalization_id,
    }

    return render(request, "scale_form.html", context)
