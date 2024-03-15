from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from config.settings import BASE_URL
from django.contrib.admin.filters import AllValuesFieldListFilter
from import_export import resources
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from import_export import fields
# Register your models here.

class EventAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=('name','type','amount','date','time')
    list_filter = [('type', AllValuesFieldListFilter)]
    search_fields = ['name','venue']
    
class TicketResource(resources.ModelResource):
    email = fields.Field(
        column_name='Email',
        attribute='user',
        widget=ForeignKeyWidget(User, 'email'))
    rollno = fields.Field(
        column_name='Roll No',
        attribute='user',
        widget=ForeignKeyWidget(User, 'profile__rollno'))
    phone = fields.Field(
        column_name='Phone No',
        attribute='user',
        widget=ForeignKeyWidget(User, 'profile__phone'))
    first_name = fields.Field(
        column_name='First Name',
        attribute='user',
        widget=ForeignKeyWidget(User, 'first_name'))
    last_name = fields.Field(
        column_name='Last Name',
        attribute='user',
        widget=ForeignKeyWidget(User, 'last_name'))
    published = fields.Field(
        column_name='Registered On',
        attribute='created', 
        widget=DateTimeWidget(format='%d %b, %Y, %-I:%M %p'))

    class Meta:
        model = Ticket
        fields = ['first_name','last_name','email','rollno','phone','published']
        
class CustomTicketResource(resources.ModelResource):
    email = fields.Field(
        column_name='Email',
        attribute='email',)
    phone = fields.Field(
        column_name='Phone No',
        attribute='phone_no',)
    name = fields.Field(
        column_name='Name',
        attribute='name',)
    published = fields.Field(
        column_name='Registered On',
        attribute='created', 
        widget=DateTimeWidget(format='%d %b, %Y, %-I:%M %p'))

    class Meta:
        model = CustomTicket
        fields = ['name','email','phone','published']
    
class TicketAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display=('get_username','get_event','get_email','get_price','created')
    readonly_fields = ['created']
    search_fields = ['user__email','event__name','event__type']
    list_filter = [('event__type', AllValuesFieldListFilter)]
    autocomplete_fields = ['user',"event"]
    resource_class = TicketResource
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset =  queryset.prefetch_related('user')
        return queryset.prefetch_related('event')
    
    def get_date(self,obj):
        return f"{obj.event.date} {obj.event.time}" 
    
    def get_price(self,obj):
        return obj.event.amount 
    def get_event(self,obj):
        return obj.event.name
    
    def get_email(self,obj):
        return obj.user.email 
    
    def get_username(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    
    get_date.short_description = "Date & Time"
    get_date.admin_order_field = "event__date"
    get_event.short_description = "Event"
    get_event.admin_order_field = "event__name"
    get_price.short_description = "Price"
    get_price.admin_order_field = "event__amount"
    get_email.short_description = "Email"
    # get_email.admin_order_field = "user__email"
    get_username.short_description = "Name"
    get_username.admin_order_field = "user__first_name"
    
    
class CustomTicketAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ['id','get_link','email','event','note']
    readonly_fields = ['id','created']
    search_fields = ['name','phone_no','email','event__name']
    autocomplete_fields = ["event"]
    resource_class = CustomTicketResource
    
    def get_link(self,obj):
        return f"{BASE_URL}/custom/{obj.id}" 
    get_link.short_description = "View Link"
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(CustomTicketAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['event'].queryset = Events.objects.filter(name__iexact='company')
    #     return form
    
    # fieldsets = (
    #     (None, {
    #         'fields': ['event','amount'],
    #         'description': f"This will generate a custom ticket for the selected event & amount, The form can be accessed from the link on display"
    #     }),
    #     (None, {
    #         'fields': ['user','date','is_paid'],
    #         }),
    # )
    # def get_link(self,obj):
    #     return f"{BASE_URL}/custom/{obj.id}" 
    # get_link.short_description = "Link"


admin.site.register(Events,EventAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(CustomTicket,CustomTicketAdmin)