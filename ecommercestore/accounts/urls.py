from django.urls import path

from ecommercestore.accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileDetailsView, \
    ChangeUserPasswordView, ChangeProfileDetails

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register account'),
    path('login/', UserLoginView.as_view(redirect_authenticated_user=True), name='login account'),
    path('logout/', UserLogoutView.as_view(), name='logout account'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/<int:pk>/', ChangeProfileDetails.as_view(), name='profile edit'),
)
