from django.contrib import admin
from .models import Contact, BankAccount, FamilyMember, Nominee, Mandate

class BankAccountInline(admin.TabularInline):
    model = BankAccount
    extra = 1

class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1

class NomineeInline(admin.TabularInline):
    model = Nominee
    extra = 1

class MandateInline(admin.TabularInline):
    model = Mandate
    extra = 1

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_no', 'bank_account_type', 'bank_name', 'created_at')
    search_fields = ('name', 'email', 'mobile_no')
    inlines = [BankAccountInline, FamilyMemberInline, NomineeInline, MandateInline]

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('contact', 'account_type', 'bank_name', 'account_no', 'ifsc_code')
    list_filter = ('account_type',)
    search_fields = ('bank_name', 'account_no', 'contact__name')

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('contact', 'relationship', 'name', 'mobile', 'pan')
    list_filter = ('relationship',)
    search_fields = ('name', 'mobile', 'pan', 'contact__name')

@admin.register(Nominee)
class NomineeAdmin(admin.ModelAdmin):
    list_display = ('contact', 'name', 'relationship', 'mobile', 'email')
    search_fields = ('name', 'relationship', 'mobile', 'email', 'contact__name')

@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ('contact', 'provider', 'bank_name', 'mandate_id', 'mandate_limit', 'umrn')
    list_filter = ('provider',)
    search_fields = ('bank_name', 'mandate_id', 'payer_name', 'umrn', 'contact__name')



