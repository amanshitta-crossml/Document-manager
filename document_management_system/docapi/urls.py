from django.urls import path, include
from . import views
from .views import DocumentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'docs', DocumentViewSet, basename='doc-list')

urlpatterns = [
	path('', views.indexView, name='api-index'),
	path('',include(router.urls),name="docs"),
	# path('doc/', views.docList, name="doc-list"),	
	# path('doc/<int:pk>/', views.docDetail, name="doc-detail"),
	# path('doc-create/', views.docCreate, name="doc-create"),
	# path('doc/update/<int:pk>', views.docUpdate, name="doc-update"),
]
