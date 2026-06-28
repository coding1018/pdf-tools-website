from django.contrib import admin
from .models import UserProfile, ConversionTask, FileStorage, UsageStatistics


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'company', 'created_at']
    search_fields = ['user__username', 'phone', 'company']
    list_filter = ['created_at']


@admin.register(ConversionTask)
class ConversionTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'task_type', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'task_type', 'created_at']
    search_fields = ['user__username', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'completed_at']
    fieldsets = (
        ('基本信息', {'fields': ['id', 'user', 'task_type', 'status']}),
        ('文件', {'fields': ['input_file', 'output_file']}),
        ('进度', {'fields': ['progress', 'error_message']}),
        ('时间', {'fields': ['created_at', 'updated_at', 'completed_at']}),
        ('其他', {'fields': ['celery_task_id', 'metadata']}),
    )


@admin.register(FileStorage)
class FileStorageAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'file_size', 'created_at', 'is_deleted']
    list_filter = ['created_at', 'is_deleted', 'file_type']
    search_fields = ['user__username', 'file_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(UsageStatistics)
class UsageStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_files_processed', 'monthly_conversions', 'total_storage_used']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['user__username']
