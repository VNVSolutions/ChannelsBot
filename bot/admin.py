from django.contrib import admin
from .models import MainChannel, SubChannel, KeywordReplacement, KeywordReplacementItem


class ReplacementItem(admin.TabularInline):
    model = KeywordReplacementItem


class Replacement(admin.ModelAdmin):
    inlines = [ReplacementItem]


admin.site.register(MainChannel)
admin.site.register(SubChannel)
admin.site.register(KeywordReplacement, Replacement)
