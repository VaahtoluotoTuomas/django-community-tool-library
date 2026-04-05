from django.shortcuts import render, get_object_or_404
from .models import Tool

def tyokalu_lista(request):
    tyokalut = Tool.objects.all().prefetch_related('manufacturers', 'tags')
    return render(request, 'tyokalut/lista.html', {'tyokalut': tyokalut})

def tyokalu_tiedot(request, tyokalu_id):
    tyokalu = get_object_or_404(Tool, id=tyokalu_id)
    return render(request, 'tyokalut/tiedot.html', {'tyokalu': tyokalu})