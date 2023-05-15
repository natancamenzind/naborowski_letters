from django.contrib import admin

from persons.models import Person, PersonTextAppearance


class PersonTextAppearanceInlineBase(admin.StackedInline):
    model = PersonTextAppearance
    fields = [
        'role',
        'appears_as',
        'context',
    ]
    readonly_fields = ('appears_as', 'context',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0


class PersonTextAppearanceInlineForPerson(PersonTextAppearanceInlineBase):
    fields = ['text'].extend(PersonTextAppearanceInlineBase.fields)


class PersonTextAppearanceInlineForText(PersonTextAppearanceInlineBase):
    fields = ['person'].extend(PersonTextAppearanceInlineBase.fields)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'first_name', 'last_name', 'altered_names', 'life_range_display'
    )
    fields = (
        'key', 'first_name', 'last_name', 'description',
        ('date_of_birth_start', 'date_of_birth_end'),
        ('date_of_death_start', 'date_of_death_end'),
        'life_range_display',
        )
    inlines = (PersonTextAppearanceInlineForPerson,)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('text_appearances')

    @admin.display(description='Występuje jako')
    def altered_names(self, obj):
        return obj.altered_names




