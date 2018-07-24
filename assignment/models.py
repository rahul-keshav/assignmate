from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.timezone import now



# Create your models here.
class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=30,default='assignment')
    discription=models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('assignment:assignment_page')

class Questions(models.Model,):
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    question=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    option_a=models.CharField(max_length=200,default=0)
    option_b=models.CharField(max_length=200,default=0)
    option_c=models.CharField(max_length=200,default=0)
    option_d=models.CharField(max_length=200,default=0)
    number_of_right_answered=models.IntegerField(default=0)
    number_of_wrong_answered=models.IntegerField(default=0)
    positive_marks=models.IntegerField(default=0)
    negative_marks=models.IntegerField(default=0)
    hint=models.CharField(max_length=500)
    tags=models.CharField(max_length=45)


    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('assignment:assignment_page')


class Assignment_answered_by(models.Model):
    name_of_assignment=models.CharField(max_length=30)
    assignment_id=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer_string=models.CharField(max_length=400)
    marks=models.IntegerField()
    total_marks=models.IntegerField()
    submitted=models.DateTimeField(default=now)
    def __str__(self):
        return self.user.first_name+' '+self.user.last_name


class Studymaterial(models.Model):
    name=models.CharField(max_length=30)
    subject=models.CharField(max_length=20)
    discription=models.CharField(max_length=500)
    document=models.FileField(upload_to='documents//%Y/%m/%d/')
    uploaded_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Blogsite(models.Model):
    name=models.CharField(max_length=30)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quotes=models.CharField(max_length=100)
    discription = models.CharField(max_length=500)
    background_image=models.ImageField(upload_to='blogger_image/')
    def __str__(self):
        return self.name

class Blog_page(models.Model):
    title=models.CharField(max_length=40)
    blog_site=models.ForeignKey(Blogsite,on_delete=models.CASCADE)
    text=models.TextField()
    image = models.ImageField(upload_to='blog_image/')
    def __str__(self):
        return self.title
