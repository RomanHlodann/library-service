from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingListRetrieveViewSet


router = routers.DefaultRouter()
router.register("", BorrowingListRetrieveViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "borrowings"
