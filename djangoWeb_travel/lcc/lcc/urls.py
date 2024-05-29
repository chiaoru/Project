"""
URL configuration for lcc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news.views import news
from tour.views import tours

from django.conf import settings
from django.conf.urls.static import static
from gallery.views import uploadFile
from contact.views import contact,about
from member.views import register, login, logout, ChangePassword
from cart.views import cart, addtocart, cartorder, cartok, cartordercheck, myorder, reportBank, ECPayCredit, bankfive

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', news),
    path('tours/', tours),
    path('gallery/', uploadFile),
    path('contact/', contact),
    path('about/', about),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('', uploadFile),
    path('addtocart/<str:ctype>/<int:toursid>/', addtocart),
    path('addtocart/<str:ctype>/', addtocart),
    path('cart/', cart),
    path('cartorder/', cartorder),
    path('cartok/', cartok),
    path('cartordercheck/', cartordercheck),
    path('myorder/', myorder),
    path('reportBank/', reportBank),
    path('creditcard/', ECPayCredit),
    path('bankfive/', bankfive),
    path('membercenter/', ChangePassword),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    

