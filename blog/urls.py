from django.urls import path
from .views import *
from .nomoz_vaqtlar import NamozVaqtlariAPIView

urlpatterns = [
    path('city/', city_list, name='city_list'),  # Shahar ro'yxati
    path('regions/<int:pk>/in_city/', RegionWithCitiesAPIView.as_view(), name='region_in_city'),
    path('general/', General_list, name='lgeneral_list'),
    path('generals/', GeneralListAPIView.as_view(), name='general_filter'),
    path('generals/<int:pk>/', generals_by_category, name='generals-by-category'),

    path('category/', category_list, name='category_list'),

    path('restfilter/', RestaurantFilter_list, name='restfilter_list'),
    path('parkfilter/', ParkFilter_list, name='parkfilter_list'),
    path('kalinkafilter/', category_list, name='kalinkafilter_list'),

    path('menu/<int:id>/', MenuCategoryListView.as_view(), name='menu-category-list'),
    path('namoz-vaqtlari/', NamozVaqtlariAPIView.as_view(), name='namoz-vaqtlari'),



]
