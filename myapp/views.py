from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .forms import signupform
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Friendship, FriendshipRequest, CustomUser
from django.views.generic import ListView

def index(request):
    return render(request, "myapp/index.html" )

class SignupView(CreateView):
    template_name = 'myapp/signup.html'
    form_class = signupform
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response 
    
class friends(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = "myapp/friends.html"
    context_object_name = 'friends_object'

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user=user).selelct_related('friend')

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.status})"

class FriendRequestListView(LoginRequiredMixin, ListView):
    model = FriendshipRequest
    template_name = 'friend_request_list.html'
    context_object_name = 'received_requests'

    def get_queryset(self):
        return FriendshipRequest.objects.filter(receiver=self.request.user, status='pending')

class SendFriendRequest(LoginRequiredMixin, View):
    def post(self, request, user_id):
        receiver = get_object_or_404(CustomUser, id=user_id)
        if request.user != receiver:
            FriendshipRequest.objects.create(sender=request.user, receiver=receiver)
        return redirect('friend_request_list') 

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



class talk_room(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "myapp/talk_room.html"
    context_object_name = 'friend'

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['friend_id'])

def setting(request):
    return render(request, "myapp/setting.html")
