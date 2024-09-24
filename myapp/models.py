from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100)
    img = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return self.username

class FriendshipRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, related_name='frineds', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friends_with', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return f"{self.user.username} is friends with {self.friend.username}"

class Message(models.Model):
    content = models.TextField()
    from_user = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}: {self.content[:20]}"
    
    class Meta: 
        ordering = ['timestamp']