from django.urls import path
from . import views

app_name = 'homepage'  # Namespace for URL names
urlpatterns = [
    path('', views.home, name='home'),  # Homepage view
    path('about/', views.about, name='about'),  # About page view
    path('contact/', views.contact, name='contact'),  # Contact page view
    # path('ielts-tests/', views.ielts_tests, name='ielts_tests'),  # IELTS tests listing
    # path('ielts-tests/<int:test_id>/', views.ielts_test_detail, name='ielts_test_detail'),  # IELTS test detail
    # path('ielts-tests/<int:test_id>/take/', views.take_ielts_test, name='take_ielts_test'),  # Take IELTS test
    # path('ielts-tests/<int:test_id>/results/', views.ielts_test_results, name='ielts_test_results'),  # IELTS test results
]