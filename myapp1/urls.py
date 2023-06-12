from . import views
from django.urls import path

app_name = 'myapp1'
urlpatterns = [
    path('', views.index1, name='index1'),
    path('Test', views.Test, name='Test'),
    path('bookingAdventure/', views.BookingAdventure, name='BookingAdventure'),
    path('updateBookingAdventure/<int:id>/', views.updateBookingAdventure, name='updateBookingAdventure'),
    path('deleteBookingAdventure/<int:id>/', views.deleteBookingAdventure, name='deleteBookingAdventure'),
    path('BookedRecords/', views.BookedRecords, name='BookedRecords'),
    path('get_capacity/', views.get_capacity, name='get_capacity'),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('packageAdventures/', views.PackageAdventures, name='PackageAdventures'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('forget_password/', views.ForgetPassword, name="forget_password"),
    path('change_password/<token>/', views.ChangePassword, name="change_password"),
    path('BookedPackageRecords/', views.BookedPackageRecords, name='BookedPackageRecords'),
    path('updatePacakageAdventure/<int:id>/', views.updatePacakageAdventure, name='updatePacakageAdventure'),
    path('deletePacakageAdventure/<int:id>/', views.deletePacakageAdventure, name='deletePacakageAdventure'),
    path('PacakageBookingAdventure/', views.PacakageBookingAdventure, name='PacakageBookingAdventure'),
    path('get_pacakagecapacity/', views.get_pacakagecapacity, name='get_pacakagecapacity'),
    path('updateUserPacakageAdventure/<int:id>/', views.updateUserPacakageAdventure,
         name='updateUserPacakageAdventure'),
    path('userpackages/', views.userpackages, name='userpackages'),
    path('deleteUserPacakageAdventure/<int:id>/', views.deleteUserPacakageAdventure,
         name='deleteUserPacakageAdventure'),
    path('save-data/', views.save_data, name='save_data'),
    path('ContactUSRecords/', views.ContactUSRecords, name='ContactUSRecords'),
    path('accounts/login/', views.NotAuthorized, name='NotAuthorized'),

]
