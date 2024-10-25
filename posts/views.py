from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from .models import Post, Like
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class PostCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')  # Consulta para buscar todos os posts
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# NOVAS FUNCIONALIDADES

# 1. Listar tweets do próprio usuário
class UserPostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Retorna os tweets apenas do usuário autenticado
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)    


# 2. Editar um tweet (somente se for do próprio usuário)
class UserPostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este post.")
        return post

# 3. Deletar um tweet (somente se for do próprio usuário)
class UserPostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        post = super().get_object()
        if post.author != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este post.")
        return post

# 4. Curtir um tweet (qualquer usuário autenticado pode curtir um tweet, mas não pode curtir o mesmo tweet duas vezes.)
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            # Tenta criar o like, se o like já existe, o usuário "descurte" o post
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            
            if not created:
                # Se o like já existe, o usuário está tentando descurtir
                like.delete()
                is_liked = False
                return Response({'message': 'Post unliked', 'is_liked': is_liked}, status=status.HTTP_200_OK)
            
            is_liked = True
            return Response({'message': 'Post liked', 'is_liked': is_liked}, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
