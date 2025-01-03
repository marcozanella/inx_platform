from django import forms
from django.db.models import ForeignKey
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.utils.translation import gettext_lazy as _
from .models import Language

from .models import (
    ProductStatus,
    Scenario,
    User,
    Bom,
    BomHeader,
    BomComponent,
    Color,
    ColorGroup,
    MadeIn,
    ProductLine,
    Division,
    Brand,
    MajorLabel,
    InkTechnology,
    NSFDivision,
    MarketSegment,
    MaterialGroup,
    Packaging,
    UnitOfMeasure,
    Industry,
    Customer,
    CountryCode,
    RateToLT,
    Currency,
    CurrencyRate,
    Contact,
    ExchangeRate,
    EuroExchangeRate,
    CustomerType,
    CustomerNote,
    Product,
    BudForDetailLine,
    BudForNote,
    BudForLine,
    Ke24ImportLine,
    Ke24Line,
    Ke30ImportLine,
    Ke30Line,
    ZAQCODMI9_import_line,
    ZAQCODMI9_line,
    Fbl5nArrImport,
    Fbl5nOpenImport,
    Order,
    UploadedFile,
    UploadedFileLog,
    Price,
    Fert,
    BudgetForecastDetail,
    BudgetForecastDetail_sales,
    ContactType,
    PackagingRateToLiter,
    UnitOfMeasureConversionFactor,
    ManualCost,
    Rebate,
    SDSReplacement,
    SDSRTFFile
    )

admin.site.site_header = "INX Platform Administration"
admin.site.site_title = "INX Platform Admin"
admin.site.index_title = "Welcome to INX Platform Admin Panel"

class ColorGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id']


class MadeInAdmin(admin.ModelAdmin):
    list_display = ['id', 'plant_name', 'plant_number', 'sqlapp_id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id', 'name_short', 'color_weight', 'hex_value', 'color_number', 'color_group']
    list_filter = ['color_group']


class ProductLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id']
    search_fields = ['name']


class DivisionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name']


class MajorLabelAdmin(admin.ModelAdmin):
    list_display = ['id', 'oem', 'name', 'sap_id', 'sap_name']


class InkTechnologyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'short_name', 'ribbon_color', 'sap_id', 'sap_name', 'sqlapp_id']


class NSFDivisionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class MarketSegmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'sqlapp_id']


class PackagingAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'base_unit_of_measure']


class ProductStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sqlapp_id', 'marked_for_deletion']

    def save_model(self, request, obj, form, change):
        if obj.marked_for_deletion:
            ProductStatus.objects.exclude(pk=obj.pk).update(marked_for_deletion=False)
        super().save_model(request, obj, form, change)


class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'year', 'rate']


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_sales', 'is_forecast', 'is_budget', 'name', 'sqlapp_id']

    def save_model(self, request, obj, form, change):
        if obj.is_sales:
            Scenario.objects.exclude(pk=obj.id).update(is_sales=False)
        if obj.is_forecast:
            Scenario.objects.exclude(pk=obj.id).update(is_forecast=False)
        if obj.is_budget:
            Scenario.objects.exclude(pk=obj.id).update(is_budget=False)
        super().save_model(request, obj, form, change)


class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'alpha_2', 'official_name_en']


class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sap_id', 'sap_name', 'get_division_name', 'get_nsf_division_name']
    search_fields = ['name']

    def get_division_name(self, obj):
        return obj.division.name

    def get_nsf_division_name(self, obj):
        return obj.nsf_division.name
    
    get_division_name.short_description = 'division_name'
    get_nsf_division_name.short_description = 'nsf_division'


class ProductAdmin(admin.ModelAdmin):

    list_display = ['id', 'number', 'name','get_color_name', 'get_colorgroup_name', 'get_brand_name', 'is_fert', 'is_ink', 'is_new',  'approved_on']
    list_filter = ['is_new', 'is_ink', 'is_fert', 'color__name']
    search_fields = ['number', 'name']
    autocomplete_fields = ['brand', 'customer']
    
    # Override changelist_view to show selected filters
    def changelist_view(self, request, extra_context=None):
        # Get current filter selections from the request GET parameters
        selected_filters = request.GET.dict()
        
        # Initialize a dictionary to hold human-readable filter values
        readable_filters = {}
        
        # Loop through the selected filters
        for filter_key, filter_value in selected_filters.items():
            # Check if the filter is for a foreign key field (e.g., 'currency__id__exact')
            if '__id__exact' in filter_key:
                # Extract the model field name (e.g., 'currency')
                field_name = filter_key.split('__id__exact')[0]
                
                # Check if the field is a ForeignKey field in the model
                if field_name in [f.name for f in self.model._meta.fields if isinstance(f, ForeignKey)]:
                    related_model = self.model._meta.get_field(field_name).related_model
                    
                    # Get the related object using the ID in the filter value
                    try:
                        related_obj = related_model.objects.get(pk=filter_value)
                        readable_filters[field_name] = f"{field_name}: {related_obj}"
                    except related_model.DoesNotExist:
                        readable_filters[field_name] = f"{field_name}: Unknown"
                else:
                    # If it's not a foreign key, just add the filter as is
                    readable_filters[filter_key] = f"{filter_key}: {filter_value}"
            else:
                # For non-ForeignKey filters, add them as is
                readable_filters[filter_key] = f"{filter_key}: {filter_value}"
        
        # Add the selected filters to the extra context so that they can be used in the template
        extra_context = extra_context or {}
        extra_context['selected_filters'] = readable_filters
        print(readable_filters)
        
        # Call the original changelist_view method
        return super().changelist_view(request, extra_context=extra_context)

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
    get_color_name.admin_order_field = 'color__name'
    get_colorgroup_name.admin_order_field = 'color_group__name'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'get_countrycode', 'get_currency_alpha_3']
    list_filter = ['active', 'customer_type', 'currency', 'is_new']
    search_fields = ['name', 'currency_text']

    # Override changelist_view to show selected filters
    def changelist_view(self, request, extra_context=None):
        # Get current filter selections from the request GET parameters
        selected_filters = request.GET.dict()
        
                # Initialize a dictionary to hold human-readable filter values
        readable_filters = {}
        
        # Loop through the selected filters
        for filter_key, filter_value in selected_filters.items():
            # Check if the filter is for a foreign key field (e.g., 'currency__id__exact')
            if '__id__exact' in filter_key:
                # Extract the model field name (e.g., 'currency')
                field_name = filter_key.split('__id__exact')[0]
                
                # Check if the field is a ForeignKey field in the model
                if field_name in [f.name for f in self.model._meta.fields if isinstance(f, ForeignKey)]:
                    related_model = self.model._meta.get_field(field_name).related_model
                    
                    # Get the related object using the ID in the filter value
                    try:
                        related_obj = related_model.objects.get(pk=filter_value)
                        readable_filters[field_name] = f"{field_name}: {related_obj}"
                    except related_model.DoesNotExist:
                        readable_filters[field_name] = f"{field_name}: Unknown"
                else:
                    # If it's not a foreign key, just add the filter as is
                    readable_filters[filter_key] = f"{filter_key}: {filter_value}"
            else:
                # For non-ForeignKey filters, add them as is
                readable_filters[filter_key] = f"{filter_key}: {filter_value}"
        
        # Add the selected filters to the extra context so that they can be used in the template
        extra_context = extra_context or {}
        extra_context['selected_filters'] = readable_filters
        
        # Call the original changelist_view method
        return super().changelist_view(request, extra_context=extra_context)

    def get_countrycode(self, obj):
        if obj.country:
            value_to_return = obj.country.alpha_2
        else:
            value_to_return = 'N/A'
        return value_to_return
    
    def get_currency_alpha_3(self, obj):
        if obj.currency:
            return_value = obj.currency.alpha_3
        else:
            return_value = "N/A"
        return return_value
    
    get_countrycode.short_description = 'country'
    get_currency_alpha_3.short_description = "currency"


class RateToLTAdmin(admin.ModelAdmin):
    list_display=['uom', 'rate_to_lt']


class IndustryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class PriceAdmin(admin.ModelAdmin):
    list_display=['id', 'customer_name', 'product_name', 'volume_from', 'volume_to', 'price', 'per', 'UoM', 'currency', 'valid_from', 'valid_to']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_contact_type_name', 'title', 'first_name', 'last_name', 'job_position', 'email', 'mobile_number']
    search_fields = ['last_name', 'first_name']

    def get_contact_type_name(self, obj):
        if obj.contact_type:
            return_value = obj.contact_type.name
        else:
            return_value = ''
        return return_value

    get_contact_type_name.short_description = 'type'


class FertAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']


class Ke30ImportLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'period_year', 'customer', 'customer_1', 'product', 'product_1', 'sales_qty_actual']


class Ke30LineAdmin(admin.ModelAdmin):
    list_display = ['id', 'year_month', 'customer_number', 'customer_name', 'product_number', 'product_name', 'currency', 'quantity', 'gross_sales']
    search_fields = ['year_month', 'customer_name', 'customer_number', 'product_name', 'product_number']


class ZACODMI9_lineAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_date', 'sold_to', 'name', 'material', 'description', 'invoice_qty', 'unit_price', 'invoice_sales', 'curr', 'batch']


class BudForLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer_name', 'get_brand_name', 'get_colorgroup_name']
    # list_display = ['id', 'customer__name']
    ordering = ['id', 'customer__name', 'brand__name', 'color_group__name']
    search_fields = ['customer__name']

    def get_customer_name(self, obj):
        return obj.customer.name
    
    def get_brand_name(self, obj):
        return obj.brand.name

    def get_colorgroup_name(self, obj):
        return obj.color_group.name
    
    get_customer_name.short_description = 'customer name'
    get_customer_name.admin_order_field = 'customer__name'
    get_brand_name.short_description = 'brand name'
    get_brand_name.admin_order_field = 'brand__name'
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


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','sales_order_number', 'customer_number', 'customer_name', 'country', 'product_number', 'product_name', 'qty_ordered', 'qty_ordered_unit']
    search_fields = ['customer_number', 'customer_name', 'product_number', 'product_name']


class BudgetForecastDetailAdmin_abs(admin.ModelAdmin):
    '''
    This is an abstract class that can be implemented as-is, the same by other models
    We adopt this strategy to avoid having Budget and Forecast together with Sales, at
    the same granulariity, in the same table. During normal operation, we must update
    Sales every time we update zaq data. If Sales are together with Budget and Forecast,
    it is very hard and takes long time to remove Sales from a single table, causing delays.
    With 2 different tables (BudgetForecast and Sales), we can manage Sales in a better way
    '''
    list_display = ['id', 'get_budforline_id', 'get_budforline_info', 'get_scenario_name', 'year', 'month', 'volume', 'price', 'value', 'get_value']
    list_filter = ['scenario__name', 'year']
    search_fields = ['id', 'budforline__id', 'scenario__name', 'budforline__customer__name', 'budforline__brand__name', 'budforline__color_group__name', 'year', 'month']
    ordering = ['id', 'budforline__id', 'scenario__name']

    # Override changelist_view to show selected filters
    def changelist_view(self, request, extra_context=None):
        # Get current filter selections from the request GET parameters
        selected_filters = request.GET.dict()
        
        # Add the selected filters to the extra context so that they can be used in the template
        extra_context = extra_context or {}
        extra_context['selected_filters'] = selected_filters
        
        # Call the original changelist_view method
        return super().changelist_view(request, extra_context=extra_context)
    
    class Meta:
        abstract = True

    def get_budforline_id(self, obj):
        return obj.budforline.id

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
    get_budforline_id.admin_order_field = 'budforline__id'
    get_scenario_name.short_description = 'scenario'
    get_scenario_name.admin_order_field = 'scenario__name'
    get_budforline_info.short_description = 'Customer - Brand - ColorGroup'


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
    list_display=['id', 'created_at', 'is_processed', 'process_status', 'owner', 'file_type', 'file_name', 'file_color']


class UploadedFileLogAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ['-date']

    list_display = ['id', 'uploaded_file_id', 'get_user_email', 'date', 'file_path', 'file_name', 'log_text']
    readonly_fields = ("user_id", "user", "uploaded_file", "file_path", "file_name", "celery_task_id", )

    
    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = 'User email'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'alpha_3', 'symbol']
    ordering = ['name']


class UserAdmin(BaseUserAdmin):
    # Forms to add and edit Users

    model = User
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'mobile_number', 'photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'budget_open', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    readonly_fields = ('date_joined',)
    search_fields = ('id', 'first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups',)


class ContactTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'year', 'rate']
    list_filter = ['currency']
    ordering = ['currency', 'year']


class PackagingRateToLiterAdmin(admin.ModelAdmin):
    list_display=['id', 'packaging', 'unit_of_measure', 'rate_to_liter']


class BomHeaderWidget(ForeignKeyRawIdWidget):
    def label_for_value(self, value):
        try:
            obj = self.rel.model.objects.get(pk=value)
            return f"{obj.product.name} ({obj.alt_bom})"
        except (self.rel.model.DoesNotExist, ValueError):
            return super().label_for_value(value)


class BomForm(forms.ModelForm):
    class Meta:
        model = Bom
        fields = '__all__'
        widgets = {
            'bom_header': BomHeaderWidget(Bom._meta.get_field('bom_header').remote_field, admin.site),
        }


class BomHeaderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_product_number', 'get_product_name', 'alt_bom', 'header_base_quantity', 'header_base_quantity_uom']
    search_fields = ['product__name', 'product__number']

    def get_product_number(self, obj):
        return f"({obj.product.id}) {obj.product.number}"
    get_product_number.admin_order_field = 'product__number'
    get_product_number.short_description = 'Product Number'

    def get_product_name(self, obj):
        return f"{obj.product.name}"
    get_product_name.admin_order_field = 'product__name'
    get_product_name.short_description = 'Product Name'


class BomComponentAdmin(admin.ModelAdmin):
    list_display = ['id', 'component_material', 'component_material_description', 'component_base_uom', 'is_fert']
    list_filter = ['is_fert']
    search_fields = ['id', 'component_material', 'component_material_description']


class BomAdmin(admin.ModelAdmin):
    form = BomForm
    list_display = ['id', 'bom_header_id', 'get_product_name', 'get_alt_bom', 'item_number', 'get_component_material_description', 'component_quantity', 'component_uom_in_bom', 'component_base_uom', 'price_unit', 'standard_price_per_unit_CZK', 'standard_price_per_unit_EUR', 'weighed_price_per_kg_ea_EUR']
    search_fields = ['bom_header__id', 'bom_header__product__name', 'bom_header__alt_bom']
    ordering = ['bom_header__id']

    def get_product_name(self, obj):
        return obj.bom_header.product.name
    get_product_name.admin_order_field = 'bom_header__product__name'
    get_product_name.short_description = 'Product Name'

    def get_alt_bom(self, obj):
        return obj.bom_header.alt_bom
    get_alt_bom.admin_order_field = 'bom_header__alt_bom'
    get_alt_bom.short_description = 'Alt BOM'
    
    def get_component_material_description(self, obj):
        return f"id{obj.bom_component.id} ({obj.bom_component.component_material}) {obj.bom_component.component_material_description}"
    get_component_material_description.short_description = 'Component'


class UnitOfMeasureConversionFactorAdmin(admin.ModelAdmin):
    list_display = ['uom_from', 'uom_to', 'factor']
    
    
class ManualCostAdmin(admin.ModelAdmin):
    list_display = ['nsf_division', 'scenario', 'year', 'rmc_perc', 'conv_perc'] 
    list_filter = ['scenario', 'nsf_division']
    
    # Override changelist_view to show selected filters
    def changelist_view(self, request, extra_context=None):
        # Get current filter selections from the request GET parameters
        selected_filters = request.GET.dict()
        
        # Initialize a dictionary to hold human-readable filter values
        readable_filters = {}
        
        # Loop through the selected filters
        for filter_key, filter_value in selected_filters.items():
            # Check if the filter is for a foreign key field (e.g., 'currency__id__exact')
            if '__id__exact' in filter_key:
                # Extract the model field name (e.g., 'currency')
                field_name = filter_key.split('__id__exact')[0]
                
                # Check if the field is a ForeignKey field in the model
                if field_name in [f.name for f in self.model._meta.fields if isinstance(f, ForeignKey)]:
                    related_model = self.model._meta.get_field(field_name).related_model
                    
                    # Get the related object using the ID in the filter value
                    try:
                        related_obj = related_model.objects.get(pk=filter_value)
                        readable_filters[field_name] = f"{field_name}: {related_obj}"
                    except related_model.DoesNotExist:
                        readable_filters[field_name] = f"{field_name}: Unknown"
                else:
                    # If it's not a foreign key, just add the filter as is
                    readable_filters[filter_key] = f"{filter_key}: {filter_value}"
            else:
                # For non-ForeignKey filters, add them as is
                readable_filters[filter_key] = f"{filter_key}: {filter_value}"
        
        # Add the selected filters to the extra context so that they can be used in the template
        extra_context = extra_context or {}
        extra_context['selected_filters'] = readable_filters
        print(readable_filters)
        
        # Call the original changelist_view method
        return super().changelist_view(request, extra_context=extra_context)


class EuroExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['id', 'currency', 'year', 'month', 'rate']
    search_fields = ['currency__alpha_3']
    list_filter = ['currency__alpha_3', 'year']
    
    # Override changelist_view to show selected filters
    def changelist_view(self, request, extra_context=None):
        # Get current filter selections from the request GET parameters
        selected_filters = request.GET.dict()
        
        # Initialize a dictionary to hold human-readable filter values
        readable_filters = {}
        
        # Loop through the selected filters
        for filter_key, filter_value in selected_filters.items():
            # Check if the filter is for a foreign key field (e.g., 'currency__id__exact')
            if '__id__exact' in filter_key:
                # Extract the model field name (e.g., 'currency')
                field_name = filter_key.split('__id__exact')[0]
                
                # Check if the field is a ForeignKey field in the model
                if field_name in [f.name for f in self.model._meta.fields if isinstance(f, ForeignKey)]:
                    related_model = self.model._meta.get_field(field_name).related_model
                    
                    # Get the related object using the ID in the filter value
                    try:
                        related_obj = related_model.objects.get(pk=filter_value)
                        readable_filters[field_name] = f"{field_name}: {related_obj}"
                    except related_model.DoesNotExist:
                        readable_filters[field_name] = f"{field_name}: Unknown"
                else:
                    # If it's not a foreign key, just add the filter as is
                    readable_filters[filter_key] = f"{filter_key}: {filter_value}"
            else:
                # For non-ForeignKey filters, add them as is
                readable_filters[filter_key] = f"{filter_key}: {filter_value}"
        
        # Add the selected filters to the extra context so that they can be used in the template
        extra_context = extra_context or {}
        extra_context['selected_filters'] = readable_filters
        print(readable_filters)
        
        # Call the original changelist_view method
        return super().changelist_view(request, extra_context=extra_context)


class RebateAdmin(admin.ModelAdmin):
    list_display=['id', 'get_customer_name', 'get_brand_name', 'get_scenario_name', 'year', 'rebate', 'is_active']
    
    def get_customer_name(self, obj):
        return obj.customer.name
    get_customer_name.admin_order_field = 'customer__name'
    get_customer_name.short_description = 'Customer'
    
    def get_brand_name(self, obj):
        return obj.brand.name
    get_brand_name.admin_order_field = 'brand__name'
    get_brand_name.short_description = 'Brand'

    def get_scenario_name(self, obj):
        return obj.scenario.name
    get_scenario_name.admin_order_field = 'scenario__name'
    get_scenario_name.short_description = 'Scenario'


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'iso_639_1', 'iso_639_2', 'family', 'name', 'native_name', 'wiki_url']
    search_fields = ['iso_639_1', 'iso_639_2', 'family', 'name', 'native_name', 'wiki_url']
    ordering = ['iso_639_1']


class ProductLanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'language', 'name', 'description']
    search_fields = ['product__number', 'product__name', 'language__iso_639_1', 'language__iso_639_2', 'language__family', 'language__name', 'language__native_name', 'language__wiki_url', 'name', 'description']
    autocomplete_fields = ['product', 'customer', 'language']


class SDSReplacementAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'language', 'product', 'search_for', 'replace_with']
    search_fields = ['product__number', 'product__name', 'search_for', 'replace_with']
    ordering = ['product__number']
    autocomplete_fields = ['product', 'customer', 'language']


class SDSRTFFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'language', 'file']
    search_fields = ['product__number', 'product__name', 'language__name', 'file_name', 'file_path']
    ordering = ['product__number']
    autocomplete_fields = ['product', 'language']


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
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ContactType, ContactTypeAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(EuroExchangeRate, EuroExchangeRateAdmin)
admin.site.register(PackagingRateToLiter, PackagingRateToLiterAdmin)
admin.site.register(BomHeader, BomHeaderAdmin)
admin.site.register(BomComponent, BomComponentAdmin)
admin.site.register(Bom, BomAdmin)
admin.site.register(UnitOfMeasureConversionFactor, UnitOfMeasureConversionFactorAdmin)
admin.site.register(ManualCost, ManualCostAdmin)
admin.site.register(Rebate, RebateAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(SDSReplacement, SDSReplacementAdmin)
admin.site.register(SDSRTFFile, SDSRTFFileAdmin)
