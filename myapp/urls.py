from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import SendFriendRequest, judgeFriendRequest, UserList, FriendRequestList,Login

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignupView.as_view(), name='signup_view'),
    path('login/', views.Login.as_view(), name='login_view'),
    path('friends/', views.friends.as_view(), name='friends'),
    path('send_friend_request/<int:user_id>/', SendFriendRequest.as_view(), name='send_friend_request'),
    path('judge_friend_request/<int:request_id>/<str:action>/', judgeFriendRequest.as_view(), name='judge_friend_request'),
    path('friend_request_list/', FriendRequestList.as_view(), name='friend_request_list'),
    path('users/', UserList.as_view(), name='user_list'),
    path('talk_room/<int:friend_id>/', views.talk_room.as_view(), name='talk_room'),
    path('setting/', views.setting.as_view(), name='setting'),
    path('usernameChange/', views.usernameChangeView.as_view(), name='usernameChange'),
    path('emailChange/', views.emailChangeView.as_view(), name='emailChange'),
    path('iconChange/', views.iconChangeView.as_view(), name='iconChange'),
    path('passwordChange/', views.passwordChangeView.as_view(), name='passwordChange'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('afterChange/', views.afterChange.as_view(), name='afterChange')
]
