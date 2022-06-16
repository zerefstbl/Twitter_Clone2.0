from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/edit/<int:pk>', views.PostEditView.as_view(), name='post_edit'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/followers/add/<int:pk>', views.AddFollowerView.as_view(), name='add_follower'),
    path('profile/followers/remove/<int:pk>', views.DeleteFollowerView.as_view(), name='remove_follower'),
    path('index/add/like/<int:pk>', views.AddLikeView.as_view(), name='add_like')
]   
