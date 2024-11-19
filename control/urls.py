from django.urls import path

from control.views import login_view, logout_view, redirect_view, test_session

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('redirect/', redirect_view),
    path('test/', test_session)
]