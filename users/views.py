from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Follow
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['POST'])  # Definindo que esta view só aceita requisições POST
@permission_classes([IsAuthenticated])  # Apenas usuários autenticados podem acessar
def follow_unfollow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    logged_in_user = request.user

    if user_to_follow == logged_in_user:
        return JsonResponse({"error": "You cannot follow yourself."}, status=400)

    # Verifica se já está seguindo
    existing_follow = Follow.objects.filter(follower=logged_in_user, followed=user_to_follow)

    if existing_follow.exists():
        # Se já estiver seguindo, deixar de seguir
        existing_follow.delete()
        return JsonResponse({"message": f"You have unfollowed {user_to_follow.username}"}, status=200)
    else:
        # Se não estiver seguindo, seguir
        Follow.objects.create(follower=logged_in_user, followed=user_to_follow)
        return JsonResponse({"message": f"You are now following {user_to_follow.username}"}, status=201)
    
class FollowingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()  # Assume que você tem um relacionamento de seguir
        return Response([user.username for user in following])
