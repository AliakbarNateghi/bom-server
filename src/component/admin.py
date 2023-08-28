from django.apps import apps
from django.contrib import admin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
    

from ..log.Tracker import TrackerAdmin
from .models import (
    BomComponent,
    BomFieldPermission,
    ProvideComponent,
    ProvideFieldPermission
)

# class MyInlines1(TabularInlineJalaliMixin, admin.TabularInline):
# 	model = SecendModel

# class MyInlines2(StackedInlineJalaliMixin, admin.StackedInline):
# 	model = ThirdModel
	
# @admin.register(FirstModel)
# class FirstModelAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
# 	# show jalali date in list display 
# 	list_display = ['some_fields', 'get_created_jalali']
	
# 	inlines = (MyInlines1, MyInlines2, )
# 	raw_id_fields = ('some_fields', )
# 	readonly_fields = ('some_fields', 'date_field',)
# 	# you can override formfield, for example:
# 	formfield_overrides = {
# 	    JSONField: {'widget': JSONEditor},
# 	}
	
# 	@admin.display(description='تاریخ ایجاد', ordering='created')
# 	def get_created_jalali(self, obj):
# 		return datetime2jalali(obj.created).strftime('%a, %d %b %Y %H:%M:%S')


admin.site.register(BomComponent, TrackerAdmin)
admin.site.register(BomFieldPermission)
admin.site.register(ProvideComponent, TrackerAdmin)
admin.site.register(ProvideFieldPermission)
