from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.Viewsets_guest)
router.register('', views.Viewsets_movies)
router.register('', views.Viewsets_reservations)


urlpatterns = [
    path("admin/", admin.site.urls),
    # 1 GET ONLY without using any framework or model by passing a json data to client
    path('django/json_response_no_model/', views.no_rest_no_model),
    # 2 GET ONLY without using any framework but get data from model and pass it to client as a json format
    path('django/json_response_with_model/', views.no_rest_from_model),
    # 3.1 GET POST from rest framework function based view
    path('rest/fbv/', views.FBV_List),
    # 3.2 GET PUT DELETE from rest framework function based view
    path('rest/fbv_item/<int:pk>', views.FBV_pk),
    # 4.1 GET POST from rest framework class based view
    path('rest/cbv/', views.CBV_List.as_view()),
    # 4.2 GET PUT DELETE from rest framework class based view
    path("rest/CBV_pk/<int:pk>", views.CBV_pk.as_view()),
    # 5.1 GET POST from rest framework class based view using mixins
    path('rest/mixins_list/', views.mixins_list.as_view()),
    # 5.2 GET PUT DELETE from rest framework class based view using mixins
    path('rest/mixins_pk/<int:pk>', views.mixins_pk.as_view()),
    # 6.1 GET POST from rest framework calss based view using generics
    path("rest/Generics_list", views.Generics_list.as_view()),
    # 6.2 GET PUT DELETE from rest framework class based view using generics
    path("rest/Generics_pk/<int:pk>", views.Generics_pk.as_view()),
    # 7 GET, POST, PUT ,DELETE, GET_WITH_PK all in one using router.register from rest framework and using viewsets.ModelViewSet from rest framework << the easiest way >>
    path("rest/Viewsets_guest/", include(router.urls)),
    path("rest/viewsets_movies/", include(router.urls)),
    path('rest/viewsets_reservations/', include(router.urls)),
    # 8 Find movie
    path("rest/find_movie/", views.find_movie),
    # 9 Create a reservation using post method only
    path('rest/create_reservation/', views.create_reservation),
]
