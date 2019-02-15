from django.contrib import admin
from membership.models import Membership, UserMembership, Subcription
from django.conf import settings
# Register your models here.

admin.site.register(Membership)
admin.site.register(UserMembership)
admin.site.register(Subcription)

