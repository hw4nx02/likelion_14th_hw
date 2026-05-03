from django.urls import path

from . import views
from .views import *

app_name = 'main'
urlpatterns = [
    path('', mainpage, name="mainpage"),
    path('second', secondpage, name='secondpage'),
    path('blog', blog, name='blog'),
    path('new_post', new_post, name='new_post'),   
    path('create_post', create_post, name='create_post'),
    path('post_detail/<int:post_id>', post_detail, name='post_detail'),
    path('edit_post/<int:post_id>', edit_post, name='edit_post'),
    path('update_post/<int:post_id>', update_post, name='update_post'),
    path('delete_post/<int:post_id>', delete_post, name='delete_post'),
]