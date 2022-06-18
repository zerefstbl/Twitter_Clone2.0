from django.shortcuts import render, redirect

from django.views.generic import TemplateView

from .models import Post, Comment, Profile

from django.contrib.auth.models import User

from django.views import View

from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from django.urls import reverse_lazy

from django.db.models import Q

from .forms import CommentForm

from .forms import PostForm

from .models import Notifications

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = PostForm()

        profiles = Profile.objects.all().order_by('-pk')

        notification = Notifications.objects.filter(to_user=request.user)
        
        seguindo = Profile.objects.get(pk=request.user.pk)

        

        logged_in_user = request.user

        posts = Post.objects.filter(
            author__profile__followers__in=[
                logged_in_user.id
            ]
        ).order_by('-id')

        context = {
            'form': form,
            'posts': posts,
            'profiles': profiles,
            'seguindo': seguindo,
        }

        
        return render(request, 'social/index.html', context)

    def post(self, request, *args, **kwargs):

        user = self.request.user

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()


        home = Profile.objects.get(user=request.user)

        home.teste.add(request.user)

        posts = Post.objects.all().order_by('-id')
        context = {
            'form': form,
            'posts': posts
        }

        return redirect('index')

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        form = CommentForm()

        comments = Comment.objects.filter(post=post)

        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }

        return render(request, 'social/post_detail.html', context)


    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        return redirect('post_detail', post.pk)


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

        posts = Post.objects.filter(author=profile.user).order_by('-id')

        is_following = False

        followers = profile.followers.all()


        count_followers = len(followers) - 1


        for follower in followers:
            if follower == user:
                is_following = True
                break
            else:
                is_following = False



        context = {
            'profile': profile,
            'posts': posts,
            'is_following': is_following,
            'count_followers': count_followers,
            'followers': followers,
        }


        return render(request, 'social/profile.html', context)

class ProfileEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'social/post_edit.html'
    model = Profile
    fields = ['name', 'bio', 'birth_date', 'picture']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
        

class AddFollowerView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):

        profile = Profile.objects.get(pk=pk)

        profile.followers.add(request.user)

        i = Profile.objects.get(pk=request.user.pk)

        i.following.add(profile.pk)

        notification = Notifications.objects.create(to_user=request.user, from_user=profile.user, notification_type=1)


        profile.teste.add(profile.pk)

        return redirect('profile', pk=profile.pk)

    
class DeleteFollowerView(View):
    def post(self, request, pk, *args, **kwargs):
        user = request.user

        profile = Profile.objects.get(pk=pk)

        notification = Notifications.objects.filter(to_user=request.user)

        notification.delete()

        profile.followers.remove(user)

        i = Profile.objects.get(pk=request.user.pk)

        i.following.remove(profile.pk)


        return redirect('profile', pk=profile.pk)

class AddLikeView(View):
    def post(self, request, pk, *args, **kwargs):

        post = Post.objects.get(pk=pk)

        is_like = False

        likes = post.likes.all() 

        for like in likes:
            if like == request.user:
                is_like = True 
                break
            else:
                is_like = False

        if is_like == True:
            post.likes.remove(request.user)

        if is_like == False:
            post.likes.add(request.user)

        

        return redirect('index')


class SearchProfileView(View):
    def post(self, request, *args, **kwargs):

        return render(request, 'social/search.html')


    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        
        try:
            search_results = Profile.objects.filter(
                Q(user__username__icontains=query)
            ).order_by('-pk')
            context = {
            'search_results': search_results
        }
            return render(request, 'social/search.html', context)
        except:
            return render(request, 'social/search.html')
            

class NotificationView(View):
    def get(self, request, pk, *args, **kwargs):
        notifications = Notifications.objects.filter(from_user=request.user).order_by('-date')

        context = {
            'notifications': notifications,
        }

        return render(request, 'social/notification.html', context)

    
        



        

