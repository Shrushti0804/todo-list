from django.shortcuts import render,redirect
from django.views.generic.list import ListView    #class based views
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView ,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy   #redirects user to certain part of page

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm   #creates user 
from django.contrib.auth import login  #redirects the newly registered user directly to dashboard instead of forcing him to login


from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name='base/login.html'
    fields='__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks')

    #to redirect the user after registeration form is submitted
    def form_valid(self,form):
        user=form.save()   #once the form is saved , the return value is gonna be the user 
        if user is not None:  #if user is authenticated , go ahead and use the login fun
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

#once the user is registered / logged in , he should be restricted to access login view and register page.
#redirect_authenticated_user=True should do this work, but it is not working for some reasons , so :

    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args,**kwargs)




class TaskList(LoginRequiredMixin ,ListView):   #this will look for task_list.html in templates
    #LoginRequiredMixin will block the view if user is not logged in    
    model=Task
    context_object_name='tasks'

    #to ensure that the logged in user gets his correct data
    def get_queryset(self):
        query_set= super().get_queryset()
        return  query_set.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] =context['tasks'].filter(user=self.request.user) 
        context['count'] =context['tasks'].filter(complete=False).count()  #to know the count of complete items
      

        return context
    

class TaskDetail(LoginRequiredMixin , DetailView):  #this will look for task_detail.html in templates
    model=Task
    context_object_name='task'
    template_name='base/task.html'    #instead of using task_detail.html we can use the name task.html with this command
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    #fields='__all__'   #takes all the fields from model task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')  #if everything goes well , redirect the user to another page

    #to ensure the task is added for the correct user
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form) 

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model=Task
    #fields='__all__'   #takes all the fields from model task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')  #if everything goes well , redirect the user to another page

class DeleteView(LoginRequiredMixin, DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')



