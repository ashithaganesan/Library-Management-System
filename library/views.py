from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView
from django.views import View
from .forms import SignUpForm, LoginForm, BookForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from .models import Book
# from django.urls import reverse

""" 
TODO
1. add separate template views for admin and member dashboard and then after login redirect to those views instead of a template. add those to urls.py
2. how to 
"""

# Create your views here.
class HomeView(TemplateView):
    template_name = 'library/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context["books"] = books
        return context
    
class DetailedBookView(DetailView):
    template_name = "library/single_book.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()  
        return render(request, "library/signup.html", {
            'form_info': form
        })
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data["username"]
            email_id = form.cleaned_data["email_id"]
            password = form.cleaned_data["password"]

            if len(password) < 8 or password.isnumeric():
                error_message = '''
                Your password is weak:
                Your password must contain atleast 8 characters.
                Your password cannot be entirely numeric.'''
                return render(request, "library/signup.html", {
                    "form_info": form,
                    "error_message": error_message
                })
        
            if User.objects.filter(username=username):
                error_message = "Username already exists!"
                return render(request, "library/signup.html", {
                    "form_info": form,
                    "error_message": error_message
                })
            
            if User.objects.filter(email=email_id).exists():
                error_message = "Email already exists!"
                return render(request, "library/signup.html", {
                    "form_info": form,
                    "error_message": error_message
                })

            user = User.objects.create_user(username, email_id, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = True
            group = Group.objects.get(name='MEMBER')
            user.groups.add(group)

            user.save()
            
            success_message = "Account has been successfully created!"
            return render(request, "library/signup.html", {
                "form_info": SignUpForm(),
                "success_message": success_message
            })
        
        return render(request, "library/signup.html", {
            'form_info': form
        })
    
def is_admin(user):
    return user.groups.filter(name='Librarian').exists()

def is_member(user):
    return user.groups.filter(name='Member').exists()
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "library/login.html", {
            'form_info': form
        })
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                books = Book.objects.all()
                login(request, user)
                fname = user.first_name
                if is_admin(request.user):
                    return HttpResponseRedirect("/admin-view")
                
                elif is_member(request.user):
                    # request.session['name'] = fname
                    # return redirect("app:MemberView")
                    return HttpResponseRedirect("/member-view")

            else:
                error_message = "Invalid login credentials!"
                return render(request, "library/login.html", {
                    'form_info': form, 
                    'error_message': error_message
                    })
            
        return render(request, "library/login.html", {
            'form_info': form
        })
    
def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/")

class AdminView(TemplateView):
    template_name = "library/admin_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context["books"] = books
        return context
    
class MemberView(TemplateView):
    template_name = "library/member_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context["books"] = books
        return context
    
@login_required
def CreateBookView(request):
    form=BookForm()
    if request.method=='POST':
        form=BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            books = Book.objects.all()
            return render(request,'library/admin_view.html', {
                "books": books
            })
        
    return render(request,'library/create.html', {
        'form':form
    })

@login_required
def editBook(request, id):
    data = Book.objects.get(id=id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('admin_view')   
        
    form = BookForm(instance=data)
    return render(request, "library/edit_book.html", {
        'form': form
    })

@login_required
def deleteBook(request, id):
    data = Book.objects.get(id=id)
    if request.method == "POST":
        data.delete()
        books = Book.objects.all()
        return HttpResponseRedirect('admin_view')
    
    return render(request, "library/delete_book.html", {
        "data": data
    })

