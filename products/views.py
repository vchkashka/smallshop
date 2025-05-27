from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Product, TagProduct
from django.views.generic.edit import (CreateView,
                                       UpdateView, DeleteView)
from .utils import DataMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.decorators import permission_required


class AddProduct(LoginRequiredMixin, PermissionRequiredMixin, DataMixin,
                 CreateView):
    model = Product
    fields = ['title', 'content', 'price', 'image', 'is_published', 'category',
              'tags']
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
    fields = ['title', 'content', 'price', 'image', 'is_published', 'category']
    template_name = 'products/addproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование товара'
    permission_required = 'products.change_product'


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    DataMixin, DeleteView):
    model = Product
    template_name = 'products/deleteproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление товара'
    permission_required = 'products.delete_product'


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
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Product.published.filter(tags__slug=self.kwargs['tag_slug'])


@permission_required(perm='products.can_mark_featured_product',
                     raise_exception=True)
def add_to_favorites(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.favorites.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@permission_required(perm='products.can_mark_featured_product',
                     raise_exception=True)
def remove_from_favorites(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.favorites.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@permission_required(perm='products.can_mark_featured_product',
                     raise_exception=True)
def favorite_products(request):
    favorites = request.user.favorite_products.all()
    return render(request, 'products/favorite_products.html',
                  {'favorites': favorites})
