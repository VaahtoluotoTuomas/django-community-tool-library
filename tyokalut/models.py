from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    manufacturers = models.ManyToManyField(Manufacturer)
    acquisition_year = models.IntegerField()
    image = models.ImageField(upload_to='tools/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    @property
    def is_available(self):
        return not self.loan_set.filter(returned_at__isnull=True).exists()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tools'


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def clean(self):
        # Lisää tämä printti hetkeksi varmistaaksesi, että koodi käy täällä
        print(f"\nDEBUG: Tarkistetaan työkalua {self.tool.name}, vapaana: {self.tool.is_available}")
        
        if self._state.adding and self.tool and not self.tool.is_available:
            raise ValidationError("Tämä työkalu on jo lainassa.")

    def save(self, *args, **kwargs):
        # 1. Aseta oletuseräpäivä, jos se puuttuu uutta lainaa luodessa
        if not self.id and not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
            
        # 2. Aja tarkistukset (tämä kutsuu clean-metodia)
        self.clean() 
        
        # 3. Tallenna kantaan
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
