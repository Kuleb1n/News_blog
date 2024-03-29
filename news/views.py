from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, Category, User, Rating
from .forms import AddNewsForm, RegisterUserForm, ChangeUserForm, RatingForm


class NewsIndex(ListView):
    paginate_by = 4
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category', 'user')

    def get_context_data(self, **kwargs):
        context = super(NewsIndex, self).get_context_data()
        context['rating'] = Rating.objects.all().select_related()

        return context


class ShowNewsByCategory(ListView):
    paginate_by = 4
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'],
                                   is_published=True).select_related('category', 'user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(Category.objects.get(slug=self.kwargs['category_slug']))
        return context


class ShowNews(DetailView):
    model = News
    template_name = 'news/show_news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()

        return context


class AddNews(CreateView):
    form_class = AddNewsForm
    template_name = 'news/add_news.html'


class DeleteNews(DeleteView):
    model = News
    slug_url_kwarg = 'news_slug'
    template_name = 'news/delete_news.html'
    success_url = reverse_lazy('profile')


class UpdateNews(UpdateView):
    model = News
    slug_url_kwarg = 'news_slug'
    fields = ['photo', 'content']
    template_name = 'news/update_news.html'


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


class DeleteAccount(DeleteView):
    model = User
    pk_url_kwarg = 'account_pk'
    template_name = 'news/delete_account.html'
    success_url = reverse_lazy('login')


def logout_us(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    news = News.objects.filter(user=request.user.id).select_related('category')
    content = {
        'news': news,
    }
    return render(request, 'news/profile.html', content)


class ChangeUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'news/change_user.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('profile')
    success_message = 'User data changed'

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.user_id = None

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


class ShowProfile(DetailView):
    model = User
    template_name = 'news/show_profile.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'user'


class AddStarRating(View):

    @staticmethod
    def post(request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user_id=request.user.pk,
                news_id=int(request.POST.get("news")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
