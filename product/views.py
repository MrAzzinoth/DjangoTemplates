from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import *



from .forms import CreateProductForm, UpdateProductForm, CreateCommentForm
from .models import Category, Product, Comment


class SearchListView(ListView):
    model = Product
    template_name = 'product/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return queryset


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'


class ProductListView(ListView):
    model = Product
    template_name = 'categories-grid.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('slug')
        queryset=queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('slug')
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'product/create_product.html'
    form_class = CreateProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product/update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    pk_url_kwarg = 'product_id'

    def get_success_url(self):
        from django.urls import reverse
        return reverse('categori')

class CommentPage(ListView):
    model = Comment
    template_name = 'product/comment_list.html'
    context_object_name = 'list_comments'


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'product/comment.html'
    form_class = CreateCommentForm

    def form_valid(self, form):
        product = self.kwargs['product_id']
        user = self.request.user
        print(product)
        product = Product.objects.get(id=product)
        comment = form.save(commit=False)
        comment.product = product
        comment.user = user
        comment.save()
        return super().form_valid(form)

    success_url = reverse_lazy('categori')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = self.get_form(self.get_form_class())
        return context


#Shopping CartViews

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("categori")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url='account/login/')
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')




