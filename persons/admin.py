from django.contrib import admin

from persons.models import Person, TextAppearance


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'first_name', 'last_name', 'altered_names_list', 'life_range_display'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('altered_names')

    def altered_names_list(self, obj):
        return ", ".join(o.name for o in obj.altered_names.all())


class TextAppearancetInline(admin.TabularInline):
    model = TextAppearance
    fields = (
        'person',
        'role',
    )

    def get_extra(self, request, obj=None, **kwargs):
        return 0
