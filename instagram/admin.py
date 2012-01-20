from instagram.models import *

from django.contrib import admin


admin.site.register(AccessToken,
    list_display = ("key", "userid", "username", "created", "fetched"),
    date_hierarchy = "created",
)
