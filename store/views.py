
from django.shortcuts import  redirect

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from django.contrib import messages


class UserCreateView(CreateView):
    model = StoreUser
    form_class = StoreUserForm
    success_url = '/login'
    template_name = 'register.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return super().form_valid(form)


class SnusListView(ListView):
    model = Snus
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'create_form': SnusCreateForm(),
                     'purchase_form': SnusPurchaseForm() }
    paginate_by = 3


class Login(LoginView):
    template_name = 'login.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class SnusCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    login_url = 'login/'
    http_method_names = ['post']
    form_class = SnusCreateForm
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form=form)


class UpdateSnusView(PermissionRequiredMixin, UpdateView):
    model = Snus
    permission_required = 'is_superuser'
    login_url = 'login/'
    form_class = SnusUpdateForm
    success_url = '/'


class PurchaseSnusView(LoginRequiredMixin, CreateView):

    form_class = SnusPurchaseForm

    success_url = '/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        product = Snus.objects.get(id=self.request.POST['product_id'])
        customer = StoreUser.objects.get(id=self.request.POST['customer_id'])
        total_price = product.price * object.quantity
        if total_price > object.user.UserWallet:
            messages.add_message(self.request, messages.ERROR, 'You have not enough money!')
            return redirect('/')
        elif product.quantity < object.quantity:
            messages.add_message(self.request, messages.ERROR, 'Not enough {} at warehouse!'
                                 .format(product.title))
            return redirect('/')


        product.quantity -= object.quantity

        customer.UserWallet -= total_price
        object.product_id = self.request.POST['product_id']
        object.customer_id = self.request.POST['customer_id']

        object.save()
        customer.save()
        product.save()
        return super().form_valid(form=form)


class PurchasesListView(LoginRequiredMixin ,ListView):
    model = Purchase
    template_name = 'purchases.html'
    login_url = 'login/'
    paginate_by = 5
    extra_context = {'return_purchase_form': SnusReturnForm()}

    def get_queryset(self):
        return super().get_queryset().filter(customer= self.request.user).order_by('-id')


class ReturnSnusView(LoginRequiredMixin, CreateView):
    form_class = SnusReturnForm
    template_name = 'purchases.html'
    success_url = '/snus/purchase_list'



    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        snus_return = Purchase.objects.get(id=self.request.POST['purchase_return_id'])
        returns = ReturnPurchase.objects.filter(purchase_return=snus_return)
        if snus_return.purchase_time + timedelta(minutes=3) < datetime.now():
            messages.add_message(self.request, messages.ERROR, 'Sorry, but you have only 3 minutes to return '
                                                               'something')
            return redirect('/snus/purchase_list')
        elif returns:
            messages.add_message(self.request, messages.INFO, 'Your request already processed')
            return redirect('/snus/purchase_list')
        user = self.request.user
        object.purchase_return_id = self.request.POST['purchase_return_id']
        object.save()
        snus_return.save()
        user.save()
        return super().form_valid(form=form)

class ReturnsListView(LoginRequiredMixin, ListView):
    model = ReturnPurchase
    template_name = 'returns.html'
    login_url = 'login/'
    paginate_by = 5

class DeclineReturnView(DeleteView):
    model = ReturnPurchase
    success_url = '/snus/returns_list'


class AcceptReturnView(DeleteView):
    model = Purchase
    success_url = '/snus/returns_list'
    http_method_names = ['post']


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = Snus.objects.get(id=self.object.product_id)
        buyer = StoreUser.objects.get(id=self.object.customer.id)
        money_return = self.object.product.price * self.object.quantity
        product.quantity += self.object.quantity

        buyer.UserWallet += money_return


        buyer.save()
        product.save()

        return self.delete(request, *args, **kwargs)


