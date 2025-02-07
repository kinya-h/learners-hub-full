from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Payment, WriterProfile,WriterApplication

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    # Fields to display in the list view
    list_display = (
        'tracking_id',
        'user_link',
        'provider',
        'status_badge',
        'currency',
        'account',
        'customer_id',
        'phone_number',
        'email',
        'created_at',
    )

    # Fields to filter by in the sidebar
    list_filter = (
        'status',
        'provider',
        'currency',
        'created_at',
        'user__is_staff',  # Example filter: whether the user is staff
    )

    # Fields to search by
    search_fields = (
        'tracking_id',
        'user__username',
        'user__email',
        'provider',
        'account',
        'customer_id',
        'phone_number',
        'email',
        'first_name',
        'last_name',
    )

    # Default ordering
    ordering = ('-created_at',)

    # Fields to display as read-only
    readonly_fields = (
        'tracking_id',
        'user',
        'provider',
        'status',
        'currency',
        'account',
        'customer_id',
        'phone_number',
        'email',
        'first_name',
        'last_name',
        'created_at',
    )

    # Fields to display in the detail view
    fieldsets = (
        (None, {
            'fields': (
                'tracking_id',
                'user',
                'provider',
                'status',
                'currency',
                'account',
                'customer_id',
                'phone_number',
                'email',
                'first_name',
                'last_name',
                'created_at',
            )
        }),
    )

    # Customize list display colors and formatting
    def status_badge(self, obj):
        """
        Returns a colored badge for the payment status.
        """
        status_colors = {
            'COMPLETED': 'green',
            'FAILED': 'red',
            'REVERSED': 'orange',
            'PROCESSED': 'blue',
        }
        color = status_colors.get(obj.status, 'grey')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 5px 10px; border-radius: 5px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'status'
    status_badge.admin_order_field = 'status'

    def user_link(self, obj):
        """
        Returns a clickable link to the related User's admin page.
        """
        from django.urls import reverse
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
    
    def amount_display(self, obj):
        """
        Formats the amount with currency.
        """
        return f"${obj.amount:,.2f}"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'

    # Define custom actions
    actions = ['mark_as_completed', 'mark_as_failed']

    def mark_as_completed(self, request, queryset):
        """
        Custom action to mark selected payments as COMPLETED.
        """
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} payment(s) marked as COMPLETED.")
    mark_as_completed.short_description = "Mark selected payments as COMPLETED"

    def mark_as_failed(self, request, queryset):
        """
        Custom action to mark selected payments as FAILED.
        """
        updated = queryset.update(status='FAILED')
        self.message_user(request, f"{updated} payment(s) marked as FAILED.")
    mark_as_failed.short_description = "Mark selected payments as FAILED"

    # Optional: Disable adding new Payment records via admin
    def has_add_permission(self, request):
        return False

    # Optional: Disable deleting Payment records via admin
    def has_delete_permission(self, request, obj=None):
        return False
    

@admin.register(WriterApplication)
class WriterApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'category',
        'experience',
        'submission_date',
        'approval_status',
        'approval_action'
    )
    list_filter = ('is_approved', 'category', 'experience')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at',)
    actions = ['approve_applications']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Name"

    def submission_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M")
    submission_date.short_description = "Submitted"

    def approval_status(self, obj):
        return "Approved" if obj.is_approved else "Pending"
    approval_status.short_description = "Status"

    def approval_action(self, obj):
        if obj.is_approved:
            return "Approved"
        return format_html(
            '<a class="button" href="{}">Approve</a>',
            f"/api/writers/writerapplication/{obj.id}/approve/"
        )
    approval_action.short_description = "Action"
    approval_action.allow_tags = True

    def approve_applications(self, request, queryset):
        for application in queryset:
            if not application.is_approved:
                self.create_writer_profile(application)
                application.is_approved = True
                application.save()
        self.message_user(request, f"{queryset.count()} applications approved")
    approve_applications.short_description = "Approve selected applications"

    def create_writer_profile(self, application):
        WriterProfile.objects.create(
            name=f"{application.first_name} {application.last_name}",
            role=application.category,
            specialization=application.category,
            experience=application.experience,
            status="Active",
            location="Unknown",
            email=application.email,
            phone_number=application.phone,
            skills=[application.category],
            projects="0",
        )


@admin.register(WriterProfile)
class WriterProfileAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'name',
        'role',
        'rating',
        'specialization',
        'location',
        'experience',
        'status',
    )

    # Fields to filter by in the sidebar
    list_filter = (
        'role',
        'specialization',
        'rating',
        'location',
        'status',
    )

    # Fields to search by
    search_fields = (
        'name',
        'role',
        'specialization',
        'location',
    )

    # Fields to display in the detail view
    fieldsets = (
        (None, {
            'fields': (
                'avatar',
                'name',
                'role',
                'rating',
                'specialization',
                'skills',
                'projects',
                'experience',
                'status',
                'location',
            )
        }),
    )

    # Customize the display of skills (optional)
    def skills_display(self, obj):
        return ", ".join(obj.skills)
    skills_display.short_description = "Skills"

    # Optional: Disable adding new records via admin
    def has_add_permission(self, request):
        return True  # Set to False if you want to disable adding new records

    # Optional: Disable deleting records via admin
    def has_delete_permission(self, request, obj=None):
        return True  # Set to False if you want to disable deleting records    