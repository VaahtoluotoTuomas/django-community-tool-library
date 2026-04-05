from django.contrib import admin
from .models import Manufacturer, Tag, Tool, Loan

Tool.manufacturers.through.__str__ = lambda x: f"{x.tool.name}"
Tool.tags.through.__str__ = lambda x: f"{x.tool.name}"

class ToolInline(admin.TabularInline):
    model = Tool.manufacturers.through
    extra = 0
    verbose_name = "Työkaluvalinta"
    verbose_name_plural = "Tämän valmistajan työkalut"

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    inlines = [ToolInline]

class ToolTagInline(admin.TabularInline):
    model = Tool.tags.through
    extra = 0
    verbose_name = "Työkaluvalinta"
    verbose_name_plural = "Tähän kategoriaan kuuluvat työkalut"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ToolTagInline]

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'acquisition_year')
    search_fields = ('name',)
    filter_horizontal = ('manufacturers', 'tags')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('tool', 'user', 'borrowed_at', 'due_date', 'returned_at')
    list_filter = ('returned_at', 'due_date')

