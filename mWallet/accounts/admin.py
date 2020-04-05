from django.contrib import admin
from .models import Person, Wallet, Operation


class PersonAdmin(admin.ModelAdmin):
    fields = (
        'first_name', 'middle_name',
        'last_name', 'email',
        'phone_number', 'living_place',
        'birth_date', 'created_date',
    )
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)


admin.site.register(Person, PersonAdmin)


class WalletAdmin(admin.ModelAdmin):
    fields = (
        'owner', 'name',
        'description',
        'balance', 'currency',
        'created_date',
    )
    search_fields = ('name', 'owner')


admin.site.register(Wallet, WalletAdmin)


class OperationAdmin(admin.ModelAdmin):
    fields = (
        'wallet', 'amount',
        'description', 'option',
        'date',
    )


admin.site.register(Operation, OperationAdmin)
