import os
import psycopg2 
import psycopg2.extras as extras 
import pandas.io.sql as sqlio

DB_CONFIG = {
    'host': os.environ.get('DEMO_DATABASE_HOST'),
    'database': os.environ.get('DEMO_DATABASE_NAME'),
    'user': os.environ.get('DEMO_DATABASE_USER'),
    'password': os.environ.get('DEMO_DATABASE_PASSWORD'),
    'port': os.environ.get('DEMO_DATABASE_PORT'),
}

conn = psycopg2.connect(**DB_CONFIG)

def execute_script(script): 
    try: 
        cursor = conn.cursor() 
    except: 
        conn = psycopg2.connect(**DB_CONFIG)

        cursor = conn.cursor() 
        
    cursor.execute(script) 
    
    conn.commit() 
    conn.close() 
    
    
def execute_to_df(script):
        
    df = sqlio.read_sql_query(script, conn)

    return df


def execute_values(conn, df, schema, table): 
  
    tuples = [tuple(x) for x in df.to_numpy()] 

    cols = ','.join(list(df.columns)) 
    # SQL query to execute 
    query = """INSERT INTO "%s".%s(%s) VALUES %%s""" % (schema, table, cols) 

    cursor = conn.cursor() 
    try: 
        extras.execute_values(cursor, query, tuples) 
        conn.commit() 
    except (Exception, psycopg2.DatabaseError) as error: 
        print("Error: %s" % error) 
        conn.rollback() 
        cursor.close() 
        return 1
    print("the dataframe is inserted") 
    cursor.close() 