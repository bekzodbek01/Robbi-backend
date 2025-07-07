from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view
from .models import General, Category, RestaurantFilter, ParkFilter, KalinkaFilter, Region
from django.db.models import Q


@api_view(['GET'])
def city_list(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True, context={'request': request})
    return Response(serializer.data)


class RegionListAPIView(APIView):
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializers(regions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegionWithCitiesAPIView(APIView):
    def get(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
        except Region.DoesNotExist:
            return Response({"error": "Region topilmadi"}, status=404)

        # Regionni serialize qilamiz
        region_data = {
            "id": region.id,
            "title": region.title,
            "cities": []
        }

        # Shu regionga tegishli barcha tumonlarni qo‘shamiz
        cities = City.objects.filter(region=region)
        for city in cities:
            region_data["cities"].append({
                "id": city.id,
                "title": city.title
            })

        return Response({
            "region": region_data
        })


@api_view(['GET'])
def RestaurantFilter_list(request):
    restaurant = RestaurantFilter.objects.all()
    serializer = RestaurantFilterSerializer(restaurant, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def ParkFilter_list(request):
    park = ParkFilter.objects.all()
    serializer = ParkFilterSerializer(park, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def KalinkaFilter_list(request):
    kalinka = KalinkaFilter.objects.all()
    serializer = KalinkaFilterSerializer(kalinka, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def General_list(request):
    general = General.objects.all()
    serializer = GeneralSerializer(general, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(['GET'])
def category_list(request):
    category = Category.objects.all()
    serializer = CategoryeSerializer(category, many=True, context={'request': request})
    return Response(serializer.data)


from django.db.models import Prefetch


class MenuCategoryListView(APIView):
    def get(self, request, id):
        # Filtrlangan MenuItem queryset
        menu_items = MenuItem.objects.filter(general_id=id)

        # Prefetch bilan MenuCategory ichida faqat shu locationdagi itemlarni olib kelish
        categories = MenuCategory.objects.filter(
            items__general_id=id
        ).distinct().prefetch_related(
            Prefetch('items', queryset=menu_items)
        )

        serializer = MenuCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


import django_filters
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import General
from .serializers import GeneralSerializer


class GeneralFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category__id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    open_now = django_filters.BooleanFilter(method='filter_open_now')
    delivery_available = django_filters.BooleanFilter(field_name='delivery_available')
    tier = django_filters.MultipleChoiceFilter(field_name='tier', choices=General.TIER_CHOICES)
    star_rating = django_filters.RangeFilter(field_name='star_rating')
    rest_filter__name = django_filters.CharFilter(field_name='rest_filter__name', lookup_expr='icontains')
    kalinka_filter__name = django_filters.CharFilter(field_name='kalinka_filter__name', lookup_expr='icontains')
    park_filter__name = django_filters.CharFilter(field_name='park_filter__name', lookup_expr='icontains')
    region = django_filters.NumberFilter(field_name='region__id')
    city = django_filters.NumberFilter(field_name='city__id')

    class Meta:
        model = General
        fields = [
            'name',
            'open_now',
            'delivery_available',
            'tier',
            'star_rating',
            'rest_filter__name',
            'kalinka_filter__name',
            'park_filter__name',
            'region',
            'city',
            'category',
        ]

    def filter_open_now(self, queryset, name, value):
        if value:
            from django.utils.timezone import localtime, now
            current_time = localtime(now()).time()
            return queryset.filter(open_time__lte=current_time, close_time__gte=current_time)
        return queryset


class GeneralListAPIView(generics.ListAPIView):
    queryset = General.objects.all()
    serializer_class = GeneralSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GeneralFilter
    search_fields = ['name']  # nom bo‘yicha qidirish
    ordering_fields = ['open_time', 'close_time', 'star_rating']


@api_view(['GET'])
def generals_by_category(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response({"error": "Category topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    generals = General.objects.filter(category_id=pk)
    serializer = GeneralSerializer(generals, many=True, context={'request': request})

    return Response({
        "category_name": category.name,
        'id': category.id,
        "generals": serializer.data
    })
