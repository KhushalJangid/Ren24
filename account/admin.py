from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.sessions.models import Session
from import_export.admin import ExportActionMixin,ExportActionModelAdmin,ImportExportMixin
from .models import *
from import_export import resources
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from import_export import fields

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email','password']
    
class AccountResource(resources.ModelResource):
    first_name = fields.Field(
        column_name='First Name',
        attribute='first_name',)
    last_name = fields.Field(
        column_name='Last Name',
        attribute='last_name',)
    email = fields.Field(
        column_name='Email',
        attribute='email',)
    rollno = fields.Field(
        column_name='Roll No',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'rollno'))
    phone = fields.Field(
        column_name='Phone No',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'phone'))
    dob = fields.Field(
        column_name='Date of Birth',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'dob'))
    address = fields.Field(
        column_name='Address',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'address'))
    published = fields.Field(
        column_name='Registered On',
        attribute='date_joined', 
        widget=DateTimeWidget(format='%d %b, %Y, %-I:%M %p'))   
    class Meta:
        model = User
        fields = ['first_name','last_name','email','rollno','phone','dob','address','published'] 

class AccountAdmin(ExportActionMixin,UserAdmin):
    # add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                  'email',
                  'password1',
                  'password2' 
                  ),
        }),
    )
    
    list_display=('id','first_name','last_name','email','last_login')
    search_fields = ["email","id","first_name"]
    readonly_fields = ['id',"date_joined","last_login"]
    autocomplete_fields = ["_pass"]
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering =()
    resource_class = AccountResource
    
class PassAdmin(ImportExportMixin,admin.ModelAdmin):
    empty_value_display = "Not selected"
    list_display=['psid','email','technical','splash']
    readonly_fields=['technical','splash']
    search_fields = ['email']


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    
class ProfileAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ['get_email','get_name','phone']
    search_fields = ['user__email','user__first_name']
    autocomplete_fields = ["user"]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('user')
    
    def get_email(self,obj):
        return obj.user.email 
    
    def get_name(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"
    get_name.short_description = "Name"
    # get_name.admin_order_field = "user__first_name"

admin.site.register(Session, SessionAdmin)
admin.site.register(User,AccountAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Passes,PassAdmin)
admin.site.register(OTP)
# admin.site.register(Wallet,WalletAdmin)
