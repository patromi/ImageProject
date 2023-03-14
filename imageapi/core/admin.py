from django.contrib import admin

from .models import Images

# Register your models here.

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'resolution', 'uploaded_by', 'create_at', 'expired_at')
    list_filter = ('uploaded_by', 'create_at', 'expired_at')
    search_fields = ('title',)
    date_hierarchy = 'create_at'
    readonly_fields = ('create_at',)

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)