from django.contrib import admin

from .models import Country, State, County, City

class CountyAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "state":
            kwargs["queryset"] = State.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(County, CountyAdmin)
admin.site.register(City)