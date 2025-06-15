import os
import uuid
from django.db import models

def clean_name(name):
    return "".join([c if c.isalnum() else "_" for c in name])

def course_upload_path(instance, filename):
    course_title = clean_name(instance.title)
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(course_title, new_filename)

def lesson_image_upload_path(instance, filename):
    if hasattr(instance, 'lesson') and hasattr(instance.lesson, 'course'):
        course_title = clean_name(instance.lesson.course.title)
        lesson_topic = clean_name(instance.lesson.topic)
    else:
        course_title = "unknown"
        lesson_topic = "unknown"
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(course_title, lesson_topic, new_filename)

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Type(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title
    
class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    duration = models.IntegerField()
    price = models.IntegerField()
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    banner = models.ImageField(upload_to=course_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    details = models.TextField()
    isComplete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic
    
class LessonImages(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to=lesson_image_upload_path)

    def __str__(self):
        return f"{self.lesson.course.title} | {self.lesson.topic} | {self.file.name.split('/')[-1]}"
