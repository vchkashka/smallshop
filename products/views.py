from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .models import Product, Category, TagProduct
from .forms import AddProductForm


def addproduct(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            # try:
            #     Product.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except Exception:
            #     form.add_error(None, 'Ошибка добавления товара')
            form.save()
            return redirect('home')
    else:
        form = AddProductForm()
    return render(request, 'products/addproduct.html',
                  {'title': 'Добавление товара', 'form': form})


def product_list(request):
    return HttpResponse("Список товаров")


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    # if product_id > 10:
    #     return redirect(reverse('home'))

    data = {
        'title': product.title,
        'product': product,
    }
    return render(request, 'products/detail.html', data)


def product_search(request):
    query = request.GET.get('q', '').strip()
    filtered_products = Product.published.all().filter(title__icontains=query)

    data = {
        'title': 'Поиск товаров',
        'products': filtered_products,
        'query': query,
    }
    return render(request, 'products/search.html', data)


def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.published.filter(category_id=category.pk)

    data = {
        'category': category,
        'cat_selected': category.pk,
        'products': products,
    }
    return render(request, 'products/category_detail.html', data)


def show_tag_productlist(request, tag_slug):
    tag = get_object_or_404(TagProduct, slug=tag_slug)
    products = tag.tags.filter(is_published=Product.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'products': products,
        'cat_selected': None,
    }

    return render(request, 'core/index.html', context=data)
