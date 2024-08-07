from celery import Celery, shared_task, current_task, group, chord
from django.utils import timezone
from celery.utils.log import get_task_logger
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import Max
from django.contrib.admin.models import ADDITION, CHANGE
from .models import *
from .utils import *
from . import import_dictionaries
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import time
import os
import pprint
import requests
from loguru import logger as django_logger
import xml.etree.ElementTree as ET


# app = Celery('core_app', broker='redis://localhost:6379/0')
celery_logger = get_task_logger(__name__)


@shared_task
def file_processor(id_of_UploadedFile, user_id):
    bom_work = False
    # Get celery task id
    celery_task_id = current_task.request.id

    # Get the UploadedFile record via the id
    uploaded_file_record = get_object_or_404(UploadedFile, pk=id_of_UploadedFile)
    user = get_object_or_404(User, pk=user_id)
    if not uploaded_file_record:
        celery_logger.error(f"No UploadedFile record with id: {id_of_UploadedFile}")
        return
    if not os.path.exists(uploaded_file_record.file_path + "/" + uploaded_file_record.file_name):
        celery_logger.error(f"File does not exist.")
        return
    
    celery_logger.info(
        f"the file {uploaded_file_record.file_path + '/' + uploaded_file_record.file_name} has been found is ready to process"
        )
    
    # Create the first log line in the log table
    post_a_log_message(id_of_UploadedFile, user_id, celery_task_id, f"process {celery_task_id} started")

    # What type is the file
    # Preparing variables according to file_type
    match uploaded_file_record.file_type:
        case "ke30":
            df = read_this_file(uploaded_file_record, user, import_dictionaries.ke30_converters_dict, celery_task_id)
            if not df.empty:
                df['Importtimestamp'] = datetime.now()
                df["YearMonth"] = (df['Fiscal Year'].astype(int) * 100 + df['Period'].astype(int)).astype(str)
                # These 2 variable are set for the following action, after the match-case
                model = Ke30ImportLine
                field_mapping = import_dictionaries.ke30_mapping_dict
                list_of_sp =['_ke30_import', '_ke30_import_add_new_customers', '_ke30_import_add_new_products']
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "ke24":
            df = read_this_file(uploaded_file_record,user, import_dictionaries.ke24_converters_dict, celery_task_id)
            if not df.empty:
                df = df.drop(columns=['Industry Code 1'])               
                model = Ke24ImportLine
                field_mapping = import_dictionaries.ke24_mapping_dict
                list_of_sp =[]
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "zaq":
            df = read_this_file(uploaded_file_record,user, import_dictionaries.zaq_converters_dict, celery_task_id)
            if not df.empty:
                df["Billing date"] = df['Billing date'].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else x)
                # This Excel file has the totals,at teh bottom, that must be removed
                # The number of rows may vary depending on the number of currencies and UoMs mentioned
                unique_uom = df['UoM'].nunique()
                unique_curr = df['Curr.'].nunique()
                rows_to_remove = max(unique_curr, unique_uom)
                df = df.head(len(df) - rows_to_remove) 
                model = ZAQCODMI9_import_line
                field_mapping = import_dictionaries.zaq_mapping_dict
                # Store procedure are importing from import table to full table
                # Then deleting sales from budfordetailline
                # Then backing up budfordetailline
                # Then filling in again sales from zaq with proper granularity
                list_of_sp = ['_zaq_import', '_budforline_add_triplets', '_budgetforecastdetail_fill_sales']
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "oo":
            df = read_this_file(uploaded_file_record,user, import_dictionaries.oo_converters_dict, celery_task_id)
            if not df.empty:
                df['LineType'] = 'OO'
                print(f"it was {len(df)}")
                uniques = len(df['Unit'].value_counts())
                df = df.iloc[:-uniques]
                print(f"it is {len(df)}")
                df = df[df["Plant"].notnull()]
                df["Order Date"] = df['Order Date'].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else x)
                df["Req. dt"] = df['Req. dt'].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else x)
                df["PL. GI Dt"] = df['PL. GI Dt'].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else x)
                df['Sold-to'] = df['Sold-to'].fillna(df['Ship-to'])
                df['Sold-to'] = np.where(df['Sold-to'] == '', df['Ship-to'], df['Sold-to'])
                model = Order
                field_mapping = import_dictionaries.oo_mapping_dict
                list_of_sp =[]
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "oi" | "arr":
            df = read_this_file(uploaded_file_record,user, import_dictionaries.oo_converters_dict, celery_task_id)
            if not df.empty:
                uniques = len(df['Document currency'].value_counts())
                df = df.iloc[:-uniques]
                print(f"{uploaded_file_record.file_type} is now {len(df)} lines long")
                # Adjusting dates
                df['Document Date'] = df['Document Date'].dt.date
                df['Net due date'] = df['Net due date'].dt.date
                df['Payment date'] = df['Payment date'].dt.date
                df['Arrears after net due date'] = df['Arrears after net due date'].fillna(0).astype(int)
                if uploaded_file_record.file_type == "arr":
                    model = Fbl5nArrImport
                    field_mapping = import_dictionaries.arr_mapping_dict
                if uploaded_file_record.file_type == "oi":
                    model = Fbl5nOpenImport
                    field_mapping = import_dictionaries.oi_mapping_dict
                list_of_sp =[]
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "pr":
            df = read_this_file(uploaded_file_record, user, import_dictionaries.pr_converters_dict, celery_task_id)
            if not df.empty:
                model = Price
                field_mapping = import_dictionaries.prl_mapping_dict
                list_of_sp =[]
            else:
                celery_logger.error(f"file could not be read - {uploaded_file_record}")
                return
        case "boms":
            bom_work = True
            celery_logger.info("About to start reading")
            df = read_this_file(uploaded_file_record, user, import_dictionaries.boms_converters_dict, celery_task_id)
            # start tasks
            if not df.empty:
                # Start task of Materials
                df['Finished Material'].replace('', np.nan, inplace=True)
                df.dropna(subset=['Finished Material'], inplace=True)
                df = df[df['Plant'] == '8800']
                # Adding new products or updating current ones
                unique_materials = df['Finished Material'].unique()
                all_unique_materials = len(unique_materials)
                material_counter = 0
                # get the marked for deletion product status
                mark_for_del = get_object_or_404(ProductStatus, marked_for_deletion = True)
                for material in unique_materials:
                    material_counter += 1
                    description = df.loc[df['Finished Material'] == material, 'Finished Material Desc'].values[0]
                    # created is True if the product has to be created
                    product, created = Product.objects.get_or_create(number=material)
                    if created:
                        product.name = description
                        product.is_new = True
                        if is_fert(material):
                            product.is_fert = True
                        product.save()
                        create_log_entry(user, product, ADDITION, f'Product imported by importing BOMs file: {product.id} {product.name}')
                    else:
                        if is_fert(material):
                            product.is_fert = True
                            product.save()
                        if product.name != description:
                            old_value = product.name
                            product.name = description
                            product.save()
                            logmessage = f'Product name changed by importing BOMs from {old_value} to {description}'
                            create_log_entry(user,product, CHANGE, logmessage)
                    if product.name.startswith('+'):
                        product.product_status = mark_for_del
                        product.save()
                    if material_counter % 100 == 0:
                        celery_logger.info(f"materials: {material_counter}/{len(unique_materials)}")
                celery_logger.info(f"Materials completed")
                # Adding new component or updating current ones
                # Count unique bom_component_sap_num values
                unique_component_count = df['Component Material'].nunique()
                celery_logger.info(f"Unique component materials count: {unique_component_count}")
                component_counter = 0
                for bom_component_sap_num in df['Component Material'].unique():
                    component_counter += 1
                    bom_comp_description = df.loc[df['Component Material'] == bom_component_sap_num, 'Component Material Desc'].values[0]
                    bom_comp_base_uom = df.loc[df['Component Material'] == bom_component_sap_num, 'Comp Base UoM'].values[0]
                    bom_component, created = BomComponent.objects.get_or_create(component_material=bom_component_sap_num)
                    if created:
                        bom_component.component_material_description = bom_comp_description
                        bom_component.component_base_uom = bom_comp_base_uom
                        bom_component.save()
                        logmessage = f'BOM component imported by importing BOMs file: {bom_component.id} {bom_component.component_material} {bom_component.component_material_description}'
                        create_log_entry(user, bom_component, ADDITION, logmessage)
                    else:
                        if bom_component.component_material_description != bom_comp_description:
                            old_value = bom_component.component_material_description
                            bom_component.component_material_description = bom_comp_description
                            bom_component.save()
                            logmessage = f'BOM component desc changed by importing BOMs from {old_value} to {bom_comp_description}'
                            create_log_entry(user,bom_component, CHANGE, logmessage)
                    if component_counter % 100 == 0:
                        celery_logger.info(f"BOM Component: {component_counter}/{unique_component_count}")
                celery_logger.info(f"BOM Component completed")
                
                # Working on BOM Headers
                unique_headers = df.drop_duplicates(subset=['Finished Material', 'Finished Material Desc', 'Alt BOM'])
                all_unique_headers = len(unique_headers)
                celery_logger.info(f"len of unique_headers: {all_unique_headers}")
                count_of_unique_headers = 0
                for _, header in unique_headers.iterrows():
                    count_of_unique_headers += 1
                    product_number = header['Finished Material']
                    alt_bom = header['Alt BOM']
                    header_base_quantity = header['Header Base Qty']
                    header_base_quantity_uom = header['Hdr Base Qty UoM']
                    product = get_object_or_404(Product, number = product_number)
                    if product:
                        header_base_quantity = float(header_base_quantity)
                        header_base_quantity_uom = str(header_base_quantity_uom).strip()
                        bom_header, created = BomHeader.objects.get_or_create(
                            product=product,
                            alt_bom=alt_bom,
                            defaults={
                                'header_base_quantity': header_base_quantity,
                                'header_base_quantity_uom': header_base_quantity_uom
                            }
                        )
                        if created:
                            logmessage = f'BOM header created for {bom_header.product.number} {bom_header.product.name} alt_bom: {alt_bom}'
                            create_log_entry(user, bom_header, ADDITION, logmessage)
                    if count_of_unique_headers % 100 == 0:
                        celery_logger.info(f"BOM headers: {count_of_unique_headers}/{all_unique_headers}")
                celery_logger.info(f"Bom headers completed")
                # Finished working on BOM headers
                # Start working on BOMs
                # slice the file
                bom_chunk_size = 3000
                df_chunks = slice_dataframe(df, bom_chunk_size)
                celery_logger.info(f"Total number of bom_chunks: {len(df_chunks)}")
                chunk_counter = 0
                number_of_chunks = len(df_chunks)
                for df_chunk in df_chunks:
                    chunk_counter += 1
                    chunk_dict = df_chunk.to_dict(orient='records')
                    process_the_bom_slice_task.delay(chunk_dict, user.id, chunk_counter, number_of_chunks)
                # Adding or updating Bom records
                # for _, row in df.iterrows():
                #     product_number = row['Finished Material']
                #     alt_bom = row['Alt BOM']
                #     item_number = row['Item Number']
                #     component_material = row['Component Material']
                #     component_quantity = row['Comp Qty']
                #     component_uom_in_bom = row['Comp UoM in BOM']
                #     price_unit = row['Price Unit']
                #     standard_price_per_unit = row['Std Pr Per Unit/Comp']

                #     product = get_object_or_404(Product, number=product_number)
                #     bom_header = get_object_or_404(BomHeader, product=product, alt_bom=alt_bom)
                #     bom_component = get_object_or_404(BomComponent, component_material=component_material)

                #     bom, created = Bom.objects.update_or_create(
                #         bom_header=bom_header,
                #         bom_component=bom_component,
                #         defaults={
                #             'item_number': item_number,
                #             'component_quantity': component_quantity,
                #             'component_uom_in_bom': component_uom_in_bom,
                #             'price_unit': price_unit,
                #             'standard_price_per_unit': standard_price_per_unit
                #         }
                #     )
                #     if created:
                #         logmessage = f'BOM record created for {bom_header.product.number} {bom_header.product.name} component: {bom_component.component_material}'
                #         create_log_entry(user, bom, ADDITION, logmessage)
                #     else:
                #         logmessage = f'BOM record updated for {bom_header.product.number} {bom_header.product.name} component: {bom_component.component_material}'
                #         create_log_entry(user, bom, CHANGE, logmessage)
                # # Finished working on Boms
            else:
                print("error reading the file")
            pass
    # celery_logger.info(f"model: {model}")
    
    ####################################################################################
    # Start inserting
    ####################################################################################
    if bom_work == False:
        model.objects.all().delete()
        post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"deleting rows from {model._meta.model_name}")
        df_length = len(df)
        df = df.replace(np.nan, '')
        chunk_size = 500
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        chunk_counter = 0
        for chunk in chunks:
            chunk_counter += 1
            post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"processing ... {chunk_counter}/{len(chunks)}")
            try:
                start_time = time.perf_counter()
                # List to hold model instances
                instances = []
                for index, row in chunk.iterrows():
                    instance = model()
                    for field, column_name in field_mapping.items():
                        setattr(instance, field, row[column_name])
                    instances.append(instance)
                with transaction.atomic():
                    model.objects.bulk_create(instances)
                    post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f'bulk_create for chunk {chunk_counter} done')
                    instances = [] # resetting
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"working on chunk {chunk_counter} of {len(chunks)}  -  it took {elapsed_time} seconds")
            except Exception as e:
                # Handle the exception
                post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"An error occurred during the transaction: {e}")
        # All chunks are processed
        post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"All chuncks are processed")
        uploaded_file_record.is_processed = True
        uploaded_file_record.processed_at = timezone.make_aware(datetime.now())
        # Working on the stored procedures now
        if list_of_sp:
            post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"There are {len(list_of_sp)} stored procedures. {list_of_sp}")
            with connection.cursor() as curs:
                for index, sp in enumerate(list_of_sp):
                    with transaction.atomic():
                        sql_command = f"EXECUTE {sp}"
                        try:
                            curs.execute(sql_command)
                        except Exception as e:
                            message = f"Error during execution of {sp}. {e}" 
                            post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, message, "error")
                            return
                        if curs.description:
                            resulting_rows = curs.fetchall()
                            post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"resulting rows from sp {sp}.")
                            for row in resulting_rows:
                                row_text = ', '.join(map(str, row))
                                post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, row_text)
        
    # Delete the file
    post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"deleting ... {uploaded_file_record.file_name}")
    if uploaded_file_record.delete_file_soft():
        post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, f"File {uploaded_file_record.file_name} removed and db updated")
    else:
        log_message = f"There is a problem with file name {uploaded_file_record.file_name} - 'process terminated for file id: {uploaded_file_record.id}  filetye: {uploaded_file_record.file_type} file_name: {uploaded_file_record.file_name} file_path: {uploaded_file_record.file_path}"
        post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, log_message)
    log_message = f'process terminated for file id: {uploaded_file_record.id}  filetye: {uploaded_file_record.file_type} file_name: {uploaded_file_record.file_name} file_path: {uploaded_file_record.file_path}'
    post_a_log_message(uploaded_file_record.id, user_id, celery_task_id, log_message)
    uploaded_file_record.save()


def post_a_log_message(id_of_UploadedFile, user_id, celery_task_id, message, level="info"):
    uploaded_file_record = get_object_or_404(UploadedFile, pk=id_of_UploadedFile)
    user = get_object_or_404(User, pk=user_id)
    log = UploadedFileLog.objects.create(
        uploaded_file = uploaded_file_record,
        user = user,
        file_path = uploaded_file_record.file_path,
        file_name = uploaded_file_record.file_name,
        celery_task_id = celery_task_id,
        log_text = message
    )
    if level == "info":
        celery_logger.info(message)
    else:
        celery_logger.error(message)


def read_this_file(the_file, user, conversion_dictionary, celery_task_id):
    user_id = user.id
    uploaded_file_id = the_file.id
    full_file_name = the_file.file_path + "/" + the_file.file_name
    post_a_log_message(uploaded_file_id, user_id, celery_task_id, f"start reading {full_file_name}")
    df = the_file.read_excel_file(full_file_name, conversion_dictionary)
    if not df.empty:
        post_a_log_message(uploaded_file_id, user_id, celery_task_id, f"completed reading Excel file {full_file_name}")
        return df
    else:
        return False


@shared_task
def ticker_task():
    for iteration in range(10):
        time.sleep(1)
        celery_logger.info(f"ticker_task: tick {iteration}")
    return "ticker_task completed"


@shared_task
def very_long_task():
    for number in range(50):
        time.sleep(.3)
        celery_logger.info(f"number: {number}")
    return"task 50x completed!"


@shared_task
def fetch_euro_exchange_rates():

    # Get the latest year from the EuroExchangeRate model
    latest_year_subquery = EuroExchangeRate.objects.aggregate(latest_year=Max('year'))
    latest_year = latest_year_subquery['latest_year']

    # Get the latest month for the latest year
    if latest_year is not None:
        latest_month_subquery = EuroExchangeRate.objects.filter(year=latest_year).aggregate(latest_month=Max('month'))
        latest_month = latest_month_subquery['latest_month']
    else:
        latest_month = None

    celery_logger.info(f'latest_year {latest_year}')
    celery_logger.info(f'latest_month {latest_month}')


    if latest_year is None or latest_month is None:
        start_date = datetime(2000, 1, 1)  # If no data exists, start from a default early date
    else:
        start_date = datetime(latest_year, latest_month, 1)



    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        celery_logger.info(f"root:{root}")
        namespaces = {'gesmes': 'http://www.gesmes.org/xml/2002-08-01',
                      '': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

        celery_logger.info(f"namespaces: {namespaces}")

        valid_currency_codes = set(Currency.objects.values_list('alpha_3', flat=True))
        rates_data = {}
        for cube in root.findall('.//Cube[@time]', namespaces):
            date_str = cube.attrib['time']
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Skip dates before the start_date
            if date < start_date:
                continue

            year, month = date.year, date.month

            for rate in cube.findall('.//Cube[@currency]', namespaces):
                currency_code = rate.attrib['currency']
                if currency_code not in valid_currency_codes:
                    continue
                
                exchange_rate = Decimal(rate.attrib['rate']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                # Initialize nested dictionaries if not already present
                if year not in rates_data:
                    rates_data[year] = {}
                if month not in rates_data[year]:
                    rates_data[year][month] = {}
                if currency_code not in rates_data[year][month]:
                    rates_data[year][month][currency_code] = {'sum': 0, 'count': 0}

                print(f"year: {year} month: {month} currency: {currency_code}; exchange rate: {exchange_rate}")
                rates_data[year][month][currency_code]['sum'] += exchange_rate
                rates_data[year][month][currency_code]['count'] += 1

        for year in rates_data:
            for month in rates_data[year]:
                for currency_code in rates_data[year][month]:
                    total_sum = rates_data[year][month][currency_code]['sum']
                    count = rates_data[year][month][currency_code]['count']
                    average_rate = total_sum / count if count else 0

                    try:
                        currency = Currency.objects.get(alpha_3=currency_code)
                        EuroExchangeRate.objects.update_or_create(
                            currency=currency,
                            year=year,
                            month=month,
                            defaults={'rate': average_rate}
                        )
                        celery_logger.info(f"{year}-{month}-{currency_code}-avg: {average_rate}")
                    except Currency.DoesNotExist:
                        celery_logger.warning(f"Currency with code {currency_code} does not exist.")
                        continue
        celery_logger.info("EUR exchange rates update completed")
    else:
        celery_logger.info(f"Failed to fetch data: {response.status_code}")


@shared_task
def process_the_bom_slice_task(chunk_dict, user_id, counter, all_chunks):
    stamp = f"{counter}/{all_chunks}"
    celery_logger.warning(f"process_the_bom_slice_task started - {stamp}")
    df = pd.DataFrame(chunk_dict)
    len_df = len(df)
    user = get_object_or_404(User, pk=user_id)
    # Start working on BOMs
    # Adding or updating Bom records
    slice_row = 0
    for _, row in df.iterrows():
        slice_row += 1
        product_number = row['Finished Material']
        alt_bom = row['Alt BOM']
        item_number = row['Item Number']
        component_material = row['Component Material']
        component_quantity = row['Comp Qty']
        component_uom_in_bom = row['Comp UoM in BOM']
        price_unit = row['Price Unit']
        standard_price_per_unit = row['Std Pr Per Unit/Comp']
        # celery_logger.info(f"{stamp}|{product_number}|{alt_bom}|{item_number}|{component_material}|{component_quantity}|{component_uom_in_bom}")

        product = get_object_or_404(Product, number=product_number)
        bom_header = get_object_or_404(BomHeader, product=product, alt_bom=alt_bom)
        bom_component = get_object_or_404(BomComponent, component_material=component_material)

        bom, created = Bom.objects.update_or_create(
            bom_header=bom_header,
            bom_component=bom_component,
            defaults={
                'item_number': item_number,
                'component_quantity': component_quantity,
                'component_uom_in_bom': component_uom_in_bom,
                'price_unit': price_unit,
                'standard_price_per_unit': standard_price_per_unit
            }
        )
        # if slice_row % 100 == 00:
        #     celery_logger.error(f"process {stamp}: {slice_row}/{len_df}")
        # if created:
        #     logmessage = f'BOM record created for {bom_header.product.number} {bom_header.product.name} component: {bom_component.component_material}'
        #     # create_log_entry(user, bom, ADDITION, logmessage)
        # else:
        #     logmessage = f'BOM record updated for {bom_header.product.number} {bom_header.product.name} component: {bom_component.component_material}'
        #     # create_log_entry(user, bom, CHANGE, logmessage)
    # Finished working on Boms
    celery_logger.warning(f"process_the_bom_slice_task stopped - {stamp}")

def slice_dataframe(dataframe, chunk_size):
    chunks = [dataframe.iloc[i:i + chunk_size] for i in range(0, dataframe.shape[0], chunk_size)]
    return chunks