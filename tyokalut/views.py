from django.shortcuts import render, get_object_or_404
from .models import Tool
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def tyokalu_lista(request):
    tyokalut = Tool.objects.all().prefetch_related('manufacturers', 'tags')
    return render(request, 'tyokalut/lista.html', {'tyokalut': tyokalut})

def tyokalu_tiedot(request, tyokalu_id):
    tyokalu = get_object_or_404(Tool, id=tyokalu_id)
    return render(request, 'tyokalut/tiedot.html', {'tyokalu': tyokalu})

def rekisteroidy(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tyokalu_lista')
    else:
            form = UserCreationForm()
        
    return render(request, 'tyokalut/rekisteroidy.html', {'form': form})