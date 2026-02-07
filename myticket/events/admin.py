from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'ticket_price', 'available_tickets')
    list_filter = ('date', 'location')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    fieldsets = (
        ('Event Information', {
            'fields': ('name', 'description')
        }),
        ('Event Details', {
            'fields': ('date', 'location')
        }),
        ('Pricing & Availability', {
            'fields': ('ticket_price', 'available_tickets')
        }),
    )
