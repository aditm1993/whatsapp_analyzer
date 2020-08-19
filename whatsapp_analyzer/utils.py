import time

import pandas as pd
from django.conf import settings
import psycopg2


def analyse_data(keywords):
    if len(keywords) == 0:
        return []
    elif len(keywords) == 1:
        query_str = f"textlower like '%{keywords[0]}%'"
    else:
        query_str = ' or '.join([f"textlower like '%{kw}%'" for kw in keywords])
    COMMAND = f"""
    select groupid, count(*)
    from "bd_cs_prod_conversations"
    where ({query_str})
      and (createdatutc > current_timestamp -5)
      and (type in ('Comment', 'Post'))
    group by groupid
    """
    print(COMMAND)

    start_time = time.time()
    try:
        with psycopg2.connect(
                dbname='datawarehousedev',
                host='datawarehousedev.cjvot3egkzt4.us-east-1.redshift.amazonaws.com',
                port='5439',
                user='dataanalyst',
                password='DataAnalyst@1234$') as database:
            with database.cursor() as cursor:
                cursor.execute(COMMAND)
                table1 = pd.DataFrame(cursor.fetchall(), columns=('group_id', 'count'))
        print(f'received response in {time.time() - start_time} secs')
        print(table1)

        # fill NaN values with 0
        table1.fillna(0, inplace=True)

        # filter table1 using keywords
        filtered_table = pd.DataFrame(
            table1.groupby(['group_id'], sort=False)['count'].apply(
                lambda x: x.astype(int).sum())
        )

        # remove rows which have count=0
        filtered_table = filtered_table[filtered_table['count'] != 0]

        # merge with table2 and return as a dict
        data_dict = pd.merge(
            filtered_table, settings.TABLE2, left_on='group_id', right_on='group_id'
        ).to_dict('records')
        data_dict.sort(key=lambda x: x['count'], reverse=True)
        return data_dict
    except:
        return []
