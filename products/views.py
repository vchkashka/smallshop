from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .forms import ProductForm
from django.views.generic import ListView, DetailView
from .models import Product, TagProduct, Category, CategoryDetails
from django.views.generic.edit import (CreateView,
                                       UpdateView, DeleteView)
from .utils import DataMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.decorators import permission_required


class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, DataMixin,
                 CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/addproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление товара'
    permission_required = 'products.add_product'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.seller = self.request.user
        return super().form_valid(form)


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    DataMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/addproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование товара'
    permission_required = 'products.change_product'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if product.seller != self.request.user:
            raise PermissionDenied("У вас нет прав для редактирования этого товара")
        return product


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    DataMixin, DeleteView):
    model = Product
    template_name = 'products/deleteproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление товара'
    permission_required = 'products.delete_product'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if product.seller != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого товара")
        return product


class ShowProduct(DataMixin, DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'
    template_name = 'products/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['product'])

    def get_object(self, queryset=None):
        return get_object_or_404(Product.published,
                                 slug=self.kwargs[self.slug_url_kwarg])


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        return Product.published.filter(title__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск товаров'
        context['query'] = self.request.GET.get('q', '').strip()
        return context


class ProductCategory(DataMixin, ListView):
    model = Product
    template_name = 'products/category_detail.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.published.filter(category__slug=self.kwargs[
            'category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products'][0].category
        return self.get_mixin_context(context,
                                      title='Категория - ' + category.name,
                                      cat_selected=category.pk,
                                      category=category
                                      )


class TagProductList(DataMixin, ListView):
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagProduct, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.name)

    def get_queryset(self):
        return Product.published.filter(tags__slug=self.kwargs['tag_slug'])


@permission_required(perm='products.can_mark_featured',
                     raise_exception=True)
def add_to_favorites(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.favorites.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@permission_required(perm='products.can_mark_featured',
                     raise_exception=True)
def remove_from_favorites(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.favorites.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@permission_required(perm='products.can_mark_featured',
                     raise_exception=True)
def favorite_products(request):
    favorites = request.user.favorite_products.all()
    return render(request, 'products/favorite_products.html',
                  {'favorites': favorites})


def manage_categories(request):
    categories = Category.objects.all()
    tags = TagProduct.objects.all()
    return render(request, 'products/manage_categories.html', {
        'categories': categories, 'tags': tags})


@permission_required(perm='products.add_category',
                     raise_exception=True)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('manage_categories')


@permission_required(perm='products.change_category',
                     raise_exception=True)
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    details, created = CategoryDetails.objects.get_or_create(category=category)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()

        details.description = request.POST.get('description', '')
        if 'banner_image' in request.FILES:
            details.banner_image = request.FILES['banner_image']
        details.save()

        return redirect('manage_categories')

    return render(request, 'products/edit_category.html',
                  {'category': category})


@permission_required(perm='products.delete_category',
                     raise_exception=True)
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('manage_categories')


@permission_required(perm='products.add_tagproduct',
                     raise_exception=True)
def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        TagProduct.objects.create(name=name)
        return redirect('manage_categories')
    return redirect('manage_categories')


@permission_required(perm='products.change_tagproduct',
                     raise_exception=True)
def edit_tag(request, pk):
    tag = get_object_or_404(TagProduct, id=pk)
    if request.method == 'POST':
        tag.name = request.POST.get('name')
        tag.save()
        return redirect('manage_categories')
    return render(request, 'products/edit_tag.html', {'tag': tag})


@permission_required(perm='products.delete_tagproduct',
                     raise_exception=True)
def delete_tag(request, pk):
    tag = get_object_or_404(TagProduct, id=pk)
    if request.method == 'POST':
        tag.delete()
    return redirect('manage_categories')
