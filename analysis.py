import pandas as pd
import datetime

pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", None)  # No line wrapping
pd.set_option("display.colheader_justify", "center")  # Center column names

def str_to_datetime(string:str)->datetime.datetime:
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f")

def pre_treatment(data:pd.DataFrame)->pd.DataFrame:
    data['send_time'] = list(map(str_to_datetime, data['send_time'].to_list()))
    data['received_time'] = list(map(str_to_datetime, data['received_time'].to_list()))
    data['# of message'] = list(map(int, data['# of message'].to_list()))
    return data

def subtract_datetimes_in_total_seconds(datetime_tuple)->float:
    return float((datetime_tuple[1] - datetime_tuple[0]).total_seconds())

def calculate_out_of_order_messages(data:pd.DataFrame):
    length = len(data)
    out_of_order_df = pd.DataFrame()
    for i in range(length):
        ith_message = data['# of message'][i]
        ith_message_receive_time = data['received_time'][i]

        df_temp = data[(data['# of message'] < ith_message) & (data['received_time'] > ith_message_receive_time)]
        df_temp['out of order message'] = data['# of message'][i]
        df_temp['out of order message receiving time'] = ith_message_receive_time
        out_of_order_df = pd.concat([out_of_order_df, df_temp])
    out_of_order_df = out_of_order_df.reset_index(drop=True)
    out_of_order_df.to_csv('zenoh_out_of_order_messages.csv', index=False, float_format='%.8f')

def calculate_time_to_receive()->pd.DataFrame:
    data = pre_treatment(pd.read_csv('zenoh-csvs/thread1.csv'))
    time_to_receive = list(map(subtract_datetimes_in_total_seconds,
                               zip(data['send_time'].to_list(),
                                   data['received_time'].to_list())))

    data['time_to_receive'] = time_to_receive
    data.to_csv('zenoh_time_to_receive.csv', index=False, float_format='%.8f')
    return data

if __name__ == '__main__':
    df = calculate_time_to_receive()
    calculate_out_of_order_messages(df)
