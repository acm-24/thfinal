from django.urls import path
from . import views

urlpatterns = [
    path('',views.register,name="register"),
    path('play/',views.play,name="play"),
    path('contact/',views.contact,name="contact"),
    path('rules/',views.rules,name="rules"),
    path('leaderboard/',views.leaderboard),
    path('signin/',views.signin,name="signin"),
    path('index/',views.index,name="index"),
    path('hint1/',views.hint1,name='hint1'),
    path('hint2/',views.hint2,name='hint2'),
    path('length/',views.length,name='length'),
    path('first_letter/',views.first_letter,name='first_letter'),
    path('logout/',views.logout,name='logout'),
    path('backup/',views.backup,name="backup"),
]
