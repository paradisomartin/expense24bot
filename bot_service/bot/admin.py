from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import TelegramUser, Expense

# Desregistrar los modelos de User y Group por defecto
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'id')
    search_fields = ('telegram_id',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'amount', 'category', 'added_at')
    list_filter = ('category', 'added_at')
    search_fields = ('description',)