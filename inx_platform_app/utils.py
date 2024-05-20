import os, sys
from django.db import connection
import json
from django.core.cache import cache
from .models import CountryCode

def check_and_create_views_and_procs(app_folder):
    table_names = connection.introspection.table_names()
    if 'inx_platform_app_product' in table_names and 'inx_platform_app_customer' in table_names:
        # Check for views
        print("*"*50)
        print("* VIEWS", end="")
        print(" "*41, "*")
        print("*"*50)
        view_folder = os.path.join(app_folder, 'database_scripts/views')
        view_files = sorted([f[:-4] for f in os.listdir(view_folder) if f.endswith('.sql')])
        print(f"view_files:{view_files}")
        with connection.cursor() as cursor:
            for view_name in view_files:
                sql_statement = f"SELECT * FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME = '{view_name}'"
                # print(f"sql_statement: {sql_statement}")
                try:
                    cursor.execute(sql_statement)
                except Exception as e:
                    print("Error executing SQL statement:", e)
                    sys.exit(1)
                if not cursor.fetchone():
                    print(f"there is not {view_name}", end = "")
                    with open(os.path.join(view_folder, f"{view_name}.sql")) as f:
                        view_sql = f.read()
                    try:
                        cursor.execute(view_sql)
                    except Exception as e:
                        print("Error executing SQL statement:", e)
                        sys.exit(1)
                    # cursor.execute(view_sql)
                    print(f" -> {view_name} CREATED in the db")
                else:
                    print(f"{view_name} exists")
                    pass
        print()

        # Check for stored procedures
        print("*"*50)
        print("* PROCS", end="")
        print(" "*41, "*")
        print("*"*50)
        proc_folder = os.path.join(app_folder, 'database_scripts/stored_procedures')
        proc_files = [f[:-4] for f in os.listdir(proc_folder) if f.endswith('.sql')]
        print(proc_files)
        with connection.cursor() as cursor:
            for proc_name in proc_files:
                sql_statement = f"SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[{proc_name}]') AND type in (N'P', N'PC')"
                try:
                    # print(sql_statement)
                    cursor.execute(sql_statement)
                except Exception as e:
                    print("Error executing SQL statement:", e)
                    sys.exit(2)
                # cursor.execute(sql_statement)
                if not cursor.fetchone():
                    print(f"there is not {proc_name}", end = "")
                    with open(os.path.join(proc_folder, f"{proc_name}.sql")) as f:
                        proc_sql = f.read()
                        try:
                            cursor.execute(proc_sql)
                        except Exception as e:
                            print("Error executing SQL statement:", e)
                            sys.exit(1)
                        print(f" -> {proc_name} CREATED in the db")
                else:
                    print(f"{proc_name} exists")
        print()

def get_cache_country_codes():
    country_codes = cache.get('country_codes')
    if not country_codes:
        country_codes = list(CountryCode.objects.values('alpha_2', 'official_name_en').order_by('official_name_en'))
        country_codes.insert(0, {'alpha_2': '00', 'official_name_en': 'All'})
        cache.set('country_codes', json.dumps(country_codes), timeout=172800) # cahche 48 hours
    else:
        country_codes = json.loads(country_codes)
    return country_codes