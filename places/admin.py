from django.contrib import admin

from places.models import PlaceTextAppearance, Place


class PlaceTextAppearanceInlineBase(admin.StackedInline):
    model = PlaceTextAppearance
    fields = [
        'role',
        'appears_as',
        'context',
    ]
    readonly_fields = ('appears_as', 'context',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0


class PlaceTextAppearanceInlineForPlace(PlaceTextAppearanceInlineBase):
    fields = ['text'].extend(PlaceTextAppearanceInlineBase.fields)


class PlaceTextAppearanceInlineForText(PlaceTextAppearanceInlineBase):
    fields = ['place'].extend(PlaceTextAppearanceInlineBase.fields)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'altered_names',
    )

    inlines = (PlaceTextAppearanceInlineForPlace,)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('text_appearances')
