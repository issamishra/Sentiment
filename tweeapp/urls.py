from django.urls import path
from . import views
urlpatterns = [
    path('home',views.home,name='home'),
    path('gettweet',views.get_tweets,name='tweets'),
    path('',views.index, name='index'),
    path('reg',views.signup,name='signup'),
    path('logout',views.signout,name='logout')
]
