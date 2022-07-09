from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='brands/logo/')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

    def image_tag(self):
        return mark_safe('<img src="%s" height="100"/>' % (self.image.url))


class Color(models.Model):
    name = models.CharField(max_length=25, unique=True, db_index=True)
    color_code = models.CharField(max_length=10, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def color_bg(self):
        return mark_safe(
            '<div style="width:30px;height:30px;background-color:%s"><div/>' % (self.color_code))


class Size(models.Model):
    size = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.size


class Product(models.Model):
    SEASONS = (
        ('demi_season', 'demi-season'),
        ('summer', 'summer'),
        ('winter', 'winter'),
    )
    vendor_code = models.CharField(max_length=100, unique=True, db_index=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    season = models.CharField(max_length=12, choices=SEASONS, default='demi-season', db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands')
    model = models.CharField(max_length=100, db_index=True)
    color = models.ManyToManyField(Color, related_name='colors')
    size = models.ManyToManyField(Size, related_name='sizes')
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('brand',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f'{self.brand.name} {self.model}'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product.model

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" height="50"/>')


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.product}'


class Banner(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=50)
    text = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='banner/posters/%Y/%m/%d', help_text='Image should be PNG')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Banner {self.product.brand} {self.product.model}'
