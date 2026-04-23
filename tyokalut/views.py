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
from django.http import HttpResponse
from django.template.loader import render_to_string

class TyokaluListView(ListView):
    model = Tool
    context_object_name = 'tyokalut'
    paginate_by = 12

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['tyokalut/partials/lista_tulokset.html']
        return ['tyokalut/lista.html']

    def get_queryset(self):
        queryset = Tool.objects.all().prefetch_related('manufacturers', 'tags')
    
        hakusana = self.request.GET.get('q')
        
        if hakusana:
            queryset = queryset.filter(name__icontains=hakusana)
        return queryset
            

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

        if request.headers.get('HX-Request'):
            html = f'''
            <div id="lainaustila-kontti" class="border-t border-brand-border-muted pt-6 flex flex-col md:flex-row justify-between items-center gap-4">
                <div class="flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-brand-danger shadow-[0_0_8px_rgba(239,68,68,0.6)]"></span>
                    <div class="flex flex-col">
                        <span class="text-brand-danger-light font-semibold">Lainassa</span>
                        <span class="text-brand-text-muted text-xs">Lainaaja: {request.user.username}</span>
                    </div>
                </div>
                <button disabled class="w-full md:w-auto bg-brand-surface text-brand-text-muted font-bold py-3 px-8 rounded-lg cursor-not-allowed border border-brand-border opacity-60">
                    Työkalu on jo lainassa
                </button>
            </div>
            '''
            html += render_to_string('tyokalut/partials/toast_oob.html', request=request)
            return HttpResponse(html)

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
    
        if request.headers.get('HX-Request'):
            html = render_to_string('tyokalut/components/loan_row.html', {'laina': laina}, request=request)
            html += render_to_string('tyokalut/partials/toast_oob.html', request=request)
            return HttpResponse(html)
        
    return redirect('omat_lainat')
    

