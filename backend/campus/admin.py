from django.contrib import admin
from campus.models import Campus, Incident

class CampusAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'city',
        'state',
        'country',
        'website',
        'head_name',
        'head_phone',
        'head_email',
        'established_year',
        'created_at',
        'updated_at'
    ]
    search_fields = ['name', 'city', 'state', 'country', 'website']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
    fieldsets = (
        ("Campus Information", {
            'fields': (
                'name',
                'address',
                'city',
                'state',
                'country',
                'zip_code',
                'phone',
                'email',
                'website',
                'head_name',
                'head_phone',
                'head_email',
                'image',
                'description',
                'established_year'
            )
        }),
    )


class IncidentAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'campus',
        'reported_by',
        'status',
        'created_at',
        'updated_at'
    ]
    search_fields = ['title', 'description', 'campus__name', 'reported_by__username']
    list_filter = ['status', 'created_at', 'updated_at']
    ordering = ['-created_at']
    fieldsets = (
        ("Incident Information", {
            'fields': (
                'title',
                'description',
                'campus',
                'reported_by',
                'status',
                'media_files',
                'location'
            )
        }),
    )


admin.site.register(Campus, CampusAdmin)
admin.site.register(Incident, IncidentAdmin)