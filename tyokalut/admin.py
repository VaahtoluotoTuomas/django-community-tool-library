from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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
    list_filter = ('tags', 'manufacturers')  
    filter_horizontal = ('manufacturers', 'tags')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('tool', 'user', 'borrowed_at', 'due_date', 'returned_at')
    list_filter = ('user', 'returned_at', 'due_date') 
    search_fields = ('tool__name', 'user__username', 'user__first_name', 'user__last_name')

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 0
    readonly_fields = ('tool', 'borrowed_at', 'due_date', 'returned_at')
    can_delete = False
    verbose_name = "Laina"
    verbose_name_plural = "Tämän käyttäjän aktiiviset ja menneet lainat"

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [LoanInline]