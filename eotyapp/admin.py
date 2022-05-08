from django.contrib import admin
from .models import Question
from .models import User_register,User_points
# Register your models here.

admin.site.register(Question)
admin.site.register(User_register)
admin.site.register(User_points)