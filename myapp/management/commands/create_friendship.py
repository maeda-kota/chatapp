import random
from django.core.management.base import BaseCommand
from myapp.models import CustomUser, FriendshipRequest, Friendship  # 自分のアプリケーション名に合わせてください

class Command(BaseCommand):
    help = 'Create friendship requests and friendships between users with a specified sender'

    def add_arguments(self, parser):
        parser.add_argument('specified_user', type=str, help='Username of the specified sender')
        parser.add_argument('num_requests', type=int, help='Number of friendship requests to create')

    def handle(self, *args, **options):
        specified_username = options['specified_user']
        num_requests = options['num_requests']

        try:
            specified_user = CustomUser.objects.get(username=specified_username)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{specified_username}" does not exist.'))
            return

        users = list(CustomUser.objects.exclude(id=specified_user.id))  # 指定されたユーザーを除外

        if len(users) < 1:
            self.stdout.write(self.style.ERROR('Not enough users to create friendship requests.'))
            return

        created_requests = 0
        while created_requests < num_requests:
            receiver = random.choice(users)  # ランダムに友達を選ぶ
            request, created = FriendshipRequest.objects.get_or_create(sender=specified_user, receiver=receiver)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created friendship request from {specified_user.username} to {receiver.username}.'))
                
                # フレンドシップの作成
                friendship, friendship_created = Friendship.objects.get_or_create(user=specified_user, friend=receiver)

                if friendship_created:
                    self.stdout.write(self.style.SUCCESS(f'Created friendship between {specified_user.username} and {receiver.username}.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Friendship already exists between {specified_user.username} and {receiver.username}.'))

                created_requests += 1
            else:
                self.stdout.write(self.style.WARNING(f'Friendship request already exists from {specified_user.username} to {receiver.username}.'))