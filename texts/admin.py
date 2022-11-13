from django.contrib import admin

from texts.forms import XmlFileForm
from texts.models import Text


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'file')

    def get_form(self, request, obj=None, change=False, **kwargs):
        return super().get_form(request, obj, change, **kwargs) if obj else XmlFileForm
