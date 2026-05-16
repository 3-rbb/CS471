from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('books/', include("apps.bookmodule.urls")), #include urls.py of bookmodule app
	path('users/', include("apps.usermodule.urls")), #include urls.py of usermodule app
	path('', RedirectView.as_view(url='/books/')),
]