from django.contrib import admin
from . models import Category, Type, Course, Lesson, LessonImages

admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonImages)