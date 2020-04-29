"""funBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path

from fun import views as fv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fv.posts, name='main'),

    path('authors/<int:username>/', fv.author_details, name='author'),
    path('authors/<int:username>/edit', fv.edit_author, name='edit_author'),
    path('authors/<int:user_id>/fav', fv.a_fav, name='fav_list'),
    path('authors/<int:user_id>/my_fav', fv.my_fav, name='my_fav'),

    path('posts/new_post/', fv.new_post, name='new_post'),
    path('posts/<int:post_id>/', fv.post_details, name='post_details'),
    path('posts/<int:post_id>/delete/', fv.delete_post, name='delete_post'),
    path('posts/<int:post_id>/edit/', fv.edit_post, name='edit_post'),

    # the weekend blinding lights

    path('login/', fv.pagelogin, name='login'),
    path('signup/', fv.signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
