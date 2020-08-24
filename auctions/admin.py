from django.contrib import admin
from .models import User, Listing, Bids, Comments
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Listing, UserAdmin)
admin.site.register(models.Bids, UserAdmin)
admin.site.register(models.Comments UserAdmin)
# Register your models here.
