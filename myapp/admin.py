from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters, register
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Customer, Order, OrderItem, Product
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.contrib import messages

admin.autodiscover()


# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PriceFilter(SimpleListFilter):
    title = 'order price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('<1000', _('less than 1k')),
            ('1000-2000', _('from 1k to 2k')),
            ('>2000', _('more than 2k')),
        )

    def queryset(self, request, queryset):
        qs = [(obj.id, obj.order_price()) for obj in queryset.all()]
        ids = [obj.id for obj in queryset.all()]
        if self.value() == '<1000':
            ids = [objId for objId, price in qs if price < 1000]
        elif self.value() == '1000-2000':
            ids = [objId for objId, price in qs if 1000 <= price <= 2000]
        elif self.value() == '>2000':
            ids = [objId for objId, price in qs if price > 2000]

        return queryset.filter(id__in=ids)


class OrderItemInline(admin.TabularInline):
    model = OrderItem

    def get_extra(self, request, obj=None, **kwargs):
        return 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_price')
    list_filter = ['status', 'customer__phone_number', PriceFilter, 'created_date']

    inlines = [OrderItemInline]
    readonly_fields = ['status']

    actions = ['cancel_order']

    @admin.action(description='Cancel selected orders')
    def cancel_order(self, request, queryset):
        updated = queryset.update(status='CA')
        self.message_user(request, ngettext(
            '%d order was successfully cancelled.',
            '%d orders were successfully cancelled.',
            updated,
        ) % updated, messages.SUCCESS)

    # ref: https://stackoverflow.com/questions/34897388/django-how-to-add-a-custom-button-to-admin-change-form-page-that-executes-an-ad
    change_form_template = '../templates/custom_change_form.html'

    def response_change(self, request, obj):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "_customaction" in request.POST:
            # handle the action on your obj
            self.cancel_order(request, Order.objects.filter(pk=pk_value))
            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts},
                                                 redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            return super(OrderAdmin, self).response_change(request, obj)


admin.site.register(Product)
