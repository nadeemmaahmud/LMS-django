from django.db import models
from users.models import CustomUser
from core.models import Course

class Batch(models.Model):
    number = models.IntegerField()
    admission_deadline = models.DateTimeField(null=True, blank=True)
    class_start = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch - {self.number}"
    
class Enrollment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    enroll_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"Batch: {self.batch.number} - Course: {self.course.title} - User: {self.user.username}"