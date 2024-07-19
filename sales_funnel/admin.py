from django.contrib import admin
from sales_funnel.models import SalesFunnelOwner, NewsletterSubscription, FunnelStep

# Admin Models

@admin.register(SalesFunnelOwner)
class SalesFunnelOwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'enabled']
    search_fields = ['id', 'user__first_name', 'user__last_name']
    list_filter = ['enabled']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subscribed_to', 'subscriptor_email', 'sent_emails', 'enabled']
    search_fields = ['id', 'subscriptor_email']
    list_filter = ['sent_emails', 'enabled']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30

@admin.register(FunnelStep)
class FunnelStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'step_number', 'title', 'youtube_video_url', 'next_step', 'enabled']
    search_fields = ['title', 'youtube_video_url']
    list_filter = ['id', 'step_number', 'next_step', 'enabled']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 30