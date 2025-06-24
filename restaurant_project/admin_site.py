from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

class RestaurantAdminSite(AdminSite):
    site_title = _('Restaurant Admin')

    site_header = _('Restaurant Administration')

    index_title = _('Site Administration')

    site_url = '/'
    
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_list = super().get_app_list(request)
        
        app_ordering = {
            'accounts': 1,
            'restaurant': 2,
            'menu': 3,
            'orders': 4,
            'reservations': 5,
            'auth': 6,
        }
        
        app_list.sort(key=lambda x: app_ordering.get(x['app_label'], 999))
        
        return app_list

admin_site = RestaurantAdminSite(name='admin') 