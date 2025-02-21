from django.urls import path,include
from rest_framework_nested import routers
from . import  views



router = routers.DefaultRouter()

# router.register('clients' , views.ClientViewSet , basename='clients')
router.register("payments" , views.PaymentViewSet , basename="payments")
router.register('writers', views.WriterProfileViewSet, basename='writers')
router.register(r'reviews', views.ReviewViewSet, basename='reviews')
router.register(r"writers/applications", views.WriterApplicationViewSet, basename="writer-application")

# router.register(r'stk-push-callback', views.STKPushCallbackViewSet, basename='stk-push-callback')

# urlpatterns = router.urls + products_router.urls
urlpatterns = router.urls 
