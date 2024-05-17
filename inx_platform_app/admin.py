from django.contrib import admin
from .models import *
# from .models import ColorGroup, Color, MadeIn, Division, MajorLabel
# from .models import InkTechnology, NSFDivision, MarketSegment, MaterialGroup, Industry
# from .models import Brand, Packaging, ProductStatus, Product, Customer, Ke30Line, UnitOfMeasure
# from .models import ExchangeRate, Scenario, CountryCode, BudForLine, BudForNote, BudForDetailLine
# from .models import CustomerType, Fbl5nArrImport, Fbl5nOpenImport, Ke30ImportLine, Ke24ImportLine
# from .models import Ke24Line, Order, CustomerNote, ProductLine, RateToLT, Fert
# from .models import ZAQCODMI9_line, ZAQCODMI9_import_line, UploadedFile, Price, User, Contact
# from .models import BudgetForecastDetail, BudgetForecastDetail_sales


class ColorGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id']


class MadeInAdmin(admin.ModelAdmin):
    list_display = ['id', 'plant_name', 'plant_number', 'sqlapp_id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id', 'name_short', 'color_weight', 'hex_value', 'color_number', 'color_group']


class ProductLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id']


class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class MajorLabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class InkTechnologyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name', 'ribbon_color', 'sap_id', 'sap_name', 'sqlapp_id']


class NSFDivisionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class MarketSegmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class PackagingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ProductStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id']


class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency']


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_sales', 'name', 'sqlapp_id']


class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'alpha_2', 'official_name_en']


class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'get_division_name', 'get_nsf_division_name']

    def get_division_name(self, obj):
        return obj.division.name

    def get_nsf_division_name(self, obj):
        return obj.nsf_division.name
    
    get_division_name.short_description = 'division_name'
    get_nsf_division_name.short_description = 'nsf_division'


class ProductAdmin(admin.ModelAdmin):
    # list_display = ['id', 'number', 'name', 'get_brand_name']
    list_display = ['id', 'number', 'name','get_color_name', 'get_colorgroup_name', 'get_brand_name']

    def get_brand_name(self, obj):
        if obj.brand:
            value = obj.brand.name
        else:
            value = ''
        return value
    
    def get_color_name(self, obj):
        if obj.color:
            value = obj.color.name
        else:
            value = ''
        return value
    
    def get_colorgroup_name(self, obj):
        if obj.color and obj.color.color_group:
            value = obj.color.color_group.name
        else:
            value =''
        return value
    
    get_brand_name.short_description = 'brand name'
    get_color_name.short_description = 'color name'
    get_colorgroup_name.short_description = 'color group'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'get_countrycode']
    search_fields = ['name']

    def get_countrycode(self, obj):
        if obj.country:
            value_to_return = obj.country.alpha_2
        else:
            value_to_return = 'N/A'
        return value_to_return
    
    get_countrycode.short_description = 'country'


class RateToLTAdmin(admin.ModelAdmin):
    list_display=['uom', 'rate_to_lt']


class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class PriceAdmin(admin.ModelAdmin):
    list_display=['id', 'customer_name', 'product_name', 'volume_from', 'volume_to', 'price', 'per', 'UoM', 'currency', 'valid_from', 'valid_to']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'first_name', 'last_name', 'job_position', 'email', 'mobile_number']


class FertAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']


class Ke30ImportLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'period_year', 'customer', 'customer_1', 'product', 'product_1', 'sales_qty_actual']


class Ke30LineAdmin(admin.ModelAdmin):
    list_display = ['id', 'year_month', 'customer_number', 'customer_name', 'product_number', 'product_name', 'currency', 'quantity', 'gross_sales']


class ZACODMI9_lineAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_date', 'sold_to', 'name', 'material', 'description', 'invoice_qty', 'unit_price', 'invoice_sales', 'curr', 'batch']


class BudForLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'get_brand_name', 'get_colorgroup_name']

    def get_customer_name(self, obj):
        return obj.customer.name
    
    def get_brand_name(self, obj):
        return obj.brand.name

    def get_colorgroup_name(self, obj):
        return obj.color_group.name
    
    get_customer_name.short_description = 'customer_name'
    get_brand_name.short_description = 'brand_name'
    get_colorgroup_name.short_description = 'color_group_name'


class BudForDetailLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_budforline_id', 'get_budforline_info', 'get_scenario_name', 'year', 'month', 'volume', 'price', 'value', 'get_value']
    search_fields = ['scenario__name', 'budforline__customer__name', 'budforline__brand__name', 'budforline__color_group__name', 'year', 'month']

    def get_budforline_id(self, obj):
        return obj.budforline.id
    
    def get_budforline_info(self, obj):
        the_related_budforline = obj.budforline
        return_value = f"{the_related_budforline.customer.name} - {the_related_budforline.brand.name} - {the_related_budforline.color_group.name}"
        return return_value
    
    def get_scenario_name(self, obj):
        return obj.scenario.name

    def get_value(self, obj):
        return_value = (obj.price or 0) * (obj.volume or 0)
        return return_value

    get_budforline_id.short_description = 'budforline_id'
    get_scenario_name.short_description = 'scenario'
    get_budforline_info.short_description = 'additional info'


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']
    search_fields = ['id', 'first_name', 'last_name', 'email']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','sales_order_number', 'customer_number', 'customer_name', 'country', 'product_number', 'product_name', 'qty_ordered', 'qty_ordered_unit']
    search_fields = ['customer_number', 'customer_name', 'product_number', 'product_name']


class BudgetForecastDetailAdmin_abs(admin.ModelAdmin):
    '''
    This is an abstract class that can be implemented as-is, the same by other models
    We adopt this strategy to avoid having Budget and Forecast together with Sales, at
    the same granulariity, in the same table. During normal operation, we must update
    Sales, every time we update zaq data. If Sales are together with Budget and Forecast,
    it is very hard and takes long time to remove Sales from a single table, causing delays.
    With 2 different tables (BudgetForecast and Sales), we can manage Sales in a better way
    '''
    list_display = ['id', 'get_budforline_id', 'get_budforline_info', 'get_scenario_name', 'year', 'month', 'volume', 'price', 'value', 'get_value']
    search_fields = ['scenario__name', 'budforline__customer__name', 'budforline__brand__name', 'budforline__color_group__name', 'year', 'month']

    class Meta:
        abstract = True

    def get_budforline_id(self, obj):
        return obj.budfoline.id

    def get_budforline_info(self, obj):
        the_related_budforline = obj.budforline
        return_value = f"{the_related_budforline.customer.name} - {the_related_budforline.brand.name} - {the_related_budforline.color_group.name}"
        return return_value

    def get_value(self, obj):
        return_value = obj.price or 0 * obj.volume or 0
        return return_value

    def get_scenario_name(self, obj):
        return obj.scenario.name
    
    get_budforline_id.short_description = 'budforline_id'
    get_scenario_name.short_description = 'scenario'
    get_budforline_info.short_description = 'additional info'


class BudgetForecastDetailAdmin(BudgetForecastDetailAdmin_abs):
    '''
    Contains only Budget and Forecast
    '''
    pass


class BudgetForecastDetail_salesAdmin(BudgetForecastDetailAdmin_abs):
    '''
    Contains only Sales
    '''
    pass


class UploadedFileAdmin(admin.ModelAdmin):
    list_display=['id', 'created_at', 'process_status', 'owner', 'file_type', 'file_name', 'file_color']


class UploadedFileLogAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ['-date']

    list_display = ['id', 'uploaded_file_id', 'get_user_email', 'date', 'file_path', 'file_name', 'log_text']
    
    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = 'User email'


admin.site.register(ColorGroup, ColorGroupAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(MadeIn, MadeInAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(MajorLabel, MajorLabelAdmin)
admin.site.register(InkTechnology, InkTechnologyAdmin)
admin.site.register(NSFDivision, NSFDivisionAdmin)
admin.site.register(MarketSegment, MarketSegmentAdmin)
admin.site.register(MaterialGroup, MaterialGroupAdmin)
admin.site.register(Packaging, PackagingAdmin)
admin.site.register(ProductStatus, ProductStatusAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(RateToLT, RateToLTAdmin)
admin.site.register(ExchangeRate, ExchangeRateAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(CountryCode, CountryCodeAdmin)
admin.site.register(CustomerType, CustomerTypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BudForLine, BudForLineAdmin)
admin.site.register(BudForNote)
admin.site.register(BudForDetailLine, BudForDetailLineAdmin)
admin.site.register(Fbl5nArrImport)
admin.site.register(Fbl5nOpenImport)
admin.site.register(Ke30ImportLine, Ke30ImportLineAdmin)
admin.site.register(Ke30Line, Ke30LineAdmin)
admin.site.register(Ke24ImportLine)
admin.site.register(Ke24Line)
admin.site.register(ZAQCODMI9_import_line)
admin.site.register(ZAQCODMI9_line, ZACODMI9_lineAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CustomerNote)
admin.site.register(UploadedFile, UploadedFileAdmin)
admin.site.register(UploadedFileLog, UploadedFileLogAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Fert, FertAdmin)
admin.site.register(BudgetForecastDetail, BudgetForecastDetailAdmin)
admin.site.register(BudgetForecastDetail_sales, BudgetForecastDetail_salesAdmin)

