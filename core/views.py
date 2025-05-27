from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
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
    # template_name = 'core/index.html'
    context_object_name = 'products'

    # extra_context = {
    #     'title': 'Главная страница',
    #     'cat_selected': 0,
    # }
    template_name = 'core/index.html'

    # extra_context = {
    #     'title': 'Главная страница',
    #     'products': products,
    #     'cat_selected': 0,
    # }

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


# def about_us(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(form.cleaned_data['file'])
#     else:
#         form = UploadFileForm()
#     return render(request, 'core/about.html', {'title': 'О нас',
# 'form': form})


class AboutUs(DataMixin, FormView):
    template_name = 'core/about.html'
    form_class = UploadFileForm
    success_url = '/about/'
    title_page = 'О нас'

    def form_valid(self, form):
        handle_uploaded_file(form.cleaned_data['file'])
        return super().form_valid(form)

# def contact(request):
#     data = {
#         'title': 'Контактная информация',
#         }
#     return render(request, 'core/contact.html', data)


class Contact(DataMixin, TemplateView):
    template_name = 'core/contact.html'
    title_page = 'Контактная информация'
