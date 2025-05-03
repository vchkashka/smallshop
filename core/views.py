from django.shortcuts import render
from products.models import Product
from .forms import UploadFileForm
import uuid


def index(request):
    products = Product.published.all()
    data = {
        'title': 'Главная страница',
        'products': products,
        'cat_selected': 0,
    }
    return render(request, 'core/index.html', data)


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


def about_us(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'core/about.html', {'title': 'О нас', 'form': form})


def contact(request):
    data = {
        'title': 'Контактная информация',
        }
    return render(request, 'core/contact.html', data)
