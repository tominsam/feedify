from flickr.models import *

from django.contrib import admin


admin.site.register(RequestToken, 
    list_display = ("key", "created"),
    date_hierarchy = "created",
)

admin.site.register(AccessToken,
    list_display = ("key", "nsid", "username", "fullname", "created"),
    date_hierarchy = "created",
)
