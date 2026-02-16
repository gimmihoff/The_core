from django.urls import path
from .views.dashboard import dashboard
from .views.structures import structure_list
from .views.dscan import dscan_list

app_name = "aa_core_hub"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("structures/", structure_list, name="structures"),
    path("dscan/", dscan_list, name="dscan"),
]
