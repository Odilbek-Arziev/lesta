from django.shortcuts import render, redirect
from .models import UploadedFile
from .utils import process_text


def index(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        UploadedFile.objects.create(file=file)
        return redirect("app:table")

    return render(request, "index.html", {})


def table(request):
    document = UploadedFile.objects.last()

    with open(document.file.path, "r", encoding="utf-8") as f:
        text = f.read()
        words = process_text(text)
    return render(request, "table.html", {"words": words})
