from django.urls import path
from .views import *
from .nomoz_vaqtlar import NamozVaqtlariAPIView

urlpatterns = [
    path('city/', city_list, name='city_list'),  # Shahar ro'yxati
    path('regions/<int:pk>/in_city/', RegionWithCitiesAPIView.as_view(), name='region_in_city'),
    path('regions/', RegionListAPIView.as_view(), name='region-list'),
    path('generals/', General_list, name='lgeneral_list'),
    path('generals/<int:pk>/', generals_by_category, name='generals-by-category'),
    path('helper/<int:pk>/', helper_by_general, name='helper'),


    path('category/', category_list, name='category_list'),

    path('restfilter/', RestaurantFilter_list, name='restfilter_list'),
    path('parkfilter/', ParkFilter_list, name='parkfilter_list'),
    path('kalinkafilter/', category_list, name='kalinkafilter_list'),

    path('menu/<int:id>/', MenuCategoryListView.as_view(), name='menu-category-list'),
    path('namoz-vaqtlari/', NamozVaqtlariAPIView.as_view(), name='namoz-vaqtlari'),



]
