from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Food

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

# Create your views here.

class Home(LoginRequiredMixin, ListView):
    template_name = 'caloriecounter/index.html'
    model = Food
    def get_queryset(self):
        allFoods = Food.objects.all()
        total = 0
        for food in Food.objects.all():
            total += food.calories
        return [allFoods, total]

class Welcome(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'caloriecounter/welcome.html'

class FoodIndex(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'caloriecounter/list_foods.html'
    def get_queryset(self):
        queryset = Food.objects.all()
        return queryset

class FoodCreate(LoginRequiredMixin, CreateView):
    model = Food
    fields = ('name', 'calories')
    template_name = 'caloriecounter/Add_Food.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FoodUpdate(LoginRequiredMixin, UpdateView):
    model = Food
    fields = ('name','calories')

class FoodDelete(LoginRequiredMixin, DeleteView):
    model = Food
    success_url = '/caloriecounter/'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # create user object
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # add user to the database
      user = form.save()
      # logging user in via code
      login(request, user)
      return redirect('caloriecounter/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
