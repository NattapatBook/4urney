from datetime import datetime

import pandas as pd
import psycopg2
from tqdm.auto import tqdm


def connect_to_db(params):
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(**params)

def load_data(connection, query):
    """Load data from a database query into a pandas DataFrame."""
    return pd.read_sql_query(query, connection)

def preprocess_data(df_msgs, df_sums, summary_col='lastest_msg_date'):
    """Process and prepare the data for analysis."""
    df_msgs['timestamp'] = df_msgs['timestamp'].dt.tz_convert('Asia/Bangkok').dt.tz_localize(None)
    
    if summary_col in df_sums.columns:
        try:
            df_sums[summary_col] = df_sums[summary_col].dt.tz_localize(None)
        except:
            pass
    
    latest_per_group = df_msgs.loc[df_msgs.groupby('platform_id')['timestamp'].idxmax()]
    diff_records = pd.concat([
        df_sums[['platform_id', summary_col]].reset_index(drop=True).rename(
            columns={
                'platform_id': 'platform_id',
                summary_col: 'timestamp'
            }
        ),
        latest_per_group[['platform_id', 'timestamp']].reset_index(drop=True)
    ]).drop_duplicates(keep=False)

    focus_user_ids = diff_records['platform_id'].unique()
    df_msgs['whose_msg'] = df_msgs['by'] + ': ' + df_msgs['message']
    grouped = df_msgs.groupby('platform_id')

    return focus_user_ids, grouped

def summarize_conversation(all_msgs, llms):
    """สรุปบทสนทนาให้ในภาษาไทย"""
    response = llms.invoke(f"""
        กรุณาสรุปความต้องการหลักของลูกค้าจากบทสนทนา โดยเน้นเฉพาะประเด็นสำคัญและเข้าใจง่ายที่สุด สรุปในรูปแบบข้อความ (bullet points) จะดีที่สุด
        บทสนทนา: {all_msgs}
        สรุป:
    """)
    return response.content

def score_satisfaction(all_msgs, llms):
    """Evaluate customer satisfaction based on the conversation."""
    response = llms.invoke(f"""
        You are tasked with analyzing a conversation between a customer and a bot to determine the satisfaction level of the customer. Provide a satisfaction score between 0 and 100 based on the conversation:
        ---
        Conversation: {all_msgs}
        ---
        Suggested Satisfaction Score:
    """)
    return int(response.content)

def score_urgency(all_msgs, llms):
    """Evaluate customer urgency based on the conversation."""
    response = llms.invoke(f"""
        You are tasked with analyzing a conversation between a customer and a bot to determine the urgency level of the customer. 
        Please follow these steps:
        
        1. Review the entire conversation for satisfaction indicators such as tone, requests, and frustrations.
        2. Assess how well the bot resolved the customer's issue, considering politeness, clarity, and helpfulness.
        3. Identify dissatisfaction signals such as frustration or confusion.

        Provide an urgency score between 0 and 100, where:
        - 0 indicates completely non-urgent.
        - 100 indicates extremely urgent.

        ---
        Conversation: {all_msgs}
        ---
        Suggested Urgency Score:
    """)
    return int(response.content.strip())


def upsert_data(user_id, result, latest_msg_date, connection, table_name, column_name):
    """Upsert data into the database."""
    data_to_upsert = {
        "user_id": user_id,
        column_name: result,
        "lastest_msg_date": latest_msg_date,
        "generated_date": datetime.now()
    }
    cursor = connection.cursor()

    upsert_query = f"""
    INSERT INTO "4urney".{table_name} (user_id, {column_name}, lastest_msg_date, generated_date)
    VALUES (%(user_id)s, %({column_name})s, %(lastest_msg_date)s, %(generated_date)s)
    ON CONFLICT (user_id)
    DO UPDATE SET
        {column_name} = EXCLUDED.{column_name},
        lastest_msg_date = EXCLUDED.lastest_msg_date,
        generated_date = EXCLUDED.generated_date;
    """

    cursor.execute(upsert_query, data_to_upsert)
    connection.commit()

def process_task(focus_user_ids, grouped, llms, task_fn, table_name, column_name):
    """Process conversations and update results in the database."""
    print(f'Updating {len(focus_user_ids)} records')
    for group in tqdm(grouped):
        user_id = group[0]
        if user_id in focus_user_ids:
            try:
                all_msgs = group[1]['whose_msg'].values[-20:]
                result = task_fn(all_msgs, llms)
                latest_msg_date = group[1]['timestamp'].max()
                # upsert_data(user_id, result, latest_msg_date, connection, table_name, column_name)
                return dict(
                    user_id=user_id,
                    result=result,
                    lastest_msg_date=latest_msg_date,
                    table_name=table_name,
                    column_name=column_name,
                )
            except Exception as e:
                print(f"An error occurred for user_id {user_id}: {e}")
                latest_msg_date = group[1]['timestamp'].max()
                return dict(
                    user_id=user_id,
                    result=None,
                    lastest_msg_date=latest_msg_date,
                    table_name=table_name,
                    column_name=column_name,
                )