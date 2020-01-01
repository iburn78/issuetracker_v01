from django.urls import path
# from django.conf.urls.static import static
# from django.conf import settings

from .views import (
        PostListView, 
        PostDetailView, 
        PostCreateView,
        PostUpdateView,
        PostDeleteView, 
        UserPostListView, 
        # AnalysisListView
        )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), 
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'), 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'), 
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'), 
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'), 
    path('about/', views.about, name='blog-about'),
    # path('analysis/', AnalysisListView.as_view(), name='analysis-list'),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




