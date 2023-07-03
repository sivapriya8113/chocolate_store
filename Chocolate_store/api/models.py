from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=False,blank=True,null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class Chocolate(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='chocolates', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    price = models.FloatField(null=True, blank=True)
    image_url = models.URLField(max_length=2083)
    choco_available = models.BooleanField()
    is_deleted = models.BooleanField()

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title


class Carts(models.Model):
    product = models.ForeignKey(Chocolate, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    options = (
        ('in-cart', 'in-cart'),
        ('order-placed', 'order-placed'),
        ('removed', 'removed')
    )
    status = models.CharField(max_length=100, choices=options, default='in-cart')
