from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nimi')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'valmistaja'
        verbose_name_plural = 'Valmistajat'

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nimi')
    # LISÄTTY: Mahdollisuus määritellä kategoriakohtainen laina-aika
    default_loan_days = models.PositiveIntegerField(
        default=14, 
        verbose_name='Oletuslaina-aika (päivää)',
        help_text='Kuinka monta päivää tämän kategorian työkaluja saa yleensä lainata?'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'kategoria'
        verbose_name_plural = 'Kategoriat'

class Tool(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Nimi')
    manufacturers = models.ManyToManyField(Manufacturer, verbose_name='Valmistaja')
    acquisition_year = models.IntegerField(verbose_name='Hankintavuosi')
    image = models.ImageField(upload_to='tools/', null=True, blank=True, verbose_name='Kuva')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Kategoria')
    description = models.TextField(verbose_name='Kuvaus')

    def __str__(self):
        return self.name
    
    @property
    def is_available(self):
        return not self.loan_set.filter(returned_at__isnull=True).exists()

    class Meta:
        ordering = ['name']
        verbose_name = 'työkalu'
        verbose_name_plural = 'Työkalut'


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Käyttäjä')
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name='Työkalu')
    borrowed_at = models.DateTimeField(auto_now_add=True, verbose_name='Lainauspäivä')
    due_date = models.DateTimeField(verbose_name='Eräpäivä')
    returned_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Palautettu')

    def clean(self):
        # Tarkistetaan onko työkalu vapaana vain uusia lainoja luotaessa
        if self._state.adding and self.tool and not self.tool.is_available:
            raise ValidationError("Tämä työkalu on jo lainassa.")

    def save(self, *args, **kwargs):
        # LISÄTTY: Dynaaminen laina-ajan haku
        if not self.pk and not self.due_date:
            loan_days = 14  # Globaali oletus, jos kategorialla ei ole määritelty aikaa
            
            # Haetaan työkalun kategoriat. Jos niitä on useita, valitaan lyhyin laina-aika (varmuuden vuoksi)
            # tai voit valita pisimmän (.order_by('-default_loan_days'))
            category_with_period = self.tool.tags.all().order_by('default_loan_days').first()
            
            if category_with_period:
                loan_days = category_with_period.default_loan_days
            
            self.due_date = timezone.now() + timedelta(days=loan_days)
            
        self.clean() 
        super().save(*args, **kwargs)

    @property
    def is_late(self):
        if self.returned_at:
            return False
        return self.due_date < timezone.now()

    def __str__(self):
        return f"{self.tool.name} - {self.user.username}"

    class Meta:
        ordering = ['-borrowed_at']
        verbose_name = 'laina'
        verbose_name_plural = 'Lainat'