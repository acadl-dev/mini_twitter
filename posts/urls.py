from django.urls import path
from .views import PostCreateView, PostListView, UserPostsView, UserPostUpdateView, UserPostDeleteView, LikePostView
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),

    # Novas rotas: feed do usuário, listar tweets do próprio usuário, editar tweet e deletar tweet
    path('user_posts/', UserPostsView.as_view(), name='user_posts'),  # Listar tweets do próprio usuário
    path('<int:pk>/edit/', UserPostUpdateView.as_view(), name='edit_post'),  # Editar tweet
    path('<int:pk>/delete/', UserPostDeleteView.as_view(), name='delete_post'),  # Deletar tweet
     path('like/<int:post_id>/', LikePostView.as_view(), name='like_post'),  # Curtir tweet
    
]
