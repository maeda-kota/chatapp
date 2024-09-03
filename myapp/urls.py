from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import SendFriendRequest, judgeFriendRequest, friends, FriendRequestListView

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup', views.signup_view, name='signup_view'),
    path('signup/', views.SignupView.as_view(), name='signup_view'),
    path('login/', LoginView.as_view( template_name='myapp/login.html'), name='login_view'),
    path('friends/', views.friends.as_view(), name='friends'),
    path('send_friend_request/<int:user_id>/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('judge_friend_request/<int:request_id>/<str:action>/', judgeFriendRequest.as_view(), name='judge_friend_request'),
    path('friend_request_list/', FriendRequestListView.as_view(), name='friend_request_list'),
    path('talk_room/<int:friend_id>/', views.talk_room.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),

]
