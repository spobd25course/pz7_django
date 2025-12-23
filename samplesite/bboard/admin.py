from django.contrib import admin
from .models import Rubric, Bb, Tag, BbExtra

class RubricAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class BbAdmin(admin.ModelAdmin):
    list_display = ['title', 'rubric', 'content', 'published', 'price', 'get_tags']
    list_filter = ['rubric', 'published']
    search_fields = ['title', 'content']
    date_hierarchy = 'published'
    ordering = ['-published']

    def get_tags(self, obj):
        return ", ".join([s.name for s in obj.tags.all()])

    get_tags.short_description = 'Тэги'


admin.site.register(Rubric, RubricAdmin)
admin.site.register(Bb, BbAdmin)
admin.site.register(Tag)
admin.site.register(BbExtra)

