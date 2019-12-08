#%%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime

    
def read_issuetrackerdb(table_name):
    try:
        connection = mysql.connector.connect(host='issuetrackerdb.cv2cs77f45ul.ap-northeast-2.rds.amazonaws.com',
                                            database='Practice',
                                            user='admin',
                                            password='passadmin')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"desc {table_name}")
            res = cursor.fetchall()
            res_columns = pd.DataFrame(res)
            res_columns_list = res_columns.iloc[:,0].tolist()
            
            query=f'''
            Select * from {table_name}
            '''
            cursor.execute(query)
            res_list = cursor.fetchall()
            res_pd = pd.DataFrame(res_list, columns = res_columns_list)
            connection.commit()
            cursor.close()
            connection.close()
            return res_pd

    except Error as e:
        print("Error while connecting to MySQL: ", e)


#%%
def table_plot(image_file_name, table_name):
    data_df = read_issuetrackerdb(table_name)
    df_person = data_df[data_df['inv_name']=='개인']
    df_foreign = data_df[data_df['inv_name']=='외국인']

    df_person_qnet_buy = df_person['qnet_buy'].to_numpy()
    df_person_pnet_buy = df_person['pnet_buy'].to_numpy()/pow(10,9)
    df_foreign_qnet_buy = df_foreign['qnet_buy'].to_numpy()
    df_foreign_pnet_buy = df_foreign['pnet_buy'].to_numpy()/pow(10,9)
    price = df_person['closeprice'].to_numpy()/pow(10,3)
    dates = df_person['date'].to_numpy()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.set_size_inches(10,7)
    ax1.plot(dates, df_person_qnet_buy, 'o:')
    ax1.plot(dates, df_foreign_qnet_buy, '*-')
    ax2.plot(dates, df_person_pnet_buy, 'o:')
    ax2.plot(dates, df_foreign_pnet_buy, '*-')
    ax3.plot(dates, price, '^-')
    ax1.set(ylabel='quantity', 
           title='Net Purchase in Quantiy')
    ax2.set(ylabel='KRW', 
           title='Net Purchase in Price (1B KRW)')
    timestamp = 'Closing Price (1K KRW) ' + str(datetime.now())
    ax3.set(xlabel='date', ylabel='KRW',
           title=timestamp)
       
    ax3.grid()
    print(price)

    fig.savefig(image_file_name)
    #fig.savefig("../static/data_imgs/"+image_file_name)
    # plt.show()
