from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(primary_key=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               related_name='children',
                               blank=True, null=True)

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

    def __str__(self):
        if self.parent:
            return f'{self.parent} --> {self.title}'
        return self.title


class Product(models.Model):
    STATUS_CHOICES = (
        ('in stock', 'В наличии'),
        ('out of stock', 'Нет в наличии'),
        ('await', 'Ожидается')
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'product_id': self.pk})


    class Meta:
        ordering = ['-id', ]



class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', verbose_name='Product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='User')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user} has left review on product: {self.product}'

    class Meta:
        ordering = ['-created']












