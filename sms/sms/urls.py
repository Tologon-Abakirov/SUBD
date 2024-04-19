
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),
    path('product_sale/', include('product_sale.urls')),
    path('positions/',include('positions.urls')),
    path('rawmaterials/',include('Rawmaterials.urls')),
    path('unit/',include('unitofmaesurement.urls')),
    path('ingredients/',include('Ingredients.urls')),
    path('finish/',include('finishedproduct.urls')),
    path('raw_sale/',include('raw_sale.urls')),
    path('production/',include('production.urls')),
    path('salaryes/',include('salaryes.urls')),
    path('budget/',include('budget.urls')),
    path('credit/',include('credit.urls')),
    path('creditpayment/',include('creditpayment.urls')),


]
