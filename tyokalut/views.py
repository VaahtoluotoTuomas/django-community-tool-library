from django.shortcuts import render, get_object_or_404
from .models import Tool, Loan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class TyokaluListView(ListView):
    model = Tool
    template_name = 'tyokalut/lista.html'
    context_object_name = 'tyokalut'
    paginate_by = 12

    def get_queryset(self):
        return Tool.objects.all().prefetch_related('manufacturers', 'tags')

class TyokaluDetailView(DetailView):
    model = Tool
    template_name = 'tyokalut/tiedot.html'
    context_object_name = 'tyokalu'
    pk_url_kwarg = 'tyokalu_id' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tyokalu = self.get_object()
        
        aktiivinen_laina = Loan.objects.filter(tool=tyokalu, returned_at__isnull=True).first()
        
        context['aktiivinen_laina'] = aktiivinen_laina
        context['on_vapaana'] = aktiivinen_laina is None
        return context
    
class OmatLainatView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = 'tyokalut/omat_lainat.html'
    context_object_name = 'lainat'
    paginate_by = 15

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user).order_by('-borrowed_at')

class RekisteroidyView(CreateView):
    form_class = UserCreationForm
    template_name = 'tyokalut/rekisteroidy.html'
    success_url = reverse_lazy('tyokalu_lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

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
    

