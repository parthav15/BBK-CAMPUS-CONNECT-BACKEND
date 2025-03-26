from django.contrib import admin
from django.utils.html import format_html
from .models import Notice

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'campus', 'status_colored', 'priority', 'is_pinned', 'created_at', 'updated_at')
    list_filter = ('campus', 'status', 'priority', 'is_pinned')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    list_per_page = 20
    exclude = ('posted_by',)

    def save_model(self, request, obj, form, change):
        obj.posted_by = request.user
        super().save_model(request, obj, form, change)

    def status_colored(self, obj):
        color = {
            'published': 'green',
            'draft': 'orange'
        }.get(obj.status, 'red')
        return format_html('<span style="font-weight: bold; color: {};">{}</span>', color, obj.get_status_display())

    status_colored.short_description = 'Status'

admin.site.register(Notice, NoticeAdmin)
