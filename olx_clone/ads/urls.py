from django.urls import path
from . import views

urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('post/', views.post_ad, name='post_ad'),
    path('run-script/', views.run_script_view, name='run_script_view'),
    path('car-data/', views.car_data_view, name='car_data'),
        path('feedback/submit/', views.submit_feedback_view, name='submit_feedback'),
    path('feedback/admin/', views.admin_feedback_view, name='admin_feedback'),

]
