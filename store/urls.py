from django.conf.urls import url
from django.urls import path, re_path
from store.views import *


urlpatterns = [
    path('', SnusListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('snus/create/', SnusCreateView.as_view(), name='snus_create'),
    path('snus/update/<int:pk>', UpdateSnusView.as_view(), name='update'),
    path('snus/purchase/<int:pk>', PurchaseSnusView.as_view(), name='purchase'),
    path('snus/purchase_list', PurchasesListView.as_view(), name='purchase_list'),
    path('snus/purchase_return/<int:pk>', ReturnSnusView.as_view(), name='return_snus'),
    path('snus/returns_list', ReturnsListView.as_view(), name='returns'),
    path('snus/delete_return/<int:pk>', DeclineReturnView.as_view(), name='decline_return'),
    path('snus/accept_return/<int:pk>', AcceptReturnView.as_view(), name='accept_return'),

]