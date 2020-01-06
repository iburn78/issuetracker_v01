from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
        ListView, 
        DetailView,
        CreateView,
        UpdateView, 
        DeleteView
        )
from django.http import HttpResponse
from .models import Post 
from taggit.models import Tag
from django.template.defaultfilters import slugify

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 7 
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['common_tags'] = Post.tags.most_common()[:4]
    #     return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 7 

    def get_queryset(self): # overriding a method
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['common_tags'] = Post.tags.most_common()[:4]
    #     return context

class PostDetailView(DetailView):
    model = Post

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['common_tags'] = Post.tags.most_common()[:4]
    #     return context
    
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag, 
        'common_tags':common_tags,
        'posts':posts,
    }
    return render(request, 'blog/home.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'tags']

    def form_valid(self, form):
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.instance.author = self.request.user
        form.save_m2m()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'tags']

    def form_valid(self, form):
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.instance.author = self.request.user
        form.save_m2m()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})




