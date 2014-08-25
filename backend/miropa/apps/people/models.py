from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.utils.constants import *
# Create your models here.


#===============================================================================
# Categories
#===============================================================================
from miropa.settings import MEDIA_URL


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/categories", null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)

    def get_url_image(self):
        return MEDIA_URL + '%s' % self.image
    url_image = property(get_url_image)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural='Categorias'

    @property
    def as_dict(self):
        """
        Returns object data as a dict

        :return: dict
        """
        category = {
            'id': self.id,
            'name': self.name,
            'image': str(self.url_image)
        }
        return category


#===============================================================================
# Products
#===============================================================================

class Product(models.Model):
    """
    A product
    Example"
    "Pant"
    "Shoes"
    """
    name = models.CharField(
        max_length=100
    )
    short_description = models.TextField()
    long_description = models.TextField()
    category = models.ManyToManyField(
        'Category'
    )
    stock = models.IntegerField(
        verbose_name=_('stock'), default=0
    )
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )
    slug = models.SlugField(
        max_length=120, unique=True
    )
    status = models.IntegerField(
        default=0, max_length=1, choices=PRODUCT_STATUS
    )
    date_created = models.DateField(
        auto_created=True,
        verbose_name=_('creation date')
    )
    last_modified = models.DateTimeField(
        auto_now_add=True
    )

    def get_url_image(self):
        return MEDIA_URL + '%s' % self.images
    url_image = property(get_url_image)

    def __unicode__(self):
        return str(self.name)

    @property
    def as_dic(self):
        """
        Return product data as a dict
        :return: dict
        """
        product = {
            'id': self.id,
            'name': self.name,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'category': self.category,
            'stock': self.stock,
            'unit_price': self.unit_price,
            'slug': self.slug,
            'is_active': self.active,
            'date_created': self.date_created,
            'last_modified': self.last_modified,
            'image': self.url_image,
            'tags': self.tags
        }
        return product

    class Meta:
        verbose_name = "Producto"


class ProductImage(models.Model):
    products = models.ForeignKey(
        'Product', related_name='images'
    )
    image = models.ImageField(
        upload_to="images/%Y/%m/%d", null=True
    )

    def __unicode__(self):
        return str(self.products)

    @property
    def as_dict(self):
        """
        Return object data as a dict
        :return: dict
        """
        product_image = {
            'id': self.id,
            'products': self.products,
            'image': self.image
        }
        return product_image


class ProductTag(models.Model):
    name = models.CharField(
        max_length=80, unique=True
    )
    products = models.ForeignKey(
        'Product', related_name='tags'
    )

    def __unicode__(self):
        return self.name

    @property
    def as_dict(self):
        """
        Returns object data as a dict

        :return: dict
        """
        product_tag = {
            'id': self.id,
            'name': self.name
        }
        return product_tag


#===============================================================================
# Variants
#===============================================================================

class OptionGroup(models.Model):
    """
    A logical group of options
    Example:

    "Colors"
    "Sizes"
    ""
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name="option_groups",
                                      blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_options(self):
        """
        A helper method to retrieve a list of options in this OptionGroup
        """
        options = Option.objects.filter(group=self)
        return options

    @property
    def as_dict(self):
        option_group = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'products': self.products
        }
        return option_group


class Option(models.Model):
    """
    A product option. Examples:

    "Red": 10$
    "Blue": 5$
    "M": 15$
    "XL": 25$
    ...
    """
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    ),
    group = models.ForeignKey(OptionGroup)

    def __unicode__(self):
        return self.name


#===============================================================================
# Stores
#===============================================================================

class Store(models.Model):
    name = models.CharField(
        max_length=120
    )
    follows = models.ManyToManyField(
        'UserProfile', verbose_name=_("Followers"), related_name="followed_by",
        symmetrical=False, null=True, blank=True
    )
    latitude = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )
    location = models.CharField(
        max_length=255, blank=True
    )
    user = models.ForeignKey(
        'UserProfile', verbose_name=_('Owner'), null=True, blank=True, related_name="owner"
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    image = models.ImageField(
        upload_to="images/stores", null=True, blank=True
    )

    def __unicode__(self):
        return self.name

    def get_url_image(self):
        return MEDIA_URL + '%s' % self.image
    url_image = property(get_url_image)

    @property
    def as_dict(self):
        store = {
            'id': self.id,
            'name': self.name,
            'follows': self.follows,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'location': self.location,
            'user': self.user,
            'image': self.url_image
        }
        return store

    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"


#===============================================================================
# Cart
#===============================================================================

class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

    def __unicode__(self):
        return unicode(self.creation_date)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('cart'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))

    def __unicode__(self):
        return u'%d units of %s' % (self.quantity, self.product.__class__.__name__)

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)

    @property
    def as_dict(self):
        cart_item = {
            'id': self.id,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total': self.total_price
        }
        return cart_item


class CartItemOption(models.Model):
    cart_item = models.ForeignKey(CartItem)
    option = models.ForeignKey(Option)


#===============================================================================
# Users
#===============================================================================

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, unique=True, related_name="user"
    )
    dni = models.CharField(
        max_length=8, verbose_name=_("DNI"), null=True, blank=True
    )
    sex = models.CharField(
        max_length=2, choices=SEX, verbose_name=_("Sexo"), null=True, blank=True
    )
    phone = models.CharField(
        max_length=11, verbose_name=_("Telefono"), null=True, blank=True
    )
    cellphone = models.CharField(
        max_length=11, verbose_name=_("Celular"), null=True, blank=True
    )
    thumb = models.ImageField(
        upload_to="images", null=True
    )
    birth_day = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username

    def get_url_image(self):
        return MEDIA_URL + '%s' % self.thumb
    url_image = property(get_url_image)

    @property
    def as_dict(self):
        """
        Return object data as a dict
        :return: dict
        """
        user = {
            'id': self.user,
            'email': self.user.email,
            'dni': self.dni,
            'sex': self.sex,
            'phone': self.phone,
            'cellphone': self.cellphone,
            'birth_day': self.birth_day,
            'thumb': self.url_image
        }
        return user

    class Meta:
        ordering=['-created']
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

@receiver(post_save, sender=User)
def create_favorites(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class UserPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        'UserProfile', related_name="posts"
    )
    date_created = models.DateTimeField(
        auto_now=True, blank=True, verbose_name=_('creation date')
    )
    url_video = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to="images/posts", null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_url_image(self):
        return MEDIA_URL + '%s' % self.image
    url_image = property(get_url_image)

    @property
    def as_dict(self):
        """
        Returns object data as a dict
        :return: dict
        """
        post = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author,
            'date_created': self.date_created,
            'url_video': self.url_video,
            'image': self.url_image
        }
        return post

    class Meta:
        verbose_name = "Post"