from django.views.generic.edit import FormView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from products.models import Product
from .models import Feedback
from .forms import UploadFileForm, FeedbackForm
from products.utils import DataMixin
from django.conf import settings
from django.shortcuts import redirect
import uuid
import os


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
    name, ext = os.path.splitext(f.name)
    suffix = str(uuid.uuid4())
    upload_dir = settings.MEDIA_ROOT / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)

    upload_path = upload_dir / f"{name}_{suffix}{ext}"
    with open(upload_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class UploadFileView(UserPassesTestMixin, FormView):
    template_name = 'core/upload.html'
    form_class = UploadFileForm
    success_url = '/about/'

    def form_valid(self, form):
        handle_uploaded_file(form.cleaned_data['file'])
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.groups.filter(name='Менеджеры').exists()

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path())


class AboutUs(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploads_dir = settings.MEDIA_ROOT / 'uploads'
        if uploads_dir.exists():
            files = os.listdir(uploads_dir)
            context['uploaded_files'] = [settings.MEDIA_URL + 'uploads/' + f for f in files]
        else:
            context['uploaded_files'] = []
        context['form'] = UploadFileForm()
        return context


class Contact(LoginRequiredMixin, TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FeedbackForm()
        context['feedbacks'] = Feedback.objects.order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('contact')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
