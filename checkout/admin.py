from django.contrib import admin
from .models import Order, PurchasedArtifact

class PurchasedArtifactAdminInLine(admin.TabularInline):
    model = PurchasedArtifact
    
class OrderAdmin(admin.ModelAdmin):
    inlines = (PurchasedArtifactAdminInLine, )
    
admin.site.register(Order, OrderAdmin)