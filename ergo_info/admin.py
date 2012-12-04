from django.contrib import admin
from ergo_info.models import Allergy, Drug, Immunization


class AllergyAdmin(admin.ModelAdmin):
    list_display = ('name', 'allergy_id',)
    search_fields = ['name']


class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'drug_id',)
    search_fields = ['name']


class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ('vaccine_name', 'vaccine_id',)
    search_fields = ['vaccine_name']


admin.site.register(Allergy, AllergyAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Immunization, ImmunizationAdmin)


