from django.shortcuts import render, get_object_or_404
from .models import Tool, Loan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

def tyokalu_lista(request):
    tyokalut = Tool.objects.all().prefetch_related('manufacturers', 'tags')
    return render(request, 'tyokalut/lista.html', {'tyokalut': tyokalut})

def tyokalu_tiedot(request, tyokalu_id):
    tyokalu = get_object_or_404(Tool, id=tyokalu_id)

    aktiivinen_laina = Loan.objects.filter(tool=tyokalu, returned_at__isnull=True).first()

    on_vapaana = aktiivinen_laina is None

    context = {
        'tyokalu': tyokalu,
        'on_vapaana': on_vapaana,
        'aktiivinen_laina': aktiivinen_laina
        }

    return render(request, 'tyokalut/tiedot.html', context)

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

@login_required
def lainaa_tyokalu(request, tyokalu_id):
    if request.method == 'POST':
        tyokalu = get_object_or_404(Tool, id=tyokalu_id)

        onko_lainassa = Loan.objects.filter(tool=tyokalu, returned_at__isnull=True).exists()

        if not onko_lainassa:
            erapaiva = timezone.now() + timedelta(days=14)

            Loan.objects.create(
                user=request.user,
                tool=tyokalu,
                due_date=erapaiva
            )
            messages.success(request, f'Työkalu "{tyokalu.name}" lainattu! Löydät sen Omat lainat -sivulta.')
        
        else:
            messages.error(request, 'Pahoittelut, työkalu ehti juuri mennä toiselle lainaajalle.')
        
        return redirect('tyokalu_tiedot', tyokalu_id=tyokalu.id)
    
    return redirect('tyokalu_lista')

@login_required
def palauta_tyokalu(request, laina_id):
    if request.method == 'POST':
        laina = get_object_or_404(Loan, id=laina_id, user=request.user)

        if not laina.returned_at:
             laina.returned_at = timezone.now()
             laina.save()
             messages.success(request, f'Työkalu "{laina.tool.name}" palautettu onnistuneesti.')
    return redirect('omat_lainat')
    

@login_required
def omat_lainat(request):
     lainat = Loan.objects.filter(user=request.user).order_by('-borrowed_at')
     return render(request, 'tyokalut/omat_lainat.html', {'lainat': lainat})