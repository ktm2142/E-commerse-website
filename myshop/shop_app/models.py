from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchVectorField


class Category(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='category_images', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    available = models.BooleanField(default=True)
    search_vector = SearchVectorField(null=True)

    def search(self, query):
        query_vector = SearchQuery(query)
        return self.objects.annotate(search=SearchVector('title', 'description')).filter(search=query_vector)

    class Meta:
        indexes = [
            GinIndex(fields=['title'], opclasses=['gin_trgm_ops'], name='product_title_gin_idx'),
            GinIndex(fields=['description'], opclasses=['gin_trgm_ops'], name='product_desc_gin_idx'),
        ]
        ordering = ('category', 'title',)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Product)
def update_search_vector(sender, instance, **kwargs):
    Product.objects.filter(pk=instance.pk).update(
        search_vector=SearchVector('title', 'description')
    )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                  message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        ],
        default='')
    email = models.EmailField(default='')
    address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order #(pk={self.pk}, user={self.user.username})"

    @property
    def total_price(self):
        return sum(order_item.total_price for order_item in self.order_items.all())

    def delete(self, *args, **kwargs):
        self.order_items.all().delete()
        super().delete(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    @property
    def total_price(self):
        return self.price * self.quantity


# @receiver(post_delete, sender=OrderItem)
# def handle_order_item_delete(sender, instance, **kwargs):
#     order = instance.order
#     if not order.order_items.exists():
#         order.delete()
