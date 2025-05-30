
from .models import General, MenuCategory, MenuItem, GeneralImage
from rest_framework import serializers
from .models import Region, City, Category, ParkFilter, KalinkaFilter, RestaurantFilter
from datetime import datetime
from django.utils.timezone import localtime, now
import django_filters

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class RegionSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'title', 'cities']


class GeneralimageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralImage
        fields = ['id', 'image']


class RestaurantFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantFilter
        fields = ['id', 'name']


class KalinkaFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KalinkaFilter
        fields = ['id', 'name']


class ParkFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkFilter
        fields = ['id', 'name']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'image']


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'items']


class GeneralSerializer(serializers.ModelSerializer):
    images = GeneralimageSerializer(many=True, read_only=True)
    menu_categories = serializers.SerializerMethodField()
    open_now = django_filters.BooleanFilter(method='filter_open_now')

    class Meta:
        model = General
        fields = [
            'id', 'name', 'image', 'address', 'phone', 'lat', 'long', 'description', 'open_time', 'close_time',
            'tier', 'star_rating', 'delivery_available', 'region', 'city', 'images', 'menu_categories'
        ]
        depth = 1

    def get_menu_categories(self, obj):
        categories = MenuCategory.objects.filter(items__general=obj).distinct()
        return MenuCategorySerializer(categories, many=True).data

    def filter_open_now(self, queryset, name, value):
        if value:  # ?open_now=true bo'lsa
            current_time = localtime(now()).time()  # hozirgi mahalliy vaqtni olamiz
            return queryset.filter(
                open_time__lte=current_time,
                close_time__gte=current_time
            )
        return queryset


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]


class CategoryeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name',]
