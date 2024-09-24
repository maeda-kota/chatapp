from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import FriendshipRequest, Friendship

CustomUser = get_user_model()

admin.site.register(CustomUser)

@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'created_at')

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend')
    search_fields = ('user__username', 'friend__username')