from django.views.generic import ListView, DetailView, CreateView
from .models import News
from .forms import AddNewsForm


class NewsIndex(ListView):
    paginate_by = 3
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class ShowNewsByCategory(ListView):
    paginate_by = 3
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = str(context['news'][0].category)
        return context


class ShowNews(DetailView):
    model = News
    template_name = 'news/show_news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'


class AddNews(CreateView):
    form_class = AddNewsForm
    template_name = 'news/add_news.html'
