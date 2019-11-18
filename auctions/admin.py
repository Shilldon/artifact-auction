from django.contrib import admin
from .models import Auction, Bid
from .forms import AuctionForm

class AuctionAdmin(admin.ModelAdmin):
    
    """ prevent admin from changing the artifact related to this auction"""    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('artifact',)
        return self.readonly_fields
    
    form = AuctionForm
    fields = ('artifact', 'start_date', 'end_date')
  
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)

