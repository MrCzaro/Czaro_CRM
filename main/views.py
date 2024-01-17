from django.shortcuts import render

from django.contrib import messages
def main(request):
    context = {
        "title": "Main Page",
    }
    messages.success(request, "Just Checking messages!")
    return render(request, "base.html", context)