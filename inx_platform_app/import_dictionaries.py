import datetime

# Converters section

ke30_converters_dict = {
    'Customer': str,
    'Customer.1': str,
    'Product': str,
    'Product.1': str,
    'Profit Center': str,
    'Profit Center.1': str,
    'Period/Year': str,
    'Period/Year.1': str,
    'Material Group': str,
    'Material Group.1': str,
    'Product Hierarchy': str,
    'Prod.hierarachy':str,
    'Cust.Acct.Assg.Group': str,
    'AccAssmtGrpCust':str,
    'Fiscal Year': str,
    'Fiscal Year.1': str,
    'Sales employee': str,
    'Sales employee.1': str,
    'CustomerHierarchy01': str,
    'CustomerHier01': str,
    'Sales district': str,
    'Sales district.1': str,
    'Period': str,
    'Period.1': str,
    'Material pricing grp': str,
    'Mat.pricing grp': str,
    'Price group': str,
    'Price group.1': str,
    'Division': str,
    'Division.1': str,
    'Color': str,
    'Color.1': str,
    'Color Group': str,
    'Color Group.1': str,
    'Product Line': str,
    'Product Line.1': str,
    'Market Segment': str,
    'Mareket Segment.1': str,
    'Major Label': str,
    'Major Label.1': str,
    'Industry': str,
    'Industry.1': str,
    'Brand Name': str,
    'Brand Name.1': str,
    'Country': str,
    'Country.1': str,
    'Currency': str,
    'Unit of Measure': str,
    'Ship-to party': str,
    'Ship-to party.1': str,
    'National Account Mgr':str,
    'National Account Mgr.1':str,
    'Field Sales Mgr': str,
    'Field Sales Mgr.1': str,
    'Unit Sales quantity':str,
    'VP sales': str
}

ke24_converters_dict = {
    "Currency": str,
    "CurrencyType": str,
    "RecordType": str,
    "YearMonth": str,
    "DocumentNumber": str,
    "ItemNumber": str,
    "ReferenceDocument": str,
    "ReferenceItemNo": str,
    "CreateBy": str,
    "CompanyCode": str,
    "SenderCostCenter": str,
    "CostElement": str,
    "CurrencyKey": str,
    "CostElement": str,
    "CurrencyKey": str,
    "SalesQuantity": str,
    "UnitSalesQuantity": str,
    "YearWeek": str,
    "Product": str,
    "IndustryCode1": str,
    "Industry": str,
    "SalesDistrict": str,
    "ReferenceOrgUnit": str,
    "LogSystemSource": str,
    "ReferenceTransaction": str,
    "PointOfValuation": str,
    "BillingType": str,
    "BusinessArea": str,
    "CustomerHierarchy01": str,
    "CustomerHierarchy02": str,
    "CustomerHierarchy03": str,
    "CustomerHierarchy04": str,
    "CustomerHierarchy05": str,
    "Origin": str,
    "SalesOrder": str,
    "CustomerGroup": str,
    "Customer": str,
    "ControllingArea": str,
    "PriceGroup": str,
    "MaterialPricingGroup": str,
    "CostObject": str,
    "CustomerAccountAssignmentGroup": str,
    "ShiToParty": str,
    "Country": str,
    "Client": str,
    "MaterialGroup": str,
    "MarketSegment": str,
    "Color": str,
    "MajorLabel": str,
    "BrandName": str,
    "ColorGroup": str,
    "ProfitabilitySegmentNo": str,
    "PartnerProfSegment": str,
    "PartSubNumber": str,
    "SubNumber": str,
    "PartnerProfitCenter": str,
    "DyeInk": str,
    "ProfitCenter": str,
    "ProductHierarchy": str,
    "SenderBusinessProcess": str,
    "WBSElement": str,
    "CurrencyOfRecord": str,
    "Order": str,
    "Update status": str,
    "Division": str,
    "CanceledDocument": str,
    "CanceledDocumentItem": str,
    "TimeCreated": str,
    "Version": str,
    "SalesOrg": str,
    "SalesEmployee": str,
    "DistributionChannel": str,
    "Plant": str,
    "NationalAccountManager": str,
    "ProductLine": str,
    "VPSales": str,
    "ProductLineSalesManager": str,
    "FieldSalesManager": str,

    "CreateOn": 'datetime64[ns]',
    "PostingDate": 'datetime64[ns]',
    "InvoiceDate": 'datetime64[ns]',
    "Date": 'datetime64[ns]',
    # "Time": 'datetime64[ns]',
    # "Time": "%H:%M:%S",
    "GoodsIssueDate": 'datetime64[ns]',

    "Year": int,
    "HierarchyAssignment": int,
    "SalesOrderItem": int,
    "Period": int,
    "PlanActIndicator": int,

    "SalesQuantity": float,
    "Revenue": float,
    "AnnualRebates": float,
    "ExchangeRate": float,
    "QuantityDiscount": float,
    "CostOfSales": float,
    "Inplant_Depreciation": float,
    "FreightCharges": float,
    "MTS_InputVar": float,
    "MTS_InputPriveVar": float,
    "MTS_LotsizeVar": float,
    "MTO_FixFreightCost": float,
    "MTO_FixMaterialCost": float,
    "MTO_VariableMaterialCost": float,
    "MTO_FixOverheadCost": float,
    "MTO_VariableOverheadCost": float,
    "MTO_FixProductionCost": float,
    "MTS_OutputPriceVar": float,
    "MTO_VariableProductionCost": float,
    "Inplant_OtherExpenses": float,
    "Inplant_Payroll": float,
    "MTS_QuantityVar": float,
    "MTS_RemainingVar": float,
    "MTS_ResUsageVar": float,
    "MTS_FixFreightCost": float,
    "MTS_FixMaterialCost": float,
    "MTS_VariableMaterialCost": float,
    "MTS_FixOverheadCost": float,
    "MTS_VarialbleOverheadCost": float,
    "MTS_FixProductionCost": float,
    "MTS_VariableProductionCost": float
    }

zaq_converters_dict = {
    'Material': str,
    'Description': str,
    'Name': str,
    'BillingDoc': str,
    'Invoice Qty': str,
    'UoM': str,
    'Unit Price': str,
    'Invoice Sales': str,
    'Curr.': str,
    'Batch': str,
    'GM (%)': str,
    'Prof': str,
    'PTrm': str,
    'Curr..1': str,
    'Cost':str,
    'Can': str,
    'Bill':str,
    'Item': str,
    'Tax amount': str,
    'Curr..2': str,
    'Dv': str,
    'ShPt': str,
    'Sold to': str,
    'Sales doc.': float #,
    # 'Billing date': datetime.date
}

oo_converters_dict = {
    "CustomerNumber": float,
    "Ship_to": float,
    "ValueInvoiced": float,

    "SalesOrderDate": datetime,
    "RequestedDate": datetime ,
    "PartialShipmentDate": datetime ,
    "InvoiceDate": datetime,
    "DeliveryDate": datetime,
    "ImportDate": datetime,

    "CustomerName": str,
    "Country": str,
    "Plant": str,
    "SalesOrderNumber": str,
    "StoreLocation": str,
    "OrderType": str,
    "ProductNumber": str,
    "ProductName": str,
    "QtyOrdered_unit": str,
    "QtyOpen_unit": str,
    "QtyPartialShipped_unit": str,
    "CustomerPONumber": str,
    "LineType": str,
    "InvoiceNumber": str,
    "DocumentCurrency": str,
    "QtyInvoiced_unit": str,

    "ItemLineNumber": int,
    "DaysLate": int,
    "QtyOrdered": int,
    "QtyOpen": int,
    "QtyPartialShipped": int,
    "LeadTime": int,
    "DeliveryNumber": int,
    "QtyInvoiced": int
}

oit_converters_dict = {
    "Document Date": datetime.date,
    "Net due date": datetime.date,
    "Arrears after net due date": float,
    "Amount in doc. curr.": float,
    "Document currency":str,
    "Document type": str,
    # "Account": int,
    "Document Number": str,
    "Billing Document": str,
    "Term of Payment": str,
    "Invoice reference": str,
    "Payment date": datetime.date,
    "Debit/Credit ind": str
}

arr_converters_dict = {
    "Document Date": datetime.date,
    "Net due date": datetime.date,
    "Arrears after net due date": float,
    "Amount in doc. curr.": float,
    "Document currency":str,
    "Document type": str,
    # "Account": int,
    "Document Number": str,
    "Billing Document": str,
    "Term of Payment": str,
    "Invoice reference": str,
    "Payment date": datetime.date,
    "Debit/Credit ind": str
}

pr_converters_dict = {
    "SOrg": str,
    "Customer": str,
    # "CustomerNumber": int,
    "Customer Name": str,
    # "ProductID": int,
    "Material": str,
    "Material Description": str,
    "Scale Qty From": int,
    "Scale Qty To": int,
    "Price": float,
    "Per": int,
    "UoM": str,
    # "Volume_From": int,
    # "Volume_To": int,
    "Start Date": datetime.date,
    "End Date": datetime.date,
    "Curr": str
}

# Mappings section

ke30_mapping_dict = {
    "period_year": "Period/Year",
    "period_year_1": "Period/Year.1",
    "customer": "Customer",
    "sales_qty_actual": "Sales Qty Actual",
    "field_sales_manager": "Field Sales Mgr",
    "field_sales_mgr_1": "Field Sales Mgr.1",
    "customer_1": "Customer.1",
    "product": "Product",
    "product_1": "Product.1",
    "unit_sales_quantity": "Unit Sales quantity",
    "net_sales_actual": "Net Sales Actual",
    "rebate_actual": "Rebates Actual",
    "gross_sales_actual": "Gross Sales Actual",
    "rmc_actual": "RMC Actual",
    "conversion_actual": "Conversion Actual",
    "other_cost_actual": "Other Cost Actual",
    "total_cost_actual": "Total Costs Actual",
    "gross_margin_actual": "Gross Margin Actual",
    "margin_perc_actual": "Margin % Actual",
    "contribution_margin_actual": "Contribution Margin Actual",
    "contribution_margin_perc_actual": "C.Margin % Actual",
    "net_sales_unit_actual": "N.Sales/unit Actual",
    "cost_unit_actual": "Cost/Unit Actual",
    "customer_hierarchy_01": "CustomerHierarchy01",
    "customer_hier_01": "CustomerHier01",
    "disc_claim_adj_actual": "Disc/Claims/Adj Actual",
    "material_group": "Material Group",
    "material_group_1": "Material Group.1",
    "product_hierarchy": "Product hierarchy",
    "prod_hierarchy": "Prod.hierarchy",
    "color": "Color",
    "color_1": "Color.1",
    "product_line": "Product Line",
    "product_line_1": "Product Line.1",
    "vp_sales": "VP Sales",
    "cust_acct_Assg_group": "Cust.Acct.Assg.Group",
    "cust_acct_Assg_grp": "AccAssmtGrpCust",
    "profit_center": "Profit Center",
    "profit_center_1": "Profit Center.1",
    "currency": "Currency",
    "unit_of_measure": "Unit of Measure",
    "market_segment": "Market Segment",
    "market_segment_1": "Market Segment.1",
    "major_label": "Major Label",
    "major_label_1": "Major Label.1",
    "national_account_manager": "National Account Mgr",
    "national_account_manager_1": "National Account Mgr.1",
    "fiscal_year": "Fiscal Year",
    "fiscal_year_1": "Fiscal Year.1",
    "country": "Country",
    "country_1": "Country.1",
    "sales_employee": "Sales employee",
    "sales_employee_1": "Sales employee.1",
    "sales_district": "Sales district",
    "sales_district_1": "Sales district.1",
    "color_group": "Color Group",
    "color_group_1": "Color Group.1",
    "material_pricing_grp": "Material pricing grp",
    "mat_pricing_grp": "Mat.pricing grp",
    "price_group": "Price group",
    "price_group_1": "Price group.1",
    "industry": "Industry",
    "industry_1": "Industry.1",
    "brand_name": "Brand Name",
    "brand_name_1": "Brand Name.1",
    "period": "Period",
    "period_1": "Period.1",
    "division": "Division",
    "division_1": "Division.1",
    "ship_to_party": "Ship-to party",
    "ship_to_party_1": "Ship-to party.1",
    "import_timestamp": "Importtimestamp",
    "year_month": "YearMonth",
}

ke24_mapping_dict = {
    "currency": "Currency",
    "currency_type": "Currency type",
    "record_type": "Record Type",
    "year_month": "Period/Year",
    "document_number": "Document number",
    "item_number": "Item number",
    "created_on": "Created On",
    "reference_document": "Reference document",
    "referenceitem_no": "Reference item no.",
    "created_by": "Created By",
    "company_code": "Company Code",
    "sender_cost_center": "Sender cost center",
    "cost_element": "Cost Element",
    "currency_key": "Currency key",
    "sales_quantity": "Sales quantity",
    "unit_sales_quantity": "Unit Sales quantity",
    "year_week": "Week/year",
    "product": "Product",
    # "industry_code_1": "Industry Code 1",
    "industry": "Industry",
    "posting_date": "Posting date",
    "sales_district": "Sales district",
    "reference_org_unit": "Reference Org Unit",
    "log_system_source": "Log. system source",
    "reference_transaction": "Reference Transact.",
    "point_of_valuation": "Point of valuation",
    "revenue": "Revenue",
    "invoice_date": "Invoice date",
    "billing_type": "Billing Type",
    "year": "Fiscal Year",
    "business_area": "Business Area",
    "customer_Hierarchy_01": "CustomerHierarchy01",
    "customer_hierarchy_02": "CustomerHierarchy02",
    "customer_hierarchy_03": "CustomerHierarchy03",
    "customer_hierarchy_04": "CustomerHierarchy04",
    "customer_hierarchy_05": "CustomerHierarchy05",
    "origin": "Origin",
    "hierarchy_assignment": "Hierarchy Assignment",
    "annual_rebates": "Annual rebates",
    "sales_order": "Sales Order",
    "customer_group": "Customer group",
    "sales_order_item": "Sales Order Item",
    "customer": "Customer",
    "controlling_area": "Controlling Area",
    "price_group": "Price group",
    "material_pricing_group": "Material pricing grp",
    "cost_object": "Cost Object",
    "customer_account_assignment_group": "Cust.Acct.Assg.Group",
    "ship_to_party": "Ship-to party",
    "exchange_rate": "Exchange rate",
    "country": "Country",
    "client": "Client",
    "material_group": "Material Group",
    "quantityDiscount": "Qty discount",
    "market_segment": "Market Segment",
    "color": "Color",
    "major_label": "Major Label",
    "brand_name": "Brand Name",
    "color_group": "Color Group",
    "profitability_segment_no": "Profitab. Segmt No.",
    "partner_prof_segment": "Partner prof.segment",
    "part_sub_number": "Partner subnumber",
    "sub_number": "Subnumber",
    "period": "Period",
    "plan_act_indicator": "Plan/Act. Indicator",
    "partner_profit_center": "Partner Profit Ctr",
    "dye_ink": "Dye Ink",
    "profit_center": "Profit Center",
    "product_hierarchy": "Product hierarchy",
    "sender_business_process": "Sender bus. process",
    "WBS_element": "WBS Element",
    "currency_of_record": "Currency of record",
    "order": "Order",
    "update_status": "Update status",
    "division": "Division",
    "canceled_document": "Canceled document",
    "canceled_document_item": "Canceled doc. item",
    "time_created": "Time created",
    "date": "Date",
    "time": "Time",
    "version": "Version",
    "sales_org": "Sales Organization",
    "sales_employee": "Sales employee",
    "distribution_channel": "Distribution Channel",
    "cost_of_sales": "Cost of Sales - SD",
    "inplant_depreciation": "INPLANT - depreciat.",
    "freight_charges": "Freight Charges",
    "mts_input_var": "MTS -Input var.",
    "mts_input_priveVar": "MTS -Inp. prive var.",
    "mts_lotsize_var": "MTS -Lotsize var.",
    "mto_fix_freight_cost": "MTO -Fix.Freight Cst",
    "mto_fix_material_cost": "MTO -Fix.Mater. Cst",
    "mto_variable_material_cost": "MTO -Vbl.Mater. Cst",
    "mto_fix_overhead_cost": "MTO -Fix.Overh. Cst",
    "mto_variable_overhead_cost": "MTO -Vbl.Overh. Cst",
    "mto_fix_production_cost": "MTO -Fix.Prod. Cst",
    "mts_output_price_var": "MTS -Outp. price var",
    "mto_variable_production_cost": "MTO -Vbl.Prod. Cst",
    "inplant_other_expenses": "INPLANT - other exp.",
    "inplant_payroll": "INPLANT - payroll",
    "mts_quantity_var": "MTS -Quantity var.",
    "mts_remaining_var": "MTS -Remaining var.",
    "mts_res_usage_var": "MTS -Res. usage var.",
    "mts_fix_freight_cost": "MTS -Fix.Freight Cst",
    "mts_fix_material_cost": "MTS - Fix. mat. cost",
    "mts_variable_material_cost": "MTS - Vbl. mat. cost",
    "mts_fix_overhead_cost": "MTS -Fix.Overh. Cst",
    "mts_varialble_overhead_cost": "MTS -Vbl.Overh. Cst",
    "mts_fix_production_cost": "MTS -Fix.Prod. Cst",
    "mts_variable_production_cost": "MTS -Vbl.Prod. Cst",
    "goods_issue_date": "Goods Issue Date",
    "plant": "Plant",
    "national_account_manager": "National Account Mgr",
    "product_line": "Product Line",
    "vp_sales": "VP Sales",
    "product_line_sales_manager": "Prod Line Sls Mgr",
    "field_sales_manager": "Field Sales Mgr",
}

zaq_mapping_dict = {
    'billing_date':'Billing date',
    'material':'Material',
    'description':'Description',
    'sold_to':'Sold to',
    'name':'Name',
    'billing_doc':'BillingDoc',
    'invoice_qty':'Invoice Qty',
    'UoM':'UoM',
    'unit_price':'Unit Price',
    'invoice_sales':'Invoice Sales',
    'curr':'Curr.',
    'batch':'Batch',
    'gm_perc':'GM (%)',
    'prof':'Prof',
    'ptrm':'PTrm',
    'curr_1':'Curr..1',
    'cost':'Cost',
    'can':'Can',
    'bill':'Bill',
    'item':'Item',
    'tax_amount':'Tax amount',
    'curr_2':'Curr..2',
    'dv':'Dv',
    'shpt':'ShPt',
    'sales_doc':'Sales doc.'
}

oo_mapping_dict = {

}

oi_mapping_dict = {
    'document_date': 'Document Date',
    'net_due_date': 'Net due date',
    'arrears': 'Arrears after net due date',
    'amount_in_doc_currency': 'Amount in doc. curr.',
    'doc_currency': 'Document currency',
    'doc_type': 'Document Type',
    'customer_number': 'Account',
    'doc_number': 'Document Number',
    'invoice_number': 'Billing Document',
    'payment_terms': 'Terms of Payment',
    'invoice_reference': 'Invoice reference',
    'payment_date': 'Payment date',
    'deb_cred': 'Debit/Credit ind'
}

arr_mapping_dict = {
    'document_date': 'Document Date',
    'net_due_date': 'Net due date',
    'arrears': 'Arrears after net due date',
    'amount_in_doc_currency': 'Amount in doc. curr.',
    'doc_currency': 'Document currency',
    'doc_type': 'Document Type',
    'customer_number': 'Account',
    'doc_number': 'Document Number',
    'invoice_number': 'Billing Document',
    'payment_terms': 'Terms of Payment',
    'invoice_reference': 'Invoice reference',
    'payment_date': 'Payment date',
    'deb_cred': 'Debit/Credit ind'
}

prl_mapping_dict = {
    'customer_number': 'Customer',
    'customer_name': 'Customer Name',
    'product_number': 'Material',
    'product_name': 'Material Description',
    'price': 'Price',
    'per': 'Per',
    'UoM': 'UoM',
    'volume_from': 'Scale Qty From',
    'volume_to': 'Scale Qty To',
    'valid_from': 'Start Date',
    'valid_to': 'End Date',
    'currency': 'Curr'
}

