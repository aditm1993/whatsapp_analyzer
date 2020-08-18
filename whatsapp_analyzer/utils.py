import pandas as pd
from django.conf import settings
from pandarallel import pandarallel


def analyse_data(keywords):
    pandarallel.initialize()

    table1 = settings.TABLE1
    table2 = settings.TABLE2

    # count the keywords in all messages
    table1['count'] = table1['text'].parallel_apply(
        lambda text: any(word in text for word in keywords)
    )

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
        filtered_table, table2, left_on='group_id', right_on='group_id'
    ).to_dict('records')
    data_dict.sort(key=lambda x: x['count'], reverse=True)
    return data_dict
