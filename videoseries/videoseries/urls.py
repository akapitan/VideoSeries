''' Hello '''
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import home
from blog.views import blog_list, blog_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include("courses.urls", namespace='courses')),
    path('memberships/', include("membership.urls", namespace='memberships')),
    path('', home),
    path('accounts/', include("accounts.urls", namespace='accounts')),
    path('blog/', blog_list),
    path('blog/index/', blog_index),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
 