from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import profile_view, RegisterView, display_products, AutocompleteProducts, seller_panel, add_to_favorites, \
    remove_from_favorites, favorites_view
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', profile_view, name='profile'),
    path('accounts/login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('products/', display_products, name='display_products'),
    path('search/', views.search_results, name='search_results'),
    path('autocomplete-products/', AutocompleteProducts.as_view(), name='autocomplete_products'),
    path('product/<str:brand>/<str:model>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category/', views.all_categories, name='all_categories'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:favorite_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('cart/', views.cart_view, name='cart'),
    path('seller/', seller_panel, name='seller_panel'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('category/<int:category_id>/<int:model_id>/', views.product_detail, name='product_detail'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('price-history-chart/', views.price_history_chart, name='price_history_chart'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
