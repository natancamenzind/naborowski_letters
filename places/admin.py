from django.contrib import admin

from places.models import PlaceTextAppearance, Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'altered_names_list',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('altered_names')

    def altered_names_list(self, obj):
        return ", ".join(o.name for o in obj.altered_names.all())


class PlaceTextAppearanceInline(admin.TabularInline):
    model = PlaceTextAppearance
    fields = (
        'place',
        'role',
    )

    def get_extra(self, request, obj=None, **kwargs):
        return 0
