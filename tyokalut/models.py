from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=200)
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

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_late(self):
        if self.returned_at:
            return False
        return self.due_date < timezone.now()

    def __str__(self):
        return f"{self.tool.name} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.id and not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)
