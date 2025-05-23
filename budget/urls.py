from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FinancialStatementViews

router = DefaultRouter()
router.register(r'financial-statements', FinancialStatementViews)

urlpatterns = router.urls