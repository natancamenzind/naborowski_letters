from django.contrib import admin

from persons.admin import PersonTextAppearanceInlineForText
from places.admin import PlaceTextAppearanceInlineForText
from texts.forms import XmlFileForm
from texts.models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'send_date', 'file', 'author', 'receiver')
    list_filter = (
        'language',
    )
    search_fields = ('title', 'content')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('file',),
        }),
    )
    fieldsets = (
        ('Dane podstawowe', {
            'fields': ('title', 'file', 'send_date', 'created_at')
        }),
        ('Metadane', {
           'fields': ('publication_statement', 'source_description', 'language')
        }),
        ('Treść', {
            'classes': ('collapse',),
            'fields': ('content',),
        })
    )
    readonly_fields = ('created_at',)
    inlines = (PersonTextAppearanceInlineForText, PlaceTextAppearanceInlineForText)

    def get_form(self, request, obj=None, change=False, **kwargs):
        return super().get_form(request, obj, change, **kwargs) if obj else XmlFileForm

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets if obj else self.add_fieldsets

    def get_inline_instances(self, request, obj=None):
        return super().get_inline_instances(request, obj) if obj else []
