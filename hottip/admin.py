import logging
import json
from django.contrib import admin
from django.forms import widgets
from .models import Tip, Channel, Distributor
from . import fields

logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        if isinstance(value, str):
            return super(PrettyJSONWidget, self).format_value(value)

        try:
            value = json.dumps(value, indent=2, sort_keys=True)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)

class TipAdmin(admin.ModelAdmin):
    exclude = ()
    readonly_fields = ('created_at', 'updated_at',)

class TipInline(admin.StackedInline):
    extra = 0
    model = Tip

class DistributorInline(admin.TabularInline):
    template = 'admin/hottip/edit_inline/tabular.html'
    extra = 0
    model = Distributor
    formfield_overrides = {
        fields.JsonField: {'widget': PrettyJSONWidget}
    }

class ChannelAdmin(admin.ModelAdmin):
    inlines = [TipInline, DistributorInline]
    exclude = ('tip',)
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Tip, TipAdmin)
admin.site.register(Channel, ChannelAdmin)

