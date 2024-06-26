# dictionaries used in the views.py import_data function
from . import models
from inx_platform_app.models import User

# Table with index column
mapping_Users = {
    'ID_SalesManager': 'ID_SalesManager',
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'email': 'email',
}

mapping_ColorGroups = {
    'ColorGroupID': 'ColorGroupID',
    'ColorGroup': 'name'
}

mapping_Divisions = {
    'DivisionID': 'DivisionID',
    'DivisionName': 'name'
}

mapping_MadeIn={
    'MadeInID': 'MadeInID',
    'PlantNumber': 'plant_number',
    'PlantName': 'plant_name',
    'MadeIn': 'name'
}

mapping_MajorLabels = {
    'MajorLabelID': 'MajorLabelID',
    'Major Label': 'name'
}

mapping_InkTechnologies = {
    'InkTechnologyID': 'InkTechnologyID',
    'InkTechnology': 'name'
}

mapping_NSFDivisions = {
    'NSFDivisionID': 'NSFDivisionID',
    'NSFDivision': 'name'
}

mapping_MarketSegments = {
    'ID': 'ID',
    'MarketSegment': 'name',
    'SAP_ID': 'sap_id'
}

mapping_MaterialGroups = {
    'ID': 'ID',
    'MaterialGroup': 'name',
    'SAP_ID': 'sap_id'
}

mapping_PackagingTypes = {
    'PackagingTypeID': 'PackagingTypeID',
    'Packaging': 'name',
    'RateToLT': 'rate_to_lt',
    'SAP_ID': 'sap_id'
}

mapping_ProductStatuses = {
    'ProductStatusID': 'ProductStatusID',
    'ProductStatus': 'name',
    'ColorR': 'color_r',
    'ColorG': 'color_g',
    'ColorB': 'color_b',
    'ColorA': 'color_a',
}

mapping_UoM = {
    'ID': 'ID',
    'UoM': 'name'
}

mapping_ExchangeRates = {
    'ID': 'ID',
    'Currency': 'currency',
    'Year': 'year',
    'Rate': 'rate'
}

mapping_Scenarios = {
    'ID': 'ID',
    'Scenario': 'name'
}

mapping_Country_codes = {
    'CountryID': 'CountryID',
    'ISO3166-1-Alpha-3': 'iso3166_1_alpha_3',
    'ISO3166-1-Alpha-2': 'iso3166_1_alpha_2',
    # 'Intermediate Region Code': 'intermediate_region_code',
    'Intermediate Region Name': 'intermediate_region_name',
    'ISO4217-currency_name': 'iso4217_currency_name',
    'ISO4217-currency_numeric_code': 'iso4217_currency_numeric_code',
    'ISO4217-currency_alphabetic_code': 'iso4217_currency_alphabetic_code',
    'ISO4217-currency_minor_unit': 'iso4217_currency_minor_unit',
    'ISO4217-currency_country_name': 'iso4217_currency_country_name',
    'UNTERM English Short': 'uniterm_english_short',
    'UNTERM English Formal': 'uniterm_english_formal',
    'Region Code': 'region_code',
    'Region Name': 'region_name',
    'Sub-region Code': 'sub_region_code',
    'Sub-region Name': 'sub_region_name',
    'Continent': 'continent',
    'Global Name': 'global_name',
    'Capital': 'capital',
    'official_name_en': 'official_name_en',
    'CLDR display name': 'cldr_display_name'
}

mapping_CustomerTypes = {
    'CustomerTypeID': 'CustomerTypeID',
    'CustomerType': 'name'
}

# Tables without index columns

mapping_Fbl5nArrImport = {
    'DocumentDate': 'document_date',
    'NetDueDate': 'net_due_date',
    'Arrears': 'arrears',
    'AmountInDocCurr': 'amount_in_doc_currency',
    'DocCurr': 'doc_currency',
    'DocType': 'doc_type',
    'CustomerNumber': 'customer_number',
    'DocNumber': 'doc_number',
    'InvoiceNumber': 'invoice_number',
    'PaymentTerms': 'payment_terms',
    'InvoiceRef': 'invoice_reference',
    'PaymentDate': 'payment_date',
    'DebCred': 'deb_cred'
}

mapping_Fbl5nOpenImport = {  
    'DocumentDate': 'document_date',
    'NetDueDate': 'net_due_date',
    'Arrears': 'arrears',
    'AmountInDocCurr': 'amount_in_doc_currency',
    'DocCurr': 'doc_currency',
    'DocType': 'doc_type',
    'CustomerNumber': 'customer_number',
    'DocNumber': 'doc_number',
    'InvoiceNumber': 'invoice_number',
    'PaymentTerms': 'payment_terms',
    'InvoiceRef': 'invoice_reference',
    'PaymentDate': 'payment_date',
    'DebCred': 'deb_cred'
}

mapping_Ke24ImportLine = {
    'Currency': 'currency',
    'CurrencyType': 'currency_type',
    'RecordType': 'record_type',
    'YearMonth': 'year_month',
    'DocumentNumber': 'document_number',
    'ItemNumber': 'item_number',
    'CreatedOn': 'created_on',
    'ReferenceDocument': 'reference_document',
    'ReferenceItemNo': 'referenceitem_no',
    'CreatedBy': 'created_by',
    'CompanyCode': 'company_code',
    'SenderCostCenter': 'sender_cost_center',
    'CostElement': 'cost_element',
    'CurrencyKey': 'currency_key',
    'SalesQuantity': 'sales_quantity',
    'UnitSalesQuantity': 'unit_sales_quantity',
    'YearWeek': 'year_week',
    'Product': 'product',
    'IndustryCode1': 'industry_code_1',
    'Industry': 'industry',
    'PostingDate': 'posting_date',
    'SalesDistrict': 'sales_district',
    'ReferenceOrgUnit': 'reference_org_unit',
    'LogSystemSource': 'log_system_source',
    'ReferenceTransaction': 'reference_transaction',
    'PointOfValuation': 'point_of_valuation',
    'Revenue': 'revenue',
    'InvoiceDate': 'invoice_date',
    'BillingType': 'billing_type',
    'Year': 'year',
    'BusinessArea': 'business_area',
    'CustomerHierarchy01': 'customer_Hierarchy_01',
    'CustomerHierarchy02': 'customer_hierarchy_02',
    'CustomerHierarchy03': 'customer_hierarchy_03',
    'CustomerHierarchy04': 'customer_hierarchy_04',
    'CustomerHierarchy05': 'customer_hierarchy_05',
    'Origin': 'origin',
    'HierarchyAssignment': 'hierarchy_assignment',
    'AnnualRebates': 'annual_rebates',
    'SalesOrder': 'sales_order',
    'CustomerGroup': 'customer_group',
    'SalesOrderItem': 'sales_order_item',
    'Customer': 'customer',
    'ControllingArea': 'controlling_area',
    'PriceGroup': 'price_group',
    'MaterialPricingGroup': 'material_pricing_group',
    'CostObject': 'cost_object',
    'CustomerAccountAssignmentGroup': 'customer_account_assignment_group',
    'ShiToParty': 'ship_to_party',
    'ExchangeRate': 'exchange_rate',
    'Country': 'country',
    'Client': 'client',
    'MaterialGroup': 'material_group',
    'QuantityDiscount': 'quantityDiscount',
    'MarketSegment': 'market_segment',
    'Color': 'color',
    'MajorLabel': 'major_label',
    'BrandName': 'brand_name',
    'ColorGroup': 'color_group',
    'ProfitabilitySegmentNo': 'profitability_segment_no',
    'PartnerProfSegment': 'partner_prof_segment',
    'PartSubNumber': 'part_sub_number',
    'SubNumber': 'sub_number',
    'Period': 'period',
    'PlanActIndicator': 'plan_act_indicator',
    'PartnerProfitCenter': 'partner_profit_center',
    'DyeInk': 'dye_ink',
    'ProfitCenter': 'profit_center',
    'ProductHierarchy': 'product_hierarchy',
    'SenderBusinessProcess': 'sender_business_process',
    'WBSElement': 'WBS_element',
    'CurrencyOfRecord': 'currency_of_record',
    'Order': 'order',
    'UpdateStatus': 'update_status',
    'Division': 'division',
    'CanceledDocument': 'canceled_document',
    'CanceledDocumentItem': 'canceled_document_item',
    'TimeCreated': 'time_created',
    'Date': 'date',
    'Time': 'time',
    'Version': 'version',
    'SalesOrg': 'sales_org',
    'SalesEmployee': 'sales_employee',
    'DistributionChannel': 'distribution_channel',
    'CostOfSales': 'cost_of_sales',
    'Inplant_Depreciation': 'inplant_depreciation',
    'FreightCharges': 'freight_charges',
    'MTS_InputVar': 'mts_input_var',
    'MTS_InputPriveVar': 'mts_input_priveVar',
    'MTS_LotsizeVar': 'mts_lotsize_var',
    'MTO_FixFreightCost': 'mto_fix_freight_cost',
    'MTO_FixMaterialCost': 'mto_fix_material_cost',
    'MTO_VariableMaterialCost': 'mto_variable_material_cost',
    'MTO_FixOverheadCost': 'mto_fix_overhead_cost',
    'MTO_VariableOverheadCost': 'mto_variable_overhead_cost',
    'MTO_FixProductionCost': 'mto_fix_production_cost',
    'MTS_OutputPriceVar': 'mts_output_price_var',
    'MTO_VariableProductionCost': 'mto_variable_production_cost',
    'Inplant_OtherExpenses': 'inplant_other_expenses',
    'Inplant_Payroll': 'inplant_payroll',
    'MTS_QuantityVar': 'mts_quantity_var',
    'MTS_RemainingVar': 'mts_remaining_var',
    'MTS_ResUsageVar': 'mts_res_usage_var',
    'MTS_FixFreightCost': 'mts_fix_freight_cost',
    'MTS_FixMaterialCost': 'mts_fix_material_cost',
    'MTS_VariableMaterialCost': 'mts_variable_material_cost',
    'MTS_FixOverheadCost': 'mts_fix_overhead_cost',
    'MTS_VarialbleOverheadCost': 'mts_varialble_overhead_cost',
    'MTS_FixProductionCost': 'mts_fix_production_cost',
    'MTS_VariableProductionCost': 'mts_variable_production_cost',
    'GoodsIssueDate': 'goods_issue_date',
    'Plant': 'plant',
    'NationalAccountManager': 'national_account_manager',
    'ProductLine': 'product_line',
    'VPSales': 'vp_sales',
    'ProductLineSalesManager': 'product_line_sales_manager',
    'FieldSalesManager': 'field_sales_manager',
}

mapping_Ke24Line = {
    'Currency': 'currency',
    'CurrencyType': 'currency_type',
    'RecordType': 'record_type',
    'YearMonth': 'year_month',
    'DocumentNumber': 'document_number',
    'ItemNumber': 'item_number',
    'CreatedOn': 'created_on',
    'ReferenceDocument': 'reference_document',
    'ReferenceItemNo': 'referenceitem_no',
    'CreatedBy': 'created_by',
    'CompanyCode': 'company_code',
    'SenderCostCenter': 'sender_cost_center',
    'CostElement': 'cost_element',
    'CurrencyKey': 'currency_key',
    'SalesQuantity': 'sales_quantity',
    'UnitSalesQuantity': 'unit_sales_quantity',
    'YearWeek': 'year_week',
    'Product': 'product',
    'IndustryCode1': 'industry_code_1',
    'Industry': 'industry',
    'PostingDate': 'posting_date',
    'SalesDistrict': 'sales_district',
    'ReferenceOrgUnit': 'reference_org_unit',
    'LogSystemSource': 'log_system_source',
    'ReferenceTransaction': 'reference_transaction',
    'PointOfValuation': 'point_of_valuation',
    'Revenue': 'revenue',
    'InvoiceDate': 'invoice_date',
    'BillingType': 'billing_type',
    'Year': 'year',
    'BusinessArea': 'business_area',
    'CustomerHierarchy01': 'customer_Hierarchy_01',
    'CustomerHierarchy02': 'customer_hierarchy_02',
    'CustomerHierarchy03': 'customer_hierarchy_03',
    'CustomerHierarchy04': 'customer_hierarchy_04',
    'CustomerHierarchy05': 'customer_hierarchy_05',
    'Origin': 'origin',
    'HierarchyAssignment': 'hierarchy_assignment',
    'AnnualRebates': 'annual_rebates',
    'SalesOrder': 'sales_order',
    'CustomerGroup': 'customer_group',
    'SalesOrderItem': 'sales_order_item',
    'Customer': 'customer',
    'ControllingArea': 'controlling_area',
    'PriceGroup': 'price_group',
    'MaterialPricingGroup': 'material_pricing_group',
    'CostObject': 'cost_object',
    'CustomerAccountAssignmentGroup': 'customer_account_assignment_group',
    'ShiToParty': 'ship_to_party',
    'ExchangeRate': 'exchange_rate',
    'Country': 'country',
    'Client': 'client',
    'MaterialGroup': 'material_group',
    'QuantityDiscount': 'quantityDiscount',
    'MarketSegment': 'market_segment',
    'Color': 'color',
    'MajorLabel': 'major_label',
    'BrandName': 'brand_name',
    'ColorGroup': 'color_group',
    'ProfitabilitySegmentNo': 'profitability_segment_no',
    'PartnerProfSegment': 'partner_prof_segment',
    'PartSubNumber': 'part_sub_number',
    'SubNumber': 'sub_number',
    'Period': 'period',
    'PlanActIndicator': 'plan_act_indicator',
    'PartnerProfitCenter': 'partner_profit_center',
    'DyeInk': 'dye_ink',
    'ProfitCenter': 'profit_center',
    'ProductHierarchy': 'product_hierarchy',
    'SenderBusinessProcess': 'sender_business_process',
    'WBSElement': 'WBS_element',
    'CurrencyOfRecord': 'currency_of_record',
    'Order': 'order',
    'UpdateStatus': 'update_status',
    'Division': 'division',
    'CanceledDocument': 'canceled_document',
    'CanceledDocumentItem': 'canceled_document_item',
    'TimeCreated': 'time_created',
    'Date': 'date',
    'Time': 'time',
    'Version': 'version',
    'SalesOrg': 'sales_org',
    'SalesEmployee': 'sales_employee',
    'DistributionChannel': 'distribution_channel',
    'CostOfSales': 'cost_of_sales',
    'Inplant_Depreciation': 'inplant_depreciation',
    'FreightCharges': 'freight_charges',
    'MTS_InputVar': 'mts_input_var',
    'MTS_InputPriveVar': 'mts_input_priveVar',
    'MTS_LotsizeVar': 'mts_lotsize_var',
    'MTO_FixFreightCost': 'mto_fix_freight_cost',
    'MTO_FixMaterialCost': 'mto_fix_material_cost',
    'MTO_VariableMaterialCost': 'mto_variable_material_cost',
    'MTO_FixOverheadCost': 'mto_fix_overhead_cost',
    'MTO_VariableOverheadCost': 'mto_variable_overhead_cost',
    'MTO_FixProductionCost': 'mto_fix_production_cost',
    'MTS_OutputPriceVar': 'mts_output_price_var',
    'MTO_VariableProductionCost': 'mto_variable_production_cost',
    'Inplant_OtherExpenses': 'inplant_other_expenses',
    'Inplant_Payroll': 'inplant_payroll',
    'MTS_QuantityVar': 'mts_quantity_var',
    'MTS_RemainingVar': 'mts_remaining_var',
    'MTS_ResUsageVar': 'mts_res_usage_var',
    'MTS_FixFreightCost': 'mts_fix_freight_cost',
    'MTS_FixMaterialCost': 'mts_fix_material_cost',
    'MTS_VariableMaterialCost': 'mts_variable_material_cost',
    'MTS_FixOverheadCost': 'mts_fix_overhead_cost',
    'MTS_VarialbleOverheadCost': 'mts_varialble_overhead_cost',
    'MTS_FixProductionCost': 'mts_fix_production_cost',
    'MTS_VariableProductionCost': 'mts_variable_production_cost',
    'GoodsIssueDate': 'goods_issue_date',
    'Plant': 'plant',
    'NationalAccountManager': 'national_account_manager',
    'ProductLine': 'product_line',
    'VPSales': 'vp_sales',
    'ProductLineSalesManager': 'product_line_sales_manager',
    'FieldSalesManager': 'field_sales_manager',
}

mapping_ZACODMI9_import_line = {
    'Billing date': 'billing_date',
    'Material': 'material',
    'Description': 'description',
    'Sold to': 'sold_to',
    'Name': 'name',
    'BillingDoc': 'billing_doc',
    'Invoice Qty': 'invoice_qty',
    'UoM': 'UoM',
    'Unit Price': 'unit_price',
    'Invoice Sales': 'invoice_sales',
    'Curr.': 'curr',
    'Batch': 'batch',
    'GM (%)': 'gm_perc',
    'Prof': 'prof',
    'PTrm': 'ptrm',
    'Curr..1': 'curr_1',
    'Cost': 'cost',
    'Can': 'can',
    'Bill': 'bill',
    'Item': 'item',
    'Tax amount': 'tax_amount',
    'Curr..2': 'curr_2',
    'Dv': 'dv',
    'ShPt': 'shpt',
    'SalesDoc': 'sales_doc',
    'ImportDate': 'import_date',
}

mapping_ZACODMI9_line = {
    'Billing date': 'billing_date',
    'Material': 'material',
    'Description': 'description',
    'Sold to': 'sold_to',
    'Name': 'name',
    'BillingDoc': 'billing_doc',
    'Invoice Qty': 'invoice_qty',
    'UoM': 'UoM',
    'Unit Price': 'unit_price',
    'Invoice Sales': 'invoice_sales',
    'Curr.': 'curr',
    'Batch': 'batch',
    'GM (%)': 'gm_perc',
    'Prof': 'prof',
    'PTrm': 'ptrm',
    'Curr..1': 'curr_1',
    'Cost': 'cost',
    'Can': 'can',
    'Bill': 'bill',
    'Item': 'item',
    'Tax amount': 'tax_amount',
    'Curr..2': 'curr_2',
    'Dv': 'dv',
    'ShPt': 'shpt',
    'SalesDoc': 'sales_doc',
    'ImportDate': 'import_date',
}

mapping_Ke30ImportLine = {
    'Period/year': 'period_year',
    'Customer': 'customer',
    'Sales Qty Actual': 'sales_qty_actual',
    'Field Sales Mgr': 'field_sales_manager',
    'Field Sales Mgr1': 'field_sales_mgr_1',
    'Customer1': 'customer_1',
    'Product': 'product',
    'Product1': 'product_1',
    'Unit Sales quantity': 'unit_sales_quantity',
    'Net Sales Actual': 'net_sales_actual',
    'Rebates Actual': 'rebate_actual',
    'Gross Sales Actual': 'gross_sales_actual',
    'RMC Actual': 'rmc_actual',
    'Conversion Actual': 'conversion_actual',
    'Other Cost Actual': 'other_cost_actual',
    'Total Costs Actual': 'total_cost_actual',
    'Gross Margin Actual': 'gross_margin_actual',
    'Margin % Actual': 'margin_perc_actual',
    'Contribution Margin Actual': 'contribution_margin_actual',
    'N#Sales/unit Actual': 'net_sales_unit_actual',
    'Cost/Unit Actual': 'cost_unit_actual',
    'CustomerHierarchy01': 'customer_hierarchy_01',
    'CustomerHier01': 'customer_hier_01',
    'Disc/Claims/Adj Actual': 'disc_claim_adj_actual',
    'Material Group': 'material_group',
    'Material Group1': 'material_group_1',
    'Product hierarchy': 'product_hierarchy',
    'Prod#hierarchy': 'prod_hierarchy',
    'Color': 'color',
    'Color1': 'color_1',
    'Product Line': 'product_line',
    'Product Line1': 'product_line_1',
    'VP Sales': 'vp_sales',
    'Cust#Acct#Assg#Group': 'cust_acct_Assg_group',
    'CustAcctAssgGrp': 'cust_acct_Assg_grp',
    'Profit Center': 'profit_center',
    'Currency': 'currency',
    'Profit Center1': 'profit_center_1',
    'Unit of Measure': 'unit_of_measure',
    'Market Segment': 'market_segment',
    'Market Segment1': 'market_segment_1',
    'Major Label': 'major_label',
    'Major Label1': 'major_label_1',
    'National Account Mgr': 'national_account_manager',
    'National Account Mgr1': 'national_account_manager_1',
    'C#Margin % Actual': 'contribution_margin_perc_actual',
    'Fiscal Year': 'fiscal_year',
    'Fiscal Year1': 'fiscal_year_1',
    'Country': 'country',
    'Country1': 'country_1',
    'Sales employee': 'sales_employee',
    'Sales employee1': 'sales_employee_1',
    'Sales district': 'sales_district',
    'Sales district1': 'sales_district_1',
    'Color Group': 'color_group',
    'Color Group1': 'color_group_1',
    'Material pricing grp': 'material_pricing_grp',
    'Mat#pricing grp': 'mat_pricing_grp',
    'Price group': 'price_group',
    'Price group1': 'price_group_1',
    'Industry': 'industry',
    'Industry1': 'industry_1',
    'Brand Name': 'brand_name',
    'Brand Name1': 'brand_name_1',
    'Period': 'period',
    'Period1': 'period_1',
    'Division': 'division',
    'Division1': 'division_1',
    'Period/year1': 'period_year_1',
    'Ship-to party': 'ship_to_party',
    'Ship-to party1': 'ship_to_party_1',
    'ImportTimestamp': 'import_timestamp',
    'YearMonth': 'year_month',
}

mapping_Ke30Line = {
    'Currency': 'currency',
    'Month': 'month',
    'Year': 'year',
    'YearMonth': 'year_month',
    'FakeDate': 'fake_date',
    'CustomerNumber': 'customer_number',
    'CustomerName': 'customer_name',
    'CountrySAP': 'sap_country',
    'SalesDistrictSAP': 'sap_sales_district',
    'SalesEmployeeSAP': 'sap_sales_employee',
    'CustomerAccountGroup': 'customer_account_group',
    'Ship-to party Number': 'ship_to_party_number',
    'Ship-to party Name': 'ship_to_party_name',
    'ProductNumber': 'product_number',
    'ProductName': 'product_name',
    'BrandSAP': 'sap_brand',
    'MajorLabelSAP': 'sap_major_label',
    'DivisionSAP': 'sap_division',
    'MaterialGroupSAP': 'sap_material_group',
    'MarketSegmentSAP': 'sap_market_segment',
    'IndustrySAP': 'sap_industry',
    'ColorSAP': 'sap_color',
    'ProductLineSAP': 'sap_product_line',
    'ProfitCenterSAP': 'sap_profit_center',
    'UoM': 'sap_UOM',
    'Quantity': 'quantity',
    'Unit Sales quantity': 'unit_sales_quantity',
    'Net Sales': 'net_sales',
    'Rebates': 'rebates',
    'Gross Sales': 'gross_sales',
    'RMC': 'rmc_costs',
    'Conversion': 'conversion_costs',
    'Other Costs': 'other_costs',
    'Total Costs': 'total_costs',
    'GrossMargin': 'gross_margin',
    'GM-perc': 'gross_margin_perc',
    'Margin % Actual': 'margin_perc_actual',
    'Contribution Margin Actual': 'contribution_margin_actual',
    'C#Margin % Actual': 'contribution_margin_perc_actual',
    'N#Sales/unit Actual': 'net_sales_unit_actual',
    'Cost/Unit Actual': 'cost_unit_actual',
    'Disc/Claims/Adj Actual': 'disc_claim_adj_actual',
    'ImportTimestamp': 'import_timestamp',
}

# Tables with ForeignKeys

mapping_Color = {
    'ColorID': 'ColorID',
    'Color': 'name',
    'ColorGroupID': 'color_group_id',
    'ColorWeight': 'color_weight',
    'HexValue': 'hex_value',
    'ColorNumber': 'color_number',
    'ColorShort': 'name_short'
}

mapping_Brand = {
    'BrandID': 'BrandID',
    'Brand': 'name',
    'DivisionID': 'division_id',
    'MajorLabelID': 'major_label_id',
    'InkTechnologyID': 'ink_technology_id',
    'NSFDivisionID': 'nsf_division_id',
    'MarketSegmentID': 'market_segment_id',
    'MaterialGroupID': 'material_group_id',
    'SAPBrandCode': 'sap_id',
    'SAPBrandName': 'sap_name',
    'NoBudget': 'no_budget'
}

mapping_Product = {
    'ProductID': 'ProductID',
    'ProductNumber': 'number',
    'ProductName': 'name',
    'isInk': 'is_ink',
    'ColorID': 'color_id',
    'MadeInID': 'made_in_id',
    'BrandID': 'brand_id',
    'PackagingID': 'packaging_id',
    'Status': 'product_status_id'
}

mapping_Customers = {
    'CustomerID': 'CustomerID',
    'CustomerNumber': 'number',
    'CustomerName': 'name',
    'Active': 'active',
    'Insurance': 'insurance_value',
    'VAT': 'vat',
    'CreditLimit': 'credit_limit',
    'CountryID': 'country_id',
    'CustomerTypeID': 'customer_type_id',
    'Currency': 'currency',
    'ApprovedBy': 'approved_by_old',
    'ApprovedOn': 'approved_on',
    'email': 'email',
    'SalesEmployeeID': 'sales_employee_id'
}

mapping_Rate_to_LT = {
    'ID': 'ID',
    'UoMID': 'uom_id',
    'PackagingTypeID': 'packaging_id',
    'RateToLT': 'rate_to_lt'
}

        # List of tables without ForeignKeys
        # and their ID field name in the SQL database and the model in the django app

mapping_BudFor = {
    'ID': 'ID',
    'CustomerID': 'customer_id',
    'BrandID': 'brand_id',
    'ColorGroupID': 'color_group_id'
}

mapping_BudForDetails = {
    'ID': 'ID',
    'BudForID': 'budforline_id',
    'ScenarioID': 'scenario_id',
    'DetailDate': 'detail_date',
    'Year': 'year',
    'MonthNumber': 'month',
    'Price': 'price',
    'Volume': 'volume',
    'Value': 'value',
    'Currency_zaq': 'currency_zaq'
}

# List of teable that we are importing
tables_list = [
    ("Users", "ID_SalesManager", User, mapping_Users),
    ("ColorGroups", "ColorGroupID", models.ColorGroup, mapping_ColorGroups),
    ("Divisions", "DivisionID", models.Division, mapping_Divisions),
    ("MadeIn", "MadeInID", models.MadeIn, mapping_MadeIn),
    ("MajorLabels", "MajorLabelID", models.MajorLabel, mapping_MajorLabels),
    ("InkTechnologies", "InkTechnologyID", models.InkTechnology, mapping_InkTechnologies),
    ("NSFDivisions", "NSFDivisionID", models.NSFDivision, mapping_NSFDivisions),
    ("MarketSegments", "ID", models.MarketSegment, mapping_MarketSegments),
    ("MaterialGroups", "ID", models.MaterialGroup, mapping_MaterialGroups),
    ("PackagingTypes", "PackagingTypeID", models.Packaging, mapping_PackagingTypes),
    ("ProductStatuses", "ProductStatusID", models.ProductStatus, mapping_ProductStatuses),
    ("UoM", "ID", models.UnitOfMeasure, mapping_UoM),
    ("ExchangeRates", "ID", models.ExchangeRate, mapping_ExchangeRates),
    ("Scenarios", "ID", models.Scenario, mapping_Scenarios),
    ("Country_Codes", "CountryID", models.CountryCode, mapping_Country_codes),
    ("CustomerTypes", "CustomerTypeID", models.CustomerType, mapping_CustomerTypes),
    
    # ("FBL5N_arr_import", None, models.Fbl5nArrImport, mapping_Fbl5nArrImport),
    # ("FBL5N_open_import", None, models.Fbl5nOpenImport, mapping_Fbl5nOpenImport),
    # ("KE24_import", None, models.Ke24ImportLine, mapping_Ke24ImportLine),
    # ("ZAQCODMI9_import", None, models.ZACODMI9_import_line, mapping_ZACODMI9_import_line),
    # ("KE30_import", None, models.Ke30ImportLine, mapping_Ke30ImportLine),
    
    ("Colors", "ColorID", models.Color, mapping_Color),
    ("Brands", "BrandID", models.Brand, mapping_Brand),
    ("RateToLT", "ID", models.RateToLT, mapping_Rate_to_LT),

    ("Products", "ProductID", models.Product, mapping_Product),
    ("Customers", "CustomerID", models.Customer, mapping_Customers),
    
    ("_BudFor", 'ID', models.BudForLine, mapping_BudFor),
    ("_BudForDetails", "ID", models.BudForDetailLine, mapping_BudForDetails),
    ("BudgetForecastDetails", "ID", models.BudgetForecastDetail, mapping_BudForDetails),

    ("Sales.KE24", None, models.Ke24Line, mapping_Ke24Line),
    ("Sales.ZAQCODMI9", None, models.ZAQCODMI9_line, mapping_ZACODMI9_line),
    ("Sales.Ke30", None, models.Ke30Line, mapping_Ke30Line),
]
