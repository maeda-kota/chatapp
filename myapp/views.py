from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .forms import usernameChangeform,emailChangeform,iconChangeform,SignupForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import login, get_user_model,authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friendship, FriendshipRequest, CustomUser, Message
from django.views.generic import ListView
from django.db.models import OuterRef, Subquery, Q
from django.contrib.auth.forms import PasswordChangeForm
from allauth.account.views import LoginView,LogoutView,PasswordResetView,PasswordSetView,ConfirmEmailView,EmailView,SignupView
from allauth.account.forms import LoginForm
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import datetime

CustomUser = get_user_model()

def index(request):
    return render(request, "myapp/index.html" )



# class Login(LoginView):
#     template_name = 'myapp/login.html'
#     form_class = LoginForm
    

# class SignupView(CreateView):
#     template_name = 'myapp/signup.html'
#     form_class = signupform
#     success_url = reverse_lazy('friends')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return response
    
class UserList(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'myapp/user_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends = Friendship.objects.filter(user=self.request.user).select_related('friend')
        friend_id = friends.values_list('friend', flat=True)
        friendship_request = FriendshipRequest.objects.filter(sender=self.request.user).select_related('receiver')
        receiver_id = friendship_request.values_list('receiver', flat=True)
        context['friends'] = friends
        context['friend_id'] = friend_id
        context['friendship_request'] = friendship_request 
        context['receiver_id'] = receiver_id

        return context
    
    def get_queryset(self):

        query1 = self.request.GET.get('query1')
        query2 = self.request.GET.get('query2')

        if query1 and query2 :
            query_user = CustomUser.objects.filter(Q(username__icontains=query1) & Q(email__icontains=query2))

        elif query1  : 
            query_user = CustomUser.objects.filter(username__icontains=query1)

        elif query2 :
            query_user = CustomUser.objects.filter(email__icontains=query2)
        else :
            query_user = CustomUser.objects.exclude(id=self.request.user.id)

        return query_user
    
class SendFriendRequest(LoginRequiredMixin, View):
    def post(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        if request.user != receiver:
            FriendshipRequest.objects.create(sender=request.user, receiver=receiver)
            print(f"Friend request sent from {request.user} to {receiver}")
        return redirect('user_list') 

class judgeFriendRequest(LoginRequiredMixin, View):
    def post(self, request, request_id, action):
        friendship_request = get_object_or_404(FriendshipRequest, id=request_id)
        if action == 'accept':
            Friendship.objects.create(user=friendship_request.receiver, friend=friendship_request.sender)
            Friendship.objects.create(user=friendship_request.sender, friend=friendship_request.receiver)
            friendship_request.status = 'accepted'
        elif action == 'reject':
            friendship_request.status = 'rejected'
        friendship_request.save()
        return redirect('friend_request_list')  

class FriendRequestList(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = 'myapp/friend_request_list.html'
    context_object_name = 'received_requests'

    def get_queryset(self):
        friends = Friendship.objects.filter(user=self.request.user).values_list('friend', flat=True)
        return FriendshipRequest.objects.filter(receiver=self.request.user, status='pending').exclude(sender__in = friends).select_related('sender')
  
    
class friends(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = "myapp/friends.html"
    context_object_name = 'friendships'

    def get_queryset(self):
        
            current_user = self.request.user

            latest_message_sender = Message.objects.filter(
                (Q(from_user=OuterRef('friend__id'), to_user=current_user) | 
                Q(from_user=current_user, to_user=OuterRef('friend__id')))
            ).select_related('from_user').order_by('-timestamp').values_list('from_user__username')[:1]

            latest_message = Message.objects.filter(
                (Q(from_user=OuterRef('friend__id'), to_user=current_user) | 
                Q(from_user=current_user, to_user=OuterRef('friend__id')))
            ).order_by('-timestamp').values('content')[:1]

            latest_message_time = Message.objects.filter(
                (Q(from_user=OuterRef('friend__id'), to_user=current_user) | 
                Q(from_user=current_user, to_user=OuterRef('friend__id')))
            ).order_by('-timestamp').values('timestamp')[:1]

            query1 = self.request.GET.get('query1')
            query2 = self.request.GET.get('query2')


            if query1 and query2 :
                query_friend = Friendship.objects.filter(Q(friend__username__icontains=query1) & Q(friend__email__icontains=query2))
                
                friendships = query_friend.filter(user=current_user).select_related('friend').annotate(
                    latest_message=Subquery(latest_message),
                    latest_message_time=Subquery(latest_message_time),
                    latest_message_sender=Subquery(latest_message_sender)
                ).order_by(Coalesce('latest_message_time', timezone.make_aware(datetime.min)).desc())

            elif query1  : 
                query_friend = Friendship.objects.filter(friend__username__icontains=query1)

                friendships = query_friend.filter(user=current_user).select_related('friend').annotate(
                    latest_message=Subquery(latest_message),
                    latest_message_time=Subquery(latest_message_time),
                    latest_message_sender=Subquery(latest_message_sender)
                ).order_by(Coalesce('latest_message_time', timezone.make_aware(datetime.min)).desc())


            elif query2 :
                query_friend = Friendship.objects.filter(friend__email__icontains=query2)

                friendships = query_friend.filter(user=current_user).select_related('friend').annotate(
                    latest_message=Subquery(latest_message),
                    latest_message_time=Subquery(latest_message_time),
                    latest_message_sender=Subquery(latest_message_sender)
                ).order_by(Coalesce('latest_message_time', timezone.make_aware(datetime.min)).desc())


            else :
                friendships = Friendship.objects.filter(user=current_user).select_related('friend').annotate(
                    latest_message=Subquery(latest_message),
                    latest_message_time=Subquery(latest_message_time),
                    latest_message_sender=Subquery(latest_message_sender)
                ).order_by(Coalesce('latest_message_time', timezone.make_aware(datetime.min)).desc())

            return friendships
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friendships = self.get_queryset()

        if not friendships.exists() and not self.request.GET.get('query'):
            context['no_query_friend'] = '現在友達はいません。ぼっちです。'
        elif not friendships.exists() and self.request.GET.get('query'):
            context['no_query_friend'] = 'そんな友達いませんね。'
        return context
    
    

class talk_room(LoginRequiredMixin, TemplateView):
    template_name = "myapp/talk_room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friend_id = self.kwargs['friend_id']
        friend = CustomUser.objects.get(id=friend_id)

        messages = Message.objects.filter(
            (Q(from_user=self.request.user) & Q(to_user=friend)) | 
            (Q(from_user=friend) & Q(to_user=self.request.user))
        ).order_by('timestamp')

        context['friend'] = friend
        context['messages'] = messages
    
        return context
    
    def post(self, request, *args, **kwargs):
        friend_id = self.kwargs['friend_id']
        friend = CustomUser.objects.get(id=friend_id)
        content = request.POST.get('message') 

        if content:
            Message.objects.create(
                from_user=request.user,
                to_user=friend,
                content=content
            )
        return self.get(request, *args, **kwargs)

class setting(TemplateView):
    template_name = "myapp/setting.html"

class usernameChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "myapp/Change.html"
    form_class = usernameChangeform
    success_url = reverse_lazy('afterChange')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ユーザーネーム変更'
        return context
    
class emailChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "myapp/Change.html"
    form_class = emailChangeform
    success_url = reverse_lazy('afterChange')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'メールアドレス変更'
        return context
    
class iconChangeView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "myapp/Change.html"
    form_class = iconChangeform
    success_url = reverse_lazy('afterChange')

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'アイコン変更'
        return context
    
class passwordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "myapp/Change.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy('afterChange')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'パスワード変更'
        return context     

# class Logout(LogoutView):
#     template_name = 'myapp/logout.html'

class afterChange(LoginRequiredMixin,TemplateView):
    template_name = 'myapp/afterChange.html'