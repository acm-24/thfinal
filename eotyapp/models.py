from distutils.command.upload import upload
from django.db import models

class Question(models.Model):
    q_id = models.IntegerField(primary_key=True)
    q_img = models.ImageField(upload_to='question/')
    q_ans = models.TextField()
    hint1 = models.TextField()
    hint2 = models.TextField()
    q_point = models.IntegerField(default=50)

class User_register(models.Model):
    e_id = models.IntegerField(primary_key=True)
    e_p = models.TextField()

class User_points(models.Model):
    #e_no = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    e_no=models.IntegerField(primary_key=True)
    reputation = models.IntegerField(default=100)
    cur_ques = models.IntegerField(default=1)
    hint = models.IntegerField(default=0)
    first_letter = models.IntegerField(default=0)
    length = models.IntegerField(default=0)
