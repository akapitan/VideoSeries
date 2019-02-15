''' Hallo '''
from django.db import models
from django.urls import reverse
from membership.models import Membership

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    allowed_membership = models.ManyToManyField(Membership)

    def __str__(self):
        return self.title

    ##Veže se na courses->urls.py gdje je path path('<slug>', CourseDetailView.as_view(), name='detail')
    def get_absolute_url(self):
        return reverse("courses:detail", kwargs={'slug':self.slug})
        # return "{}/".format(self.slug)


    ##Propery allows us to use "lessons" instead of "lessons()"
    ## Returns all lessons from the foreighn key
    ### If we would have class "Lectures" we would use  lecture_set.all()'''
    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position') 
    
class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video = models.CharField(max_length=400)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", 
        kwargs={
            'course_slug': self.course.slug,
            'lesson_slug': self.slug
            })