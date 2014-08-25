from django.contrib import admin
from .models import Category, ProductTag, Cart, ProductImage, UserProfile, CartItem, \
    CartItemOption, OptionGroup, Option, Product, Store, UserPost


class UserProfileAdmin(admin.ModelAdmin):
    def user_email(self, instance):
        return instance.user.email

    user_email.short_description = "Correo electronico"

    def get_thumb(self, instance):
        url = instance.url_image
        tag = "<img width='50' src='%s'>" % url
        return tag

    get_thumb.allow_tags = True
    get_thumb.short_description = "Thumb"
    list_display = ('user', 'user_email', 'dni', 'sex', 'phone', 'cellphone',
                    'birth_day', 'created', 'get_thumb',)


admin.site.register(UserProfile, UserProfileAdmin)


class UserPostAdmin(admin.ModelAdmin):
    def get_image(self, instance):
        url = instance.url_image
        tag = "<img width='50' src='%s'>" % url
        return tag
    get_image.allow_tags = True
    get_image.short_description = "Imagen"
    list_display = ('title', 'description', 'author', 'url_video', 'date_created', 'get_image',)

admin.site.register(UserPost, UserPostAdmin)


class StoreAdmin(admin.ModelAdmin):
    def follows_name(self, instance):
        return ", ".join([x.__str__() for x in instance.follows.all()])
    def get_image(self, instance):
        url = instance.url_image
        tag = "<img width='50' src='%s'>" % url
        return tag
    get_image.allow_tags = True
    get_image.short_description = "Imagen"
    follows_name.short_description = 'Seguidores'
    list_display = ('name', 'follows_name', 'latitude', 'longitude', 'location', 'user', 'get_image',)


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    def get_image(self, instance):
        url = instance.url_image
        tag = "<img width='50' src='%s'>" % url
        return tag

    get_image.allow_tags = True
    get_image.short_description = "Imagen"

    list_display = ('name', 'get_image',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    def get_image(self, instance):
        url = instance.url_image
        tag = "<img width='50' src='%s'>" % url
        return tag

    get_image.allow_tags = True
    get_image.short_description = "Imagen"

    def categories_name(self, instance):
        return ", ".join([x.__str__() for x in instance.category.all()])

    categories_name.short_description = 'Categoris'

    def tags_name(self, instance):
        return ", ".join([x.__str__() for x in instance.tags.all()])

    tags_name.short_description = 'Tags'

    list_display = ('name', 'short_description', 'categories_name', 'tags_name',
                    'stock', 'unit_price', 'slug', 'status', 'last_modified', 'get_image',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductTag)
admin.site.register(OptionGroup)
admin.site.register(Option)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CartItemOption)

