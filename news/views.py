from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import News, Category, User
from .forms import AddNewsForm, RegisterUserForm, ChangeUserForm


class NewsIndex(ListView):
    paginate_by = 3
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class ShowNewsByCategory(ListView):
    paginate_by = 3
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True).select_related(
            'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(Category.objects.get(slug=self.kwargs['category_slug']))
        return context


class ShowNews(DetailView):
    model = News
    template_name = 'news/show_news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'


class AddNews(CreateView):
    form_class = AddNewsForm
    template_name = 'news/add_news.html'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    template_name = 'news/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


def logout_us(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    return render(request, 'news/profile.html')


class ChangeUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'news/change_user.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk

        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()

        return get_object_or_404(queryset, pk=self.user_id)


class PasswordChange(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'news/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = "The user's password has been changed"
