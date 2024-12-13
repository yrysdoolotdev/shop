from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=True, null=True, blank=True,
                                           validators=[MinValueValidator(15), MaxValueValidator(100)])
    phone = PhoneNumberField(null=True, blank=True, region='KG')
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    STATUS_CHOICES = (
        ('gold', 'gold'),
        ('silver', 'silver'),
        ('bronze', 'bronze'),
        ('simple', 'simple')
    )
    status = models.CharField(choices=STATUS_CHOICES, default='simple', max_length=16)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.PositiveIntegerField()
    check_original = models.BooleanField(default=True)
    product_video = models.FileField(upload_to='product_videos/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.product_name

    def get_avg_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum([i.start for i in ratings]) / ratings.count(), 1)
        return 0

    def get_count_people(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.count()
        return 0


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='product_images/')


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    start = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.user}, {self.start}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_review')
    product = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='product_review')
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.product}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.items.all())
        discount = 0

        if self.user.status == 'gold':
            discount = 0.75
        elif self.user.status == 'silver':
            discount = 0.50
        elif self.user.status == 'bronze':
            discount = 0.25

        final_price = total_price * (1 - discount)
        return final_price


class CarItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

