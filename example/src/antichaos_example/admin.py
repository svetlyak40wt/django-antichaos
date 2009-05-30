from django.contrib import admin
from models import *

_display_fields = ('id', 'url', 'tags')
admin.site.register(Link,
    list_display = _display_fields,
    list_display_links = _display_fields,
)
