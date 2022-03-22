from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView # импортируем уже знакомый generic 
 
from .models import Product, Category
from .filters import ProductFilter  # импортируем недавно написанный фильтр
from .forms import ProductForm
 
# Create your views here.
 
class Products(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1  # поставим постраничный вывод в один элемент
    # form_class = ProductForm # добавляем форм класс, чтобы получать доступ к форме через метод POST
 
 
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
          # вписываем наш фильтр в контекст
        # context['categories'] = Category.objects.all()
        # context['form'] = ProductForm()
        return context

# дженерик для получения деталей о товаре
class ProductDetailView(DetailView):
    template_name = 'productDetail.html'
    queryset = Product.objects.all()

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreateView(CreateView):
    template_name = 'productCreate.html'
    form_class = ProductForm

# дженерик для редактирования объекта
class ProductUpdateView(UpdateView):
    template_name = 'productCreate.html'
    form_class = ProductForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)
 
 
# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'productDelete.html'
    queryset = Product.objects.all()
    success_url = '/products/'