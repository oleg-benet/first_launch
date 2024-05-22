from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .filters import PostFilter
from .forms import PostForm
from .models import Post

class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'post_search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == "/articles/create":
            post.post_kind = "ART"
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = self.request.path
        return context


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    pk_url_kwarg = 'id'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('post_list')
