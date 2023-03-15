from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
path('api_schema/', get_schema_view(
        title='API Schema',
        description='Guide for the REST API'
    ), name='api_schema'),

    path("upload/small/", views.UploadSmallImage.as_view(),name='small_upload'),
    path("upload/medium/", views.UploadMediumImage.as_view(),name='medium_upload'),
    path("upload/orginal/", views.UploadOriginalImage.as_view(),name='original_upload'),
    path("upload/custom/",views.UploadCustomImage.as_view(),name='custom_upload'),
    path("login/", obtain_auth_token,name='obtain-token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("list/",views.ListImage.as_view(),name='img_listview'),
    path("view/<str:id>/", views.ImageView.as_view(),name='img_view'),

]