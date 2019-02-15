from django.contrib import admin

from .models import Course, Lesson

#admin.site.register(Course)
#admin.site.register(Lesson)

class InlineLession(admin.TabularInline):
    model = Lesson
    extra = 1
    max_num = 3

#@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (InlineLession, )
    list_display = ('title', 'slug', 'description','combine_title_and_slug')
    #list_display_links = ('title', 'slug')
    list_editable = ('slug',)
    search_fields = ('title',)
    # fields = (
    #     'slug',
    #     'title',
    #     'description',
    #     'allowed_membership'
    #)
    fieldsets = (
        (None, {
            'fields': (
                'title', 
                'slug', 
                'description', 
                'allowed_membership')
        }),
    )    

    def combine_title_and_slug(self, obj):
        return '{} - {}'.format(obj.title, obj.slug)
admin.site.register(Course, CourseAdmin)