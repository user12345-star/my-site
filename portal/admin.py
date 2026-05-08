from django.contrib import admin
from .models import UserProfile, Product, Promotion, Comment, Review, Order

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Promotion)
admin.site.register(Review)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_full_name',
        'product',
        'quantity',
        'name',
        'phone',
        'email',
        'address',
        'delivery_date',
        'payment_method',
        'order_date',
        'status',
    )
    list_filter = ('payment_method', 'delivery_date', 'order_date')
    search_fields = (
        'user_profile__first_name',
        'user_profile__last_name',
        'product__name',
        'name',
        'phone',
        'email',
        'address',
    )
    list_editable = ('status',)

    def user_full_name(self, obj):
        return f"{obj.user_profile.first_name} {obj.user_profile.last_name}"
    user_full_name.short_description = 'Пользователь'


