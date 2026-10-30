import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("Error: Django modules not found.")
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=30, null=False, default='online course')
    description = models.CharField(max_length=1000)
    img = models.ImageField(upload_to='course_images/')
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_instructors')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment', related_name='courses_joined')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    body = models.TextField()

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text

    def calculate_grade(self, selected_ids):
        correct_ids = self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        if set(correct_ids) == set(selected_ids):
            return True
        return False

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=10, choices=[('audit', 'Audit'), ('honor', 'Honor')], default='audit')
    rating = models.IntegerField(default=5)

class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
