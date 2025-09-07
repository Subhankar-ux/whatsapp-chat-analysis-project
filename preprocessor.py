import re
import pandas as pd
def preprocess(data):
    pattern=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    messages=re.split(pattern,data)
    dates = re.findall(pattern,data)
    
    df=pd.DataFrame({'user_message':messages[1:],'message_date':dates})
    #convert messages_data type
    df['message_date']=df['message_date'].str.replace("\u202f", " ",regex=False).str.replace(" -","",regex=False)
    df['message_date']=pd.to_datetime(df['message_date'],errors='coerce',infer_datetime_format=True)
    df.rename(columns={'message_date':'date_time'},inplace=True)
    
    #seperate users and messages
    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1: ]:
           users.append(entry[1])
           messages.append(entry[2])
        else:
          users.append('group_notification')
          messages.append(entry[0])
    df['user']=users
    df['messages']=messages
    df.drop(columns=['user_message'],inplace=True)
    
    df['year']=df['date_time'].dt.year
    df['month_num']=df['date_time'].dt.month
    df['only_date']=df['date_time'].dt.date
    df['month']=df['date_time'].dt.month_name()
    df['day_name']=df['date_time'].dt.day_name()
    df['day']=df['date_time'].dt.day
    df['hour']=df['date_time'].dt.hour
    df['minute']=df['date_time'].dt.minute
    
    return df