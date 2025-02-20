from django.contrib import admin
from .models import Course, Profile, Lesson, Homework, HomeworkSubmission, HomeworkComment



class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('students',) #  Для ManyToMany полей


admin.site.register(Profile)
admin.site.register(Course, CourseAdmin) # регистрируем кастомную админку
admin.site.register(Lesson)
admin.site.register(Homework)
admin.site.register(HomeworkSubmission)
admin.site.register(HomeworkComment)