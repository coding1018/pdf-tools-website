from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid
import os


class UserProfile(models.Model):
    """扩展用户资料"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class ConversionTask(models.Model):
    """PDF转换任务"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]

    TYPE_CHOICES = [
        ('merge', 'PDF合并'),
        ('split', 'PDF分割'),
        ('compress', 'PDF压缩'),
        ('convert', 'PDF转换'),
        ('encrypt', 'PDF加密'),
        ('decrypt', 'PDF解密'),
        ('watermark', 'PDF水印'),
        ('img_to_pdf', '图片转PDF'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    input_file = models.FileField(
        upload_to='inputs/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'gif'])]
    )
    output_file = models.FileField(upload_to='outputs/%Y/%m/%d/', null=True, blank=True)
    error_message = models.TextField(blank=True)
    progress = models.IntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    celery_task_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # 存储额外参数

    class Meta:
        verbose_name = '转换任务'
        verbose_name_plural = '转换任务'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.get_task_type_display()} - {self.id}"

    def is_completed(self):
        return self.status == 'completed'

    def is_failed(self):
        return self.status == 'failed'


class FileStorage(models.Model):
    """文件存储记录"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='storage/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # 字节
    file_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # 过期时间
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = '文件存储'
        verbose_name_plural = '文件存储'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.file_name

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class UsageStatistics(models.Model):
    """用户使用统计"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usage_stats')
    total_files_processed = models.IntegerField(default=0)
    total_storage_used = models.BigIntegerField(default=0)  # 字节
    total_conversions = models.IntegerField(default=0)
    monthly_conversions = models.IntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '使用统计'
        verbose_name_plural = '使用统计'

    def __str__(self):
        return f"{self.user.username}'s Statistics"
