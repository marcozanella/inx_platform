from typing import Any
from django.apps import apps
from django.db.models.query import QuerySet
from django.db import connection
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import models, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from .models import Ke30ImportLine, Ke24ImportLine, ZACODMI9_import_line, Order, Fbl5nArrImport, Fbl5nOpenImport, Price
from .models import MadeIn, MajorLabel, ProductStatus
from .models import Brand, Product, Customer, InkTechnology, User
from .models import UploadedFile, StoredProcedure, Contact
from .forms import EditMajorLabelForm, EditBrandForm, EditCustomerForm, EditProductForm, StoredProcedureForm, CustomUserCreationForm, UserPasswordChangeForm, RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm
from .forms import ProductForm, CustomerForm, BrandForm
from .forms import get_generic_model_form
from . import dictionaries, import_dictionaries
import pyodbc
import pandas as pd
import numpy as np
import os, time, asyncio, uuid, json
from datetime import datetime
from time import perf_counter
from sqlalchemy import create_engine

def index(request):
    return render(request, "app_pages/index.html", {})

def index_original(request):
    return render(request, "app_pages/index_original.html", {})

def profile(request):
    return render(request, "app_pages/profile.html", {})

def index_inx(request):
    return render(request, "index-inx.html")

def account_settings(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'app_pages/settings.html', context)

@login_required
def loader(request):
    if request.method == "POST":

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        ke30_file = request.FILES.get('ke30_file')
        ke24_file = request.FILES.get('ke24_file')
        zaq_file = request.FILES.get('zaq_file')
        oo_file = request.FILES.get('oo_file')
        oh_file = request.FILES.get('oh_file')
        oi_file = request.FILES.get('oi_file')
        arr_file = request.FILES.get('arr_file')
        pr_file = request.FILES.get('pr_file')
        boms_file = request.FILES.get('boms_file')

        user_name = request.user.get_snakecase_name()

        files_list = [
            ('ke30_file', ke30_file),
            ('ke24_file', ke24_file),
            ('zaq_file', zaq_file),
            ('oo_file', oo_file),
            ('oh_file', oh_file),
            ('oi_file', oi_file),
            ('arr_file', arr_file),
            ('pr_file', pr_file),
            ('boms_file', boms_file),
        ]

        for file_field, original_file in files_list:
            if original_file is not None:
                original_file_nane = original_file.name.lower()
                prefix = file_field.split('_')[0]
                original_file_nane = prefix +"_" + user_name + "_" + timestamp + "_" + original_file_nane
                upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                with open(os.path.join(upload_dir, original_file_nane), 'wb+') as destination:
                    # for chunk in ke30_file.chunks():
                    for chunk in original_file.chunks():
                        destination.write(chunk)
                    # here it's done, update the database
                    uploaded_file = UploadedFile(owner=request.user, file_type=prefix, file_path=upload_dir, file_name=original_file_nane)
                    uploaded_file.save()
        return redirect('display_files')
    else:
        return render(request, "loader.html", {})


def update_profile(request):
    from django.shortcuts import render, redirect
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from django.contrib.auth.models import User

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if not first_name or not last_name or not email:
            messages.error(request, 'Please fill out all fields.')
            return redirect('account_settings')
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('account_settings')
        

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, 'Your profile was successfully updated!')
        return redirect('index') 
    else:
        return redirect('account_settings')


@login_required
def loading(request):
    if request.method == "POST":
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        ke30_file = request.FILES.get('ke30_file')
        ke24_file = request.FILES.get('ke24_file')
        zaq_file = request.FILES.get('zaq_file')
        oo_file = request.FILES.get('oo_file')
        oh_file = request.FILES.get('oh_file')
        oi_file = request.FILES.get('oi_file')
        arr_file = request.FILES.get('arr_file')
        pr_file = request.FILES.get('pr_file')
        boms_file = request.FILES.get('boms_file')

        user_name = request.user.get_snakecase_name()

        files_list = [
            ('ke30_file', ke30_file),
            ('ke24_file', ke24_file),
            ('zaq_file', zaq_file),
            ('oo_file', oo_file),
            ('oh_file', oh_file),
            ('oi_file', oi_file),
            ('arr_file', arr_file),
            ('pr_file', pr_file),
            ('boms_file', boms_file),
        ]

        are_all_empty = all(file is None for _, file in files_list)
        if are_all_empty:
            return render(request, "app_pages/index.html")

        for file_field, original_file in files_list:
            if original_file is not None:
                original_file_nane = original_file.name.lower()
                prefix = file_field.split('_')[0]
                print(f"prefix {prefix}")
                print(f"user_name {user_name}")
                print(f"timestamp {timestamp}")
                print(f"original_file_name {original_file_nane}")
                original_file_nane = prefix +"_" + user_name + "_" + timestamp + "_" + original_file_nane.replace(" ", "_")
                upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

                match prefix:
                    case 'ke30':
                        file_color = 'blue'
                    case 'zaq':
                        file_color = 'red'
                    case 'oo':
                        file_color = 'purple'
                    case 'ke24':
                        file_color = 'orange'
                    case 'oo':
                        file_color = 'green'
                    case 'oi':
                        fiile_color = 'cyan'
                    case 'arr':
                        file_color = 'indigo'
                    case 'pr':
                        file_color = 'indigo'
                    case _:
                        file_color = 'muted'

                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                with open(os.path.join(upload_dir, original_file_nane), 'wb+') as destination:
                    # for chunk in ke30_file.chunks():
                    for chunk in original_file.chunks():
                        destination.write(chunk)
                    # here it's done, update the database
                    uploaded_file = UploadedFile(owner=request.user, file_type=prefix, file_path=upload_dir, file_name=original_file_nane, file_color=file_color)
                    uploaded_file.save()
        return redirect('importing-files')
    else:
        return render(request, "app_pages/loading_data.html", {})


@login_required
def import_data(request):
    import_from_SQL(dictionaries.tables_list)
    return render(request, "index-inx.html")

def import_single(request):
    context = {'options': dictionaries.tables_list}
    if request.method == 'POST':
        submit_action = request.POST.get('submit_type')
        table_name = request.POST.get('table_name')
        filtered_tuple = [(t1, t2, t3, t4) for t1, t2, t3, t4 in dictionaries.tables_list if t1 == table_name]
        if submit_action == 'Import':
            import_from_SQL(filtered_tuple)
            messages.success(request, f"Import done on {table_name}")
        if submit_action == 'Clean':
            clean_the_table(filtered_tuple)
            messages.success(request, f"Clean done on {table_name}")
        return render(request, "import_single.html", context)
    else:
        return render(request, "import_single.html", context)

def import_from_SQL(table_tuples):
    host = os.getenv("DB_SERVER", default=None)
    if  host == None: host = 'localhost'
    database = os.getenv("ORIGINAL_DB_NAME", default=None)
    if database == None: database = 'INXD_Database'
    username = os.getenv("ORIGINAL_DB_USERNAME", default=None)
    if  username == None: username = 'sa'
    password = os.getenv("ORIGINAL_DB_PASSWORD", default=None)
    if password == None: password = "dellaBiella2!"
    driver = os.getenv("DB_DRIVER", None)
    if driver == None: driver = '{ODBC Driver 18 for SQL Server}'
   
    connection_string = f"DRIVER={driver};SERVER={host};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Connection Timeout=30;"
    # print(connection_string)
    try:        
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Connection Error: {str(e)}")
    # Working to import
    for table_name, field_name, model_class, mapping in table_tuples:
        # Query to get all records of the table
        query = f"SELECT * FROM {table_name}"
        msg = "startint to get rows ..."
        print(msg, end="")
        cursor.execute(query)
        records = cursor.fetchall()
        print("\r", " "* len(msg), end="")
        print(f"completed. {query}")
        if not records:
            print("no rows")
            continue # Skip empty tables
        how_many_records = len(records)
        print(' '*80,'\n','-'*80)
        print('SQL table name:', table_name, '-', how_many_records, "records")
        print('-'*80)
        # Get column names, in a list
        column_names = [column[0] for column in cursor.description]
        
        # Making a Dataframe
        data_dicts = [dict(zip(row.cursor_description, row)) for row in records]
        df = pd.DataFrame(data_dicts)
        df.columns = column_names
        df_length = len(df)
        print("Dataframe creation completed")
        
        # Manage the duplication of that user
        if table_name == 'Users': 
            for index, row in df.iterrows():
                if row['email'] == 'marco.zanella@inxeurope.com':
                    df.at[index, 'email'] = 'marco.zanella.sql@inxeurope.com'
                
                if row['email'] == 'stefano.rogora@inxeurope.com':
                    df.at[index, 'email'] = 'stefano.rogora.sql@inxeurope.com'

        # Manage the import of Customer number that comes as 12345.0
        if table_name == 'Customers':
            df['CustomerNumber'] = df['CustomerNumber'].astype(int).astype(str)
        
        # For testing
        # df = df.head(1)

        # Trim unnecessary columns
        columns_to_keep = [column for column in df.columns if column in mapping]
        df = df[columns_to_keep]
        # print("Columns to keep:", columns_to_keep)

        # creating a copy of the index column, if there is one
        if not field_name == None:
            df['sqlapp_id'] = df[field_name]
            df.drop(columns=[field_name], inplace=True)
            print("Copy of index line created")
        
        # When the tables have no index, the table will be truncated
        if field_name == None:
            model_class.objects.all().delete()
            print(f"All records from {model_class.__name__} have been deleted")

        # Changing column names
        for sql_column, django_field in mapping.items():
            # Rename the column using the mapping
            if sql_column in df.columns:
                df.rename(columns={sql_column: django_field}, inplace=True)
        print("Applied django column names")

        # Remove np.nan
        df = df.replace(np.nan, None)
        print("Removed np.nan")

        # Iterate through the model_class fields and detect data types
        for field in model_class._meta.get_fields():
            field_name = field.name
            if field_name in model_class._meta.fields_map: continue
            if field_name in df.columns:
                if isinstance(field, models.IntegerField):
                    df[field_name] = df[field_name].fillna(0)
                    df[field_name] = df[field_name].astype(int)
                elif isinstance(field, models.FloatField):
                    df[field_name] = df[field_name].fillna(0)
                    df[field_name] = df[field_name].astype(float)
                elif isinstance(field, models.DateTimeField):
                    df[field_name] = pd.to_datetime(df[field_name], errors='coerce')
                elif isinstance(field, models.CharField):
                    df[field_name] = df[field_name].fillna('')
                    df[field_name] = df[field_name].astype(str)


        # --------------------------------------------------
        # FOREIGN KEYS JOB
        # Here I am building a small list of lists
        # The innner list is built as follows
        # (app_db_column_name, Model)
        # --------------------------------------------------

        # Building model_fks_dict
        # This is a dictionary of foreign keys
        # key: name of the field
        # value: model_class referenced
        model_fks_dict = {}
        other_model_fks_dict = {}
        t_start = perf_counter()
        for field in model_class._meta.get_fields():
            if isinstance(field, models.ForeignKey):
                app_db_column_name = field.db_column
                # Perchè questo if qui sotto?
                if not app_db_column_name:
                    app_db_column_name = field.name + '_id'
                # model_fks_dict.update({app_db_column_name: field.related_model})
                #----------
                related_model = field.related_model
                related_objects = related_model.objects.all()
                related_df = pd.DataFrame(list(related_objects.values()))
                # Store the DataFrame in model_fks_dict
                other_model_fks_dict[app_db_column_name] = (related_model, related_df)
                # ------------

        # if model_fks_dict: pass
        # if other_model_fks_dict:
        #     print(f"FK fields of table {table_name}")
        #     for fk in other_model_fks_dict.items():
        #         print(f"-{fk}")
        print(f"created model FKs dictionary in {round(perf_counter()-t_start, 2):.2f} seconds")

        # Iterating to update FKs IDs
        # Iterate through the DataFrame
        t_start = perf_counter()
        for index, row in df.iterrows():
            print (f"row {index+1}/{df_length}", end="\r")
            for sql_column, django_field in mapping.items():
                if (sql_column == 'ID' and django_field == 'ID') or sql_column == django_field:
                    continue
                # --------------
                if django_field in other_model_fks_dict:
                    related_model, related_df = other_model_fks_dict[django_field]
                    # Get the SQL column value
                    sql_column_value = row[django_field]

                    # Look up the related model instance by sqlapp_id in the DataFrame
                    matching_rows = related_df.loc[related_df['sqlapp_id'] == sql_column_value]

                    if not matching_rows.empty:
                        # Get the first matching instance (if there is one)
                        found_results = True
                        related_instance = matching_rows.iloc[0]
                    else:
                        found_results = False

                    if found_results:
                        if not related_instance.empty:
                            # Update the DataFrame column with the related model's ID
                            df.at[index, django_field] = related_instance.id
                    else:
                        df.at[index, django_field] = None
                # -------------
        print(f"Update of FKs done in {round(perf_counter()-t_start, 2):.2f} seconds")
    
        # Removing from df those lines where sqlapp_id are already in the model records
        # Fetch existing sqlapp_id values from the model records
        if 'sqlapp_id' in df.columns:
            print(f"trimming df based on sqlapp_id values, df length={df_length}...", end="")
            existing_ids = set(model_class.objects.values_list('sqlapp_id', flat=True))
            # Filter the DataFrame to exclude rows with existing sqlapp_id values
            df = df[~df['sqlapp_id'].isin(existing_ids)]
            df_length = len(df)
            print ("done")
            print (f"df length after trimming = {df_length}")

        if df_length > 0:
            try:
                with transaction.atomic():
                    print("start atomic transaction")
                    instances_to_create = []
                    problematic_rows = []
                    row_counter = 1
                    for row in df.to_dict(orient='records'):
                        try:
                            instances_to_create.append(model_class(**row))
                            print(f"filling model instances ... {row_counter}/{df_length}", end="\r")
                            row_counter += 1
                        except Exception as ex:
                            problematic_rows.append((row, str(ex)))
                    print()
                    if problematic_rows:
                        print("Problematic Rows:")
                        for idx, (row_data, error_msg) in enumerate(problematic_rows):
                            print(f"Row {idx + 1}: {error_msg}\n{row_data}\n")
                    else:
                        print("no problematic rows")
                    
                    print(f"working on bulk_create - model {model_class.__name__}")
                    model_class.objects.bulk_create(instances_to_create)
                    print(f"Completed importing {table_name}")                 
            except Exception as e:
                print(e)
    conn.close() 


def get_pk_from_sqlapp_id(model_class, sqlapp_id_value):
    # print("model_class:", model_class.__name__, "\n input sqlapp_id_value:", sqlapp_id_value, end='')
    try:
        instance = model_class.objects.get(sqlapp_id=sqlapp_id_value)
        # print("\t returned pk value:", instance.pk)
        return instance.pk
    except model_class.DoesNotExist:
        # Handle the case where the instance is not found
        # print("instance not found")
        return None


@login_required
def clean_single(request):
    context = {'options': dictionaries.tables_list}
    if request.method == 'POST':
        selected_table = request.POST.get('selected_option', None)
        if selected_table:
            # filter the list of tuples and leave only the selected one
            filtered_tuple_list = [(t1, t2, t3, t4) for t1, t2, t3, t4 in dictionaries.tables_list if t1 == selected_table]
            clean_the_table(filtered_tuple_list)
            return render(request, "clean_single.html", context)
    else:
        return render(request, "clean_single.html", context)


def clean_the_table(tuple_list):
    # Take the name of the model from the tuple passed as argument
    model_to_clean = tuple_list[0][2]
    model_to_clean.objects.all().delete()

@login_required
def clean_db(request):

    list_of_table_names = [table[0] for table in dictionaries.tables_list]
    list_of_table_names.reverse()

    model_list = []
    for table in list_of_table_names:
        for item in dictionaries.tables_list:
            if table == item[0]: model_list.append(item[2])
    
    for model in model_list:
        if not model == User:
            model.objects.all().delete()
    
    return render(request, 'index-inx.html', {})

@login_required
def save_model(the_class, the_data, counter, all_records, logs=None):
    if the_class.__name__ == 'User':
        if the_data['email'] == 'marco.zanella@inxeurope.com':
            if the_data['first_name'] == 'Marco':
                the_data['email'] = "old_marco_zanella@inxeurope.com"
                the_data['first_name'] = "First"
                the_data['last_name'] = "Last"
            elif the_data['first_name'] == 'New':
                the_data['email'] = "new_business@inxeurope.com"
                the_data['first_name'] = "New"
                the_data['last_name'] = "Business"

    if 'sqlapp_id' in the_data:
        sql_app_to_find = the_data.get('sqlapp_id')
        rec_exists = the_class.objects.filter(sqlapp_id=sql_app_to_find)
        if not rec_exists:
            model_item = the_class(**the_data)
        else:
            model_item = None
    else:
        model_item = the_class(**the_data)
    if model_item:
        model_item.save()
        counter += 1
        message = f"saved ... {str(counter).zfill(6)} / {str(all_records).zfill(6)}"
        soglia =100
        if all_records < soglia:
            # print(" " * length_of_message, end="\r")
            print(message, end="\r")
            # print(message)
        if counter % soglia == 0:
            # print(" " * length_of_message, end="\r")
            print(message, end="\r")
            # print(message)
        if counter == all_records:
            # print(" " * length_of_message, end="\r")
            print(message, end="\r")
            # print(message)

        logs.append(f"Imported {the_class.__name__} - {counter}/{all_records}")
    else:
        print(50*' ', end='\r')
        print(f'skipping sqlapp_id {sql_app_to_find}', end='\r')
    return counter, logs

@login_required
def display_files(request):
    user = request.user
    user_files = UploadedFile.objects.filter(owner=user)
    
    return render(request, "display_files.html", {'user_files': user_files})

@login_required
def importing_files(request):
    user = request.user
    user_files = UploadedFile.objects.filter(owner=user, is_processed=False)
    return render(request, "app_pages/importing_files.html", {'user_files': user_files})

@login_required
def importing_files_x(request):
    
    if request.htmx:
        print("HTMX request")
        print ('trigger', request.htmx.trigger)
        print ('target', request.htmx.target)
        print ('boosted', request.htmx.boosted)
        return render(request, "app_pages/importing_files_x_partial.html")
    else:
        print("Normal request")
        user = request.user
        user_files = UploadedFile.objects.filter(owner=user, is_processed=False)
        return render(request, "app_pages/importing_files_x.html", {'user_files': user_files})

@login_required
def imported_files(request, page=0):
    user = request.user
    user_files = UploadedFile.objects.filter(owner=user, is_processed=True).order_by('-processed_at')
    
    items_per_page = 10

    paginator = Paginator(user_files.order_by('-processed_at'), items_per_page)
    # Get the current page from the GET request or in the URL
    if page != 0:
        page_number = page
    else:
        try:
            page_number = request.GET.get('page', 1)
        except (ValueError, TypeError):
            page_number = 1
        
    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)



    context = {
        'user_files': page_obj,
        'page_object': page_obj
        }
    return render(request, "app_pages/imported_files.html", context)

def start_processing(request, file_id):
    pass


@login_required
def start_file_processing(request, file_id):
    def event_stream():
        print("event_stream function")
        yield f'data:start yielding\n\n'
        file = get_object_or_404(UploadedFile, id = file_id)
        yield from process_this_file(file)
        
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    return response

def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id = file_id)
    try:
        file.delete_file()
    except FileNotFoundError as fnf:
        print(fnf)
        file.is_processed = False
        file.save()
    return redirect('importing-files')


def process_this_file(file):
    file_path = file.file_path + "/" + file.file_name
    log_text = ''
    list_of_sp = []
    if not os.path.exists(file_path):
        # The file does not exists
        log_message = f"data:The file {file_path} is not existing, marking the UploadedFile record as is_processed=True\n\n"
        yield log_message
        log_text += log_message + '\n'
        file.is_processed = True
        file.save()
    else:
        match file.file_type:
            case "ke30":
                convert_dict = import_dictionaries.ke30_converters_dict
                log_message = "data:start reading the Excel file\n\n"
                print(log_message)
                yield log_message
                log_text += log_message + '\n'
                df = file.read_excel_file(file_path, convert_dict)
                log_message = "data:completed reading the Excel file\n\n"
                print(log_message)
                yield log_message
                log_text += log_message + '\n'
                df['Importtimestamp'] = datetime.now()
                df["YearMonth"] = (df['Fiscal Year'].astype(int) * 100 + df['Period'].astype(int)).astype(str)
                # These 2 variable are set for the following action, after the match-case
                model = Ke30ImportLine
                field_mapping = import_dictionaries.ke30_mapping_dict
                list_of_sp =['_ke30_import', '_ke30_import_add_new_customers', '_ke30_import_add_new_products']
            case "ke24":
                convert_dict = import_dictionaries.ke24_converters_dict
                df = file.read_excel_file(file_path, convert_dict)
                df = df.drop(columns=['Industry Code 1'])
                # df['Industry Code 1'] = df['Industry Code 1'].astype(str)               
                model = Ke24ImportLine
                field_mapping = import_dictionaries.ke24_mapping_dict
            case "zaq":
                convert_dict = import_dictionaries.zaq_converters_dict
                df = file.read_excel_file(file_path, convert_dict)
                df["Billing date"] = df['Billing date'].apply(lambda x: x.strftime("%Y-%m-%d") if not pd.isna(x) else x)
                # This Excel file has the totals,at teh bottom, that must be removed
                # The number of rows may vary depending on the number of currencies and UoMs mentioned
                unique_uom = df['UoM'].nunique()
                unique_curr = df['Curr.'].nunique()
                rows_to_remove = max(unique_curr, unique_uom)
                df = df.head(len(df) - rows_to_remove) 
                model = ZACODMI9_import_line
                field_mapping = import_dictionaries.zaq_mapping_dict
            case "oo":
                convert_dict = import_dictionaries.oo_converters_dict
                df = file.read_excel_file(file_path, convert_dict)
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
            case "oi" | "arr":
                convert_dict = import_dictionaries.oo_converters_dict
                df = file.read_excel_file(file_path, convert_dict)
                # Removing bottom lines
                print(f"{file.file_type} was {len(df)} lines long")
                uniques = len(df['Document currency'].value_counts())
                df = df.iloc[:-uniques]
                print(f"{file.file_type} is now {len(df)} lines long")
                # Adjusting dates
                df['Document Date'] = df['Document Date'].dt.date
                df['Net due date'] = df['Net due date'].dt.date
                df['Payment date'] = df['Payment date'].dt.date
                df['Arrears after net due date'] = df['Arrears after net due date'].fillna(0).astype(int)
                if file.file_type == "arr":
                    model = Fbl5nArrImport
                    field_mapping = import_dictionaries.arr_mapping_dict
                if file.file_type == "oi":
                    model = Fbl5nOpenImport
                    field_mapping = import_dictionaries.oi_mapping_dict
            case "pr":
                convert_dict = import_dictionaries.pr_converters_dict
                df = file.read_excel_file(file_path)
                model = Price
                field_mapping = import_dictionaries.pr_mapping_dict
        model.objects.all().delete()
        log_message = "data:deleting rows from the db table\n\n"
        yield log_message
        log_text += log_message + '\n'
        df_length = len(df)
        df = df.replace(np.nan, '')
        chunk_size = 500
        chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        log_message = f"data:based on chunck_size, we got {len(chunks)} chunks for {df_length} total datframe rows\n\n"
        yield log_message
        log_text += log_message + '\n'
        chunk_counter = 0
        for chunk in chunks:
            chunk_counter += 1
            log_message = f"data:processing {chunk_counter}/{len(chunks)}\n\n"
            print(f"processing {chunk_counter}/{len(chunks)}")
            yield log_message
            log_text += log_message + '\n'
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
                    print(f'bulk_create for chunk {chunk_counter} done')
                    instances = []
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                log_message = f"data:working on chunk {chunk_counter} of {len(chunks)}  -  it took {elapsed_time} seconds\n\n"
                yield log_message
                log_text += log_message + '\n'
            except Exception as e:
                # Handle the exception
                log_message = f"data:An error occurred during the transaction: {e}\n\n"
                yield log_message
                log_text += log_message + '\n'
        # All chunks are processed
        print('all chunks processed')
        file.is_processed = True
        file.processed_at = datetime.now()
        # Woring on the stored procedures now
        if list_of_sp:
            print(f'There are {len(list_of_sp)} stored procedures')
            with connection.cursor() as curs:
                for index, sp in enumerate(list_of_sp):
                    print(f'sp{index}: {sp}')
                    sql_command = f'EXECUTE {sp}'
                    curs.execute(sql_command)
                    if curs.description:
                        resulting_rows = curs.fetchall()
                        print(f'resulting_rows from procedure: {len(resulting_rows)}')
                        print(resulting_rows)
                        result_text=''
                        for row in resulting_rows:
                            row_text = ', '.join(map(str, row))
                            result_text += row_text + "\n"
                            log_message = result_text
                            yield log_message
                            log_text += log_message + '\n'

            
        # Delete the file
        print(f'deleting ...{file.file_name}')
        if file.delete_file_soft():
            log_message = f"data:File {file.file_name} removed and db updated"
        else:
            log_message = f"data:There is a problem with file name {file.file_name}"
        yield log_message
        log_text += log_message + '\n'
        file.log = log_text
        file.save()
        log_message = f'data:process terminated for file id: {file.id}  filetye: {file.file_type} file_name: {file.file_name} file_path: {file.file_path}\n\n'
        yield log_message
        yield f'data:basta\n\n'


@login_required
def customers_list(request, page=0):
    search_term = request.GET.get('search')
    entries = request.GET.get('entries')
    view_entries = request.GET.get('radios_view')
    
    if 'new_customers' in request.GET:
        only_new_ustomers = request.GET.get('new_customers')
        if only_new_ustomers == 'on':
            only_new_ustomers = True
        else:
            only_new_ustomers = False
        customers = Customer.objects.filter(is_new = only_new_ustomers).order_by('name')
    else:
        only_new_ustomers = False
        customers = Customer.objects.all()

    if search_term:
        customers = customers.filter(
                models.Q(name__icontains=search_term) |
                models.Q(number__icontains=search_term) |
                models.Q(country__iso3166_1_alpha_2__icontains=search_term) |
                models.Q(country__official_name_en__icontains=search_term) |
                models.Q(sales_employee__first_name__icontains=search_term) |
                models.Q(sales_employee__last_name__icontains=search_term) |
                models.Q(customer_service_rep__last_name__icontains=search_term) |
                models.Q(customer_service_rep__first_name__icontains=search_term)
                ).order_by('name')
    else:
        customers = customers.order_by('-is_new','name')
    
    if view_entries is not None or view_entries != '':
        if view_entries == 'active':
            customers = customers.filter(active=True)
        elif view_entries == 'inactive':
            customers = customers.filter(active=False)
        else:
            customers = customers    

    if entries is not None:
        try:
            entries = int(entries)
        except ValueError:
            entries = 10
        items_per_page = entries
    else:
        items_per_page = 10

    paginator = Paginator(customers, items_per_page)
    # Get the current page from the GET request or in the URL
    if page != 0:
        page_number = page
    else:
        try:
            page_number = request.GET.get('page', 1)
        except (ValueError, TypeError):
            page_number = 1

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    filter_params = {
        'search_term': search_term,
        'entries': entries,
        'only_new': only_new_ustomers
    }

    context = {
        'page_object': page_obj,
        'filter_params': filter_params
    }
    return render(request, "app_pages/customers_list.html", context)


@login_required
def customer_view(request, pk):
    customer = Customer.objects.filter(id=pk).first()

    if request.method == "POST":
        operation = request.POST.get('operation')
        if operation == 'add':

            new_contact = Contact(
                customer = customer,
                first_name = request.POST.get('first_name',),
                middle_name = request.POST.get('middle_name', ''),
                last_name = request.POST.get('last_name', ''),
                job_position = request.POST.get('job_position', ''),
                mobile_number = request.POST.get('mobile_number', ''),
                email = request.POST.get('email', ''),
            )
            new_contact.save()
        elif operation == 'update':
            contact_id = request.POST.get('contact_id')
            contact = get_object_or_404(Contact, pk=contact_id, customer=customer)
            contact.first_name = request.POST.get('first_name')
            contact.middle_name = request.POST.get('middle_name')
            contact.last_name = request.POST.get('last_name')
            contact.job_position = request.POST.get('job_position')
            contact.mobile_number = request.POST.get('mobile_number')
            contact.email = request.POST.get('email')
            contact.save()
        return HttpResponseRedirect(request.path_info)

    # Get Contacts of this customer
    contacts = Contact.objects.filter(customer = customer)

    context = {
        'customer': customer,
        'contacts': contacts
    }
    return render(request, "app_pages/customer_view.html", context)


@login_required
def customer_edit(request, pk):
    c = get_object_or_404(Customer, id=pk)
    # Save is_new here to avoid overwriting when making form.is_valid()
    # for.is_valid would overwrite with False is is_new is not in the 
    # form template, or it is disabled
    is_new_value = c.is_new 
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance = c)
        if form.is_valid():
            print ("c.is_new", c.is_new)
            # Check if it's NEW
            if is_new_value:
                form.instance.approved_by = request.user
                form.instance.approved_on = datetime.today().date()
                form.instance.active = True
                form.instance.is_new = False
            form.save()
            return redirect('customer-view', pk=c.pk)
        else:
            print(form.errors)
    else:
        form = CustomerForm(instance=c)
        form.fields['is_new'].disabled = True
        form.fields['approved_by'].disabled = True
        form.fields['approved_on'].disabled = True
        print(c.import_note)
    context = {
        'form': form,
        'customer_is_new': c.is_new,
        'import_note': c.import_note
        }
    return render(request, "app_pages/customer_edit.html", context)


def get_contact_details(request, id):
    if request.method == 'GET':
        try:
            contact = Contact.objects.filter(pk=id).first()
            contact_data = {
                'id': contact.id,
                'first_name': contact.first_name,
                'middle_name': contact.middle_name,
                'last_name': contact.last_name,
                'job_position': contact.job_position,
                'mobile_number': contact.mobile_number,
                'email': contact.email,
            }
            return JsonResponse(contact_data)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Contact not found')


@login_required
def products_list(request, page=0):
    search_term = request.GET.get('search')
    entries = request.GET.get('entries') # how many rows to show
    category = request.GET.get('product_category')
    if category == '' or category == None: category = 'all'
    status = request.GET.get('product_status_selected')
    if status == '' or status == None: status = 'all'
    made_in = request.GET.get('made_in_country_selected')
    if made_in == '' or made_in == None: made_in = 'all'

    if search_term:
        products = Product.objects.filter(
                models.Q(name__icontains=search_term) |
                models.Q(number__icontains=search_term) |
                models.Q(brand__name__icontains=search_term) |
                models.Q(made_in__name__icontains=search_term)
                ).order_by('-number')
    else:
        products = Product.objects.all()
    
    if category is not None or category != '':
        if category == 'ink':
            products = products.filter(is_ink=True)
        elif category == 'non_ink':
            products = products.filter(is_ink=False)
        else:
            products = products.order_by('-number')

    products = products.order_by('-is_new', '-number')

    if status is not None and status != 'all':
        products = products.filter(product_status_id=status)


    if made_in is not None and made_in != 'all':
        products = products.filter(made_in=made_in)


    if entries is not None:
        try:
            entries = int(entries)
        except ValueError:
            entries = 10
        items_per_page = entries
    else:
        items_per_page = 10


    paginator = Paginator(products, items_per_page)
    # Get the current page from the GET request or in the URL
    if page != 0:
        page_number = page
    else:
        try:
            page_number = request.GET.get('page', 1)
        except (ValueError, TypeError):
            page_number = 1

    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)


    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)


    #Get all values of Product Status and Made In Countries
    product_statuses = ProductStatus.objects.all()
    made_in_countries = MadeIn.objects.all()


    filter_params = {
        'search_term': search_term,
        'entries': entries,
        'product_category': category, #ink/non-ink
        'product_status_selected': status,
        'made_in_country_selected': made_in,
    }

    context = {
        'page_object': page_obj,
        'product_statuses_all': product_statuses,
        'made_in_counties_all': made_in_countries,
        'filter_params': filter_params
    }
    return render(request, "app_pages/products_list.html", context)


@login_required
def product_view(request, pk):
    product = Product.objects.filter(id=pk).first()
    context = {
        'product': product
    }
    return render(request, "app_pages/product_view.html", context)

@login_required
def product_edit(request, pk):
    p = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance = p)
        if form.is_valid():
            form.save()
            return redirect('product-view', pk=p.pk)
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=p)
    context = {'form': form}
    return render(request, "app_pages/product_edit.html", context)


@login_required
def brands_list(request, page=0):
    search_term = request.GET.get('search')
    number_of_entries = request.GET.get('number_of_entries',12)
    selected_major_labels = request.GET.get('selected_major_labels')
    selected_ink_technologies = request.GET.getlist('selected_ink_technologies')

    if number_of_entries == '': number_of_entries = 12

    b = Brand.objects.all().order_by('name')

    if search_term:
        b = b.filter(
                models.Q(name__icontains=search_term) |
                models.Q(division__name__icontains=search_term) |
                models.Q(nsf_division__name__icontains=search_term) |
                models.Q(ink_technology__name__icontains=search_term) 
                ).order_by('name')
    else:
        b = b.order_by('name')

    if selected_ink_technologies:
         b = b.filter(ink_technology__name__in=selected_ink_technologies).distinct()

    if selected_major_labels:
        b = b.filter(major_label__name=selected_major_labels).distinct()

    if number_of_entries is not None:
        try:
            number_of_entries = int(number_of_entries)
        except ValueError:
            number_of_entries = 12
        items_per_page = number_of_entries

    paginator = Paginator(b, items_per_page)
     # Get the current page from the GET request or in the URL
    if page != 0:
        page_number = page
    else:
        try:
            page_number = request.GET.get('page', 1)
        except (ValueError, TypeError):
            page_number = 1
    
    try:
        page_obj = paginator.get_page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.get_page(1)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    ink_technologies = InkTechnology.objects.all()
    major_labels = MajorLabel.objects.all()

    print("selected_ink_technologies", selected_ink_technologies)
    print("selected_major_labels", selected_major_labels)

    filter_params = {
        'selected_ink_technologies': selected_ink_technologies,
        'selected_major_labels': selected_major_labels
    }

    context = {
        'page_object': page_obj,
        'brands': page_obj,
        'major_labels': major_labels,
        'ink_technologies': ink_technologies,
        'filter_params': filter_params
    }

    return render(request, "app_pages/brands_list.html", context)


@login_required
def brand_view(request, pk):
    b = Brand.objects.filter(id=pk).first()
    context = {
        'brand': b
    }
    return render(request, "app_pages/brand_view.html", context)


@login_required
def brand_edit(request, pk):
    b = get_object_or_404(Brand, id=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance = b)
        if form.is_valid():
            form.save()
            return redirect('brand-view', pk=b.pk)
        else:
            print(form.errors)
    else:
        form = BrandForm(instance=b)
    context = {'form': form}
    return render(request, "app_pages/brand_edit.html", context)


@login_required
def stored_procedures(request):
    procedures = StoredProcedure.objects.all()
    context = {'procedures': procedures}
    return render(request, "app_pages/stored_procedures.html", context)


@login_required
def stored_procedure(request, pk):
    procedure = get_object_or_404(StoredProcedure, id=pk)
    if request.method == 'POST':
        f = StoredProcedureForm(request.POST, instance=procedure)
        if f.is_valid():
            f.save()
            return redirect('stored-procedures')
        else:
            print(f.errors)
    else:
        form = StoredProcedureForm(instance=procedure)
    context = {'form': form}
    return render(request,"app_pages/stored_procedure.html", context)

@login_required
def stored_procedure_push(request, pk):
    pass

@login_required
def stored_procedure_execute(request, pk):
    pass


def edit_dictionary(request, dictionary_name):
    print(dictionary_name)
    dict_path = os.path.join(settings.MEDIA_ROOT, "dictionaries")
    path_dict_converting = f"{dict_path}/{dictionary_name}_converting.json"
    path_dict_renaming = f"{dict_path}/{dictionary_name}_renaming.json"

    if request.method == 'POST':
        if 'submit_button' in request.POST:
            button_value = request.POST['submit_button']
            if button_value == 'form_converting':
                data_converting = {}
                for key, value in request.POST.items():
                    if key.startswith('data_converting'):
                        key_name = key[len('data_converting['):-1]
                        data_converting[key_name] = value
                with open(path_dict_converting, 'w') as file_converting:
                    json.dump(data_converting, file_converting)

            if button_value == 'form_renaming':
                data_renaming = {}
                for key, value in request.POST.items():
                    if key.startswith('data_renaming'):
                        key_name = key[len('data_renaming['):-1]
                        data_renaming[key_name] = value
                with open(path_dict_renaming, 'w') as file_renaming:
                    json.dump(data_renaming, file_renaming)

    with open(path_dict_converting, 'r') as file_converting:
        data_converting = json.load(file_converting)

    with open(path_dict_renaming, 'r') as file_renaming:
        data_renaming = json.load(file_renaming)
    
    return render(request, "edit_dictionary.html", {'dictionary_name': dictionary_name, 'data_converting': data_converting, 'data_renaming': data_renaming})

def dictionary_add_key(request, dictionary_name):
    key_name = request.GET.get('key_name', '')
    if key_name:
        # Add the key to the dictionary and update the JSON file
        # You can use a similar approach as in the update_dictionary view
        return JsonResponse({'message': 'Key added successfully'})
    return JsonResponse({'message': 'Key not added'})

def dictionary_delete_key(request, dictionary_name):
    print('delete dictionary key on the dictionary: ', dictionary_name)
    key_name = request.GET.get('key_name', '')
    if key_name:
        # Add the key to the dictionary and update the JSON file
        # You can use a similar approach as in the update_dictionary view
        return JsonResponse({'message': 'Key deleted successfully'})
    return JsonResponse({'message': 'Key not deleted'})

@method_decorator(login_required, name='dispatch')
class BrandListView(ListView):
    model = Brand
    paginate_by = 24
    template_name = "brand_list.html"
    context_object_name = "brands"

@method_decorator(login_required, name='dispatch')
class BrandEditView(UpdateView):
    model = Brand
    form_class = EditBrandForm
    template_name = "brand_edit.html"
    success_url = "/brands/"

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', None)
        return get_object_or_404(Brand, id=id)

@method_decorator(login_required, name='dispatch')
class CustomerListView(ListView):
    model=Customer
    paginate_by=24
    template_name = "customer_list.html"
    context_object_name = "customers"

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('search')
        reset_pressed = 'reset' in self.request.GET
        if query and not reset_pressed:
            return Customer.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(number__icontains=query) |
                models.Q(country__iso3166_1_alpha_2__icontains=query) |
                models.Q(country__official_name_en__icontains=query) |
                models.Q(sales_employee__first_name__icontains=query) |
                models.Q(sales_employee__last_name__icontains=query)
                ).order_by('name')
        else:
            return Customer.objects.all().order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_pressed'] = 'reset' in self.request.GET
        return context

@method_decorator(login_required, name='dispatch')
class CustomerEditView(UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = "customer_edit.html"
    success_url = "/customers/"

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', None)
        return get_object_or_404(Customer, id=id)

@method_decorator(login_required, name='dispatch')
class ProductListView(ListView):
    model=Product
    paginate_by=24
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('search')
        queryset = Product.objects.all().order_by('name')
        reset_pressed = 'reset' in self.request.GET
        if query and not reset_pressed:
            queryset = Product.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(number__icontains=query) |
                models.Q(color__name__icontains=query) |
                models.Q(made_in__name__icontains=query) |
                models.Q(brand__name__icontains=query) |
                models.Q(packaging__name__icontains=query) |
                models.Q(product_line__name__icontains=query) |
                models.Q(product_status__name__icontains=query)
                ).order_by('name')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_pressed'] = 'reset' in self.request.GET
        return context

@method_decorator(login_required, name='dispatch')
class ProductEditView(UpdateView):
    model = Product
    form_class = EditProductForm
    template_name = "product_edit.html"
    success_url = "/products/"

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', None)
        return get_object_or_404(Product, id=id)

@method_decorator(login_required, name='dispatch')
class MajorLabelListView(ListView):
    model = MajorLabel
    paginate_by = 10
    template_name = "major_label_list.html"
    context_object_name = "major_labels"

@method_decorator(login_required, name='dispatch')
class MajorLabelEditView(UpdateView):
    model = MajorLabel
    form_class = EditMajorLabelForm
    template_name = "major_label_edit.html"
    success_url = "/major/"

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', None)
        return get_object_or_404(MajorLabel, id=id)

@method_decorator(login_required, name='dispatch')
class MajorLabelCreateView(CreateView):
    model = MajorLabel
    form_class = EditMajorLabelForm
    template_name = "major_label_create.html"
    success_url = "/major/"


def push_and_execute(request, pk):
    procedure = get_object_or_404(StoredProcedure, pk=pk)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM information_schema.routines WHERE routine_name = '{procedure.name}'")
        exists = cursor.fetchone()[0]
    
    if exists:
        # If it exists, drop the existing stored procedure
        with connection.cursor() as cursor:
            cursor.execute(f"DROP PROCEDURE {procedure.name}")
            
    with connection.cursor() as cursor:
        cursor.execute(procedure.script)
        cursor.execute(f"EXEC {cursor.name}")

    return redirect('procedure_list')
    

# For User Management
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or any other desired page after successful user creation
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authenticate/create_user.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        email = request.POST["login_email"]
        password = request.POST["login_password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You were successfully logged in'))
            # Check if there is a 'next' parameter in the URL
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            messages.success(request, ("There was an error loggin in ..."))
            return redirect('login')
    else:
        return render (request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('index')

class UserListView(ListView):
    model = User
    template_name = "list_users.html"
    context_object_name = "users"

class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('list_users')

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'app_pages/password-change.html'
  form_class = UserPasswordChangeForm


# Interface
def accordion(request):
    context = {
        'parent': 'interface',
        'segment': 'accordion',
    }
    return render(request, 'app_pages/accordion.html', context)

def blank_page(request):
    context = {
        'parent': 'interface',
        'segment': 'blank_page',
    }
    return render(request, 'app_pages/blank.html', context)

def badges(request):
    context = {
        'parent': 'interface',
        'segment': 'badges',
    }
    return render(request, 'app_pages/badges.html', context)

def buttons(request):
    context = {
        'parent': 'interface',
        'segment': 'buttons',
    }
    return render(request, 'app_pages/buttons.html', context)

# Cards
def sample_cards(request):
    context = {
        'parent': 'interface',
        'segment': 'sample_cards',
    }
    return render(request, 'app_pages/cards.html', context)

def card_actions(request):
    context = {
        'parent': 'interface',
        'segment': 'card_actions',
    }
    return render(request, 'app_pages/card-actions.html', context)

def cards_masonry(request):
    context = {
        'parent': 'interface',
        'segment': 'cards_masonry',
    }
    return render(request, 'app_pages/cards-masonry.html', context)

def colors(request):
    context = {
        'parent': 'interface',
        'segment': 'colors',
    }
    return render(request, 'app_pages/colors.html', context)

def data_grid(request):
    context = {
        'parent': 'interface',
        'segment': 'data_grid',
    }
    return render(request, 'app_pages/datagrid.html', context)

def datatables(request):
    context = {
        'parent': 'interface',
        'segment': 'datatables',
    }
    return render(request, 'app_pages/datatables.html', context)

def dropdowns(request):
    context = {
        'parent': 'interface',
        'segment': 'dropdowns',
    }
    return render(request, 'app_pages/dropdowns.html', context)

def modals(request):
    context = {
        'parent': 'interface',
        'segment': 'modals',
    }
    return render(request, 'app_pages/modals.html', context)

def maps(request):
    context = {
        'parent': 'interface',
        'segment': 'maps',
    }
    return render(request, 'app_pages/maps.html', context)

def map_fullsize(request):
    context = {
        'parent': 'interface',
        'segment': 'map_fullsize',
    }
    return render(request, 'app_pages/map-fullsize.html', context)

def vector_maps(request):
    context = {
        'parent': 'interface',
        'segment': 'vector_maps',
    }
    return render(request, 'app_pages/maps-vector.html', context)

def navigation(request):
    context = {
        'parent': 'interface',
        'segment': 'navigation',
    }
    return render(request, 'app_pages/navigation.html', context)

def charts(request):
    context = {
        'parent': 'interface',
        'segment': 'charts',
    }
    return render(request, 'app_pages/charts.html', context)

def pagination(request):
    context = {
        'parent': 'interface',
        'segment': 'pagination',
    }
    return render(request, 'app_pages/pagination.html', context)

def placeholder(request):
    context = {
        'parent': 'interface',
        'segment': 'placeholder',
    }
    return render(request, 'app_pages/placeholder.html', context)

def steps(request):
    context = {
        'parent': 'interface',
        'segment': 'steps',
    }
    return render(request, 'app_pages/steps.html', context)

def stars_rating(request):
    context = {
        'parent': 'interface',
        'segment': 'stars_rating',
    }
    return render(request, 'app_pages/stars-rating.html', context)

def tabs(request):
    context = {
        'parent': 'interface',
        'segment': 'tabs',
    }
    return render(request, 'app_pages/tabs.html', context)

def tables(request):
    context = {
        'parent': 'interface',
        'segment': 'tables',
    }
    return render(request, 'app_pages/tables.html', context)

def inxd_customers(request):
    customers = Customer.objects.all()
    context = {
        'parent': 'interface',
        'segment': 'inxd_customers',
        'customers': customers
    }
    return render(request, 'app_pages/inxd_customers.html', context)

def carousel(request):
    context = {
        'parent': 'interface',
        'segment': 'carousel',
    }
    return render(request, 'app_pages/carousel.html', context)

def lists(request):
    context = {
        'parent': 'interface',
        'segment': 'lists',
    }
    return render(request, 'app_pages/lists.html', context)

def typography(request):
    context = {
        'parent': 'interface',
        'segment': 'typography',
    }
    return render(request, 'app_pages/typography.html', context)

def offcanvas(request):
    context = {
        'parent': 'interface',
        'segment': 'offcanvas',
    }
    return render(request, 'app_pages/offcanvas.html', context)

def markdown(request):
    context = {
        'parent': 'interface',
        'segment': 'markdown',
    }
    return render(request, 'app_pages/markdown.html', context)

def dropzone(request):
    context = {
        'parent': 'interface',
        'segment': 'dropzone',
    }
    return render(request, 'app_pages/dropzone.html', context)

def lightbox(request):
    context = {
        'parent': 'interface',
        'segment': 'lightbox',
    }
    return render(request, 'app_pages/lightbox.html', context)

def tinymce(request):
    context = {
        'parent': 'interface',
        'segment': 'tinymce',
    }
    return render(request, 'app_pages/tinymce.html', context)

def inline_player(request):
    context = {
        'parent': 'interface',
        'segment': 'inline_player',
    }
    return render(request, 'app_pages/inline-player.html', context)


# Authentication
class RegistrationView(CreateView):
  template_name = 'app_pages/sign-up.html'
  form_class = RegistrationForm
  success_url = '/accounts/login/'

class LoginView(LoginView):
  template_name = 'app_pages/sign-in.html'
  form_class = LoginForm

class LoginViewIllustrator(LoginView):
  template_name = 'app_pages/sign-in-illustration.html'
  form_class = LoginForm

class LoginViewCover(LoginView):
  template_name = 'app_pages/sign-in-cover.html'
  form_class = LoginForm

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')

def login_link(request):
    return render(request, 'app_pages/sign-in-link.html')

class PasswordReset(PasswordResetView):
  template_name = 'app_pages/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'app_pages/password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'app_pages/password-change.html'
  form_class = UserPasswordChangeForm

def terms_service(request):
    return render(request, 'app_pages/terms-of-service.html')

def lock_screen(request):
    return render(request, 'app_pages/auth-lock.html')

# Error and maintenance
def error_404(request):
    return render(request, 'app_pages/error-404.html')

def error_500(request):
    return render(request, 'app_pages/error-500.html')

def maintenance(request):
    return render(request, 'app_pages/error-maintenance.html')


def form_elements(request):
    context = {
        'parent': '',
        'segment': 'form_elements',
    }
    return render(request, 'app_pages/form-elements.html', context)

# Extra
def empty_page(request):
    context = {
        'parent': 'extra',
        'segment': 'empty_page',
    }
    return render(request, 'app_pages/empty.html', context)

def cookie_banner(request):
    context = {
        'parent': 'extra',
        'segment': 'cookie_banner',
    }
    return render(request, 'app_pages/cookie-banner.html', context)

def activity(request):
    context = {
        'parent': 'extra',
        'segment': 'activity',
    }
    return render(request, 'app_pages/activity.html', context)

def gallery(request):
    context = {
        'parent': 'extra',
        'segment': 'gallery',
    }
    return render(request, 'app_pages/gallery.html', context)

def invoice(request):
    context = {
        'parent': 'extra',
        'segment': 'invoice',
    }
    return render(request, 'app_pages/invoice.html', context)

def search_results(request):
    context = {
        'parent': 'extra',
        'segment': 'search_results',
    }
    return render(request, 'app_pages/search-results.html', context)

def pricing_cards(request):
    context = {
        'parent': 'extra',
        'segment': 'pricing_cards',
    }
    return render(request, 'app_pages/pricing.html', context)

def pricing_table(request):
    context = {
        'parent': 'extra',
        'segment': 'pricing_table',
    }
    return render(request, 'app_pages/pricing-table.html', context)

def faq(request):
    context = {
        'parent': 'extra',
        'segment': 'faq',
    }
    return render(request, 'app_pages/faq.html', context)

def users(request):
    context = {
        'parent': 'extra',
        'segment': 'users',
    }
    return render(request, 'app_pages/users.html', context)

def license(request):
    context = {
        'parent': 'extra',
        'segment': 'license',
    }
    return render(request, 'app_pages/license.html', context)

def logs(request):
    context = {
        'parent': 'extra',
        'segment': 'logs',
    }
    return render(request, 'app_pages/logs.html', context)

def music(request):
    context = {
        'parent': 'extra',
        'segment': 'music',
    }
    return render(request, 'app_pages/music.html', context)

def photogrid(request):
    context = {
        'parent': 'extra',
        'segment': 'photogrid',
    }
    return render(request, 'app_pages/photogrid.html', context)

def tasks(request):
    context = {
        'parent': 'extra',
        'segment': 'tasks',
    }
    return render(request, 'app_pages/tasks.html', context)

def uptime(request):
    context = {
        'parent': 'extra',
        'segment': 'uptime',
    }
    return render(request, 'app_pages/uptime.html', context)

def widgets(request):
    context = {
        'parent': 'extra',
        'segment': 'widgets',
    }
    return render(request, 'app_pages/widgets.html', context)

def wizard(request):
    context = {
        'parent': 'extra',
        'segment': 'widgets',
    }
    return render(request, 'app_pages/wizard.html', context)

def app_settings(request):
    context = {
        'parent': 'extra',
        'segment': 'settings',
    }
    return render(request, 'app_pages/settings.html', context)

def settings_plan(request):
    context = {
        'parent': 'extra',
        'segment': 'settings',
    }
    return render(request, 'app_pages/settings-plan.html', context)

def trial_ended(request):
    context = {
        'parent': 'extra',
        'segment': 'trial_ended',
    }
    return render(request, 'app_pages/trial-ended.html', context)

def job_listing(request):
    context = {
        'parent': 'extra',
        'segment': 'job_listing',
    }
    return render(request, 'app_pages/job-listing.html', context)

def page_loader(request):
    context = {
        'parent': 'extra',
        'segment': 'page_loader',
    }
    return render(request, 'app_pages/page-loader.html', context)

# Layout
def layout_horizontal(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_horizontal',
    }
    return render(request, 'app_pages/layout-horizontal.html', context)

def layout_boxed(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_boxed',
    }
    return render(request, 'app_pages/layout-boxed.html', context)

def layout_vertical(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_vertical',
    }
    return render(request, 'app_pages/layout-vertical.html', context)

def layout_vertical_transparent(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_vertical_transparent',
    }
    return render(request, 'app_pages/layout-vertical-transparent.html', context)

def layout_vertical_right(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_vertical_right',
    }
    return render(request, 'app_pages/layout-vertical-right.html', context)

def layout_condensed(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_condensed',
    }
    return render(request, 'app_pages/layout-condensed.html', context)

def layout_combined(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_combined',
    }
    return render(request, 'app_pages/layout-combo.html', context)

def layout_navbar_dark(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_navbar_dark',
    }
    return render(request, 'app_pages/layout-navbar-dark.html', context)

def layout_navbar_sticky(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_navbar_sticky',
    }
    return render(request, 'app_pages/layout-navbar-sticky.html', context)

def layout_navbar_overlap(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_navbar_overlap',
    }
    return render(request, 'app_pages/layout-navbar-overlap.html', context)

def layout_rtl(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_rtl',
    }
    return render(request, 'app_pages/layout-rtl.html', context)

def layout_fluid(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_fluid',
    }
    return render(request, 'app_pages/layout-fluid.html', context)

def layout_fluid_vertical(request):
    context = {
        'parent': 'layout',
        'segment': 'layout_fluid_vertical',
    }
    return render(request, 'app_pages/layout-fluid-vertical.html', context)

def changelog(request):
    return render(request, 'app_pages/changelog.html')

def profile(request):
    return render(request, 'app_pages/profile.html')

def icons(request):

    context = {
        'parent': '',
        'segment': 'icons',
    }
    return render(request, 'app_pages/icons.html', context)

def edit_model_record(request, pk, model):
    model_class = apps.get_model(app_label='inx_platform_app', model_name=model)
    instance = get_object_or_404(model_class, pk=pk)
    generic_model_form = get_generic_model_form(model_class)
    if request.method == 'POST':
        form = generic_model_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            # Generate the URL dynamically using reverse()
            redirect_url = reverse(f'{model.lower()}-view', args=[pk])
            # Redirect the user to the generated URL
            return redirect(redirect_url)
    else:
        form = generic_model_form(instance=instance)
    context = {
        'model_name': model,
        'form': form
        }
    return render(request, 'app_pages/edit_generic_model.html', context)


def sse(request):
    return render(request, "app_pages/sse.html", {})


async def sse_stream(request):
    '''
    Sends SSEs to the client
    '''
    async def stream_the_event():
        counter = 0
        while counter <= 10:
            message = message = f"data: {str(uuid.uuid4())}  -  {counter}\n\n"
            yield message
            await asyncio.sleep(0.3)
            counter += 1

    return StreamingHttpResponse(stream_the_event(), content_type='text/event-stream')

        

