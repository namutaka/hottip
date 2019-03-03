from django.contrib import admin
from .models import Tip, Channel, Distributor

class TipAdmin(admin.ModelAdmin):
    exclude = ()
    readonly_fields = ('created_at', 'updated_at',)

class TipInline(admin.TabularInline):
    extra = 0
    model = Channel.tips.through

class DistributorInline(admin.TabularInline):
    extra = 0
    model = Distributor

class ChannelAdmin(admin.ModelAdmin):
    inlines = [TipInline, DistributorInline]
    exclude = ('tip',)
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Tip, TipAdmin)
admin.site.register(Channel, ChannelAdmin)

