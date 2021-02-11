from django.urls import path
from . import views

urlpatterns = [
    path('',views.bank, name='bank'), 
    path('create_user/',views.create_user, name='create_user'), 
    path('transaction/',views.transaction, name='transaction'), 
    path('transfer/<user_id>/',views.transfer, name='transfer'), 
    path('transaction_history/',views.transaction_history, name='transaction_history'), 
]

