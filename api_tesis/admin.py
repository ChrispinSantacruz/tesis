from django.contrib import admin
from .models import Thesis, Approval

class ThesisAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'approved', 'created_at', 'updated_at')
    search_fields = ('title', 'student__username')
    list_filter = ('approved', 'created_at', 'updated_at')
    ordering = ('-created_at',)

class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('thesis', 'approved_by', 'approved_at', 'is_approved')
    search_fields = ('thesis__title', 'approved_by__username')
    list_filter = ('is_approved', 'approved_at')
    ordering = ('-approved_at',)

admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Approval, ApprovalAdmin)
