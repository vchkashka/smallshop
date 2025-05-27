from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import UserPassesTestMixin
from products.models import Product
from .forms import UploadFileForm
from products.utils import DataMixin
import uuid


# def index(request):
#     products = Product.published.all()
#     data = {
#         'title': 'Главная страница',
#         'products': products,
#         'cat_selected': 0,
#     }
#     return render(request, 'core/index.html', data)


class Home(DataMixin, ListView):
    def get_queryset(self):
        return Product.published.all()
    context_object_name = 'products'
    template_name = 'core/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title='Главная страница',
                                      cat_selected=0
                                      )


def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class AboutUs(UserPassesTestMixin, DataMixin, FormView):
    template_name = 'core/about.html'
    form_class = UploadFileForm
    success_url = '/about/'
    title_page = 'О нас'

    def form_valid(self, form):
        handle_uploaded_file(form.cleaned_data['file'])
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.groups.filter(
            name='Менеджеры').exists()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path())


class Contact(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'core/contact.html'
    title_page = 'Контактная информация'
