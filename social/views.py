from django.shortcuts import render, redirect

from django.views.generic import TemplateView

from .models import Post, Comment, Profile

from django.contrib.auth.models import User

from django.views import View

from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy

from .forms import PostForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        posts = Post.objects.all().order_by('-id')
        user = self.request.user

        
        context = {
            'form': form,
            'posts': posts,
        }

        return render(request, 'social/index.html', context)

    def post(self, request, *args, **kwargs):

        user = self.request.user

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()


        posts = Post.objects.all().order_by('-id')
        context = {
            'form': form,
            'posts': posts
        }

        return redirect('index')

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        context = {'post': post}

        return render(request, 'social/post_detail.html', context)

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'social/post_delete.html'
    model = Post
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'social/post_edit.html'
    model = Post
    fields = ['body']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})

    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
        
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = request.user

        posts = Post.objects.filter(author=user).order_by('-id')

        context = {
            'profile': profile,
            'posts': posts
        }

        return render(request, 'social/profile.html', context)