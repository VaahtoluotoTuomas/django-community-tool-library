from django.shortcuts import render
from .models import Tool

def tyokalu_lista(request):
    tyokalut = Tool.objects.all().prefetch_related('manufacturers', 'tags')
    return render(request, 'tyokalut/lista.html', {'tyokalut': tyokalut})
