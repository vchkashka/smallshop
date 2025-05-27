from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Product, TagProduct
from django.views.generic.edit import (CreateView,
                                       UpdateView, DeleteView)
from .utils import DataMixin
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)


# def addproduct(request):
#     if request.method == 'POST':
#         form = AddProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Product.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except Exception:
#             #     form.add_error(None, 'Ошибка добавления товара')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddProductForm()
#     return render(request, 'products/addproduct.html',
#                   {'title': 'Добавление товара', 'form': form})


# class AddProduct(View):
#     def get(self, request):
#         form = AddProductForm()
#         return render(request, 'products/addproduct.html',
#                       {'title': 'Добавление товара', 'form': form})

#     def post(self, request):
#         form = AddProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return render(request, 'products/addproduct.html',
#                       {'title': 'Добавление товара', 'form': form})


# class AddProduct(FormView):
#     form_class = AddProductForm
#     template_name = 'products/addproduct.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'title': 'Добавление товара',
#     }

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


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


class UpdateProduct(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Product
    fields = ['title', 'content', 'price', 'image', 'is_published', 'category']
    template_name = 'products/addproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование товара'
    permission_required = 'products.change_product'


class DeleteProduct(DataMixin, DeleteView):
    model = Product
    template_name = 'products/deleteproduct.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление товара'


# def product_detail(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#     # if product_id > 10:
#     #     return redirect(reverse('home'))

#     data = {
#         'title': product.title,
#         'product': product,
#     }
#     return render(request, 'products/detail.html', data)


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


# def product_search(request):
#     query = request.GET.get('q', '').strip()
#     filtered_products = Product.published.all().filter(
# title__icontains=query)

#     data = {
#         'title': 'Поиск товаров',
#         'products': filtered_products,
#         'query': query,
#     }
#     return render(request, 'products/search.html', data)


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


# def category_detail(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     products = Product.published.filter(category_id=category.pk)

#     data = {
#         'category': category,
#         'cat_selected': category.pk,
#         'products': products,
#     }
#     return render(request, 'products/category_detail.html', data)


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


# def show_tag_productlist(request, tag_slug):
#     tag = get_object_or_404(TagProduct, slug=tag_slug)
#     products = tag.tags.filter(is_published=Product.Status.PUBLISHED)
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'products': products,
#         'cat_selected': None,
#     }

#     return render(request, 'core/index.html', context=data)


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
