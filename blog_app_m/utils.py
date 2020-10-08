from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseFormSet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from .models import *

class ObjectDetailMixin(FormMixin,DetailView):
    form_class = None
    model = None
    template = None

    def get_success_url(self,**kwargs):
        return reverse_lazy('post_detail_url', args={self.get_object().slug})

    def get(self, request, slug):
        form = self.form_class
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj,'form':form})

    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ObjectCreateMixin(LoginRequiredMixin):

    model_form = None
    template = None

    def get(self,request):
        form = self.model_form()
        return render(request,self.template,context={'form':form})

    def post(self, request):
        image = request.FILES
        bound_form = self.model_form(request.POST, image)
        if bound_form.is_valid():
            new_obj = bound_form.save(commit=False)
            new_obj.author = self.request.user
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template,context={'form':bound_form})

class ObjectUpdateMixin(LoginRequiredMixin,BaseFormSet):
    model = None
    model_form = None
    template = None


    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        instance = bound_form.save(commit=False)
        author = instance.author
        if self.request.user != author:
             return self.handle_no_permission()
        return render(request, self.template, context={'form': bound_form,self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST,instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form':bound_form, self.model.__name__.lower(): obj})

class ObjectDeleteMixin(LoginRequiredMixin):
    model = None
    model_form = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)

        bound_form = self.model_form(instance=obj)
        instance = bound_form.save(commit=False)
        author = instance.author
        if self.request.user != author:
            return self.handle_no_permission()

        return render(request, self.template, context={self.model.__name__.lower():obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))

