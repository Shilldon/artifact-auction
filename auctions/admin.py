from django.contrib import admin
from .forms import AuctionAdminForm, UserModelChoiceField
from .models import Auction
from artifacts.models import Artifact

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['artifact'].queryset = Artifact.objects.filter(sold=False, in_auction=False)
        return super(AuctionAdmin, self).render_change_form(request, context, *args, **kwargs)
        
admin.site.register(Auction, AuctionAdmin)