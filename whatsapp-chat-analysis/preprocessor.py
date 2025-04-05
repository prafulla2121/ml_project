import re
import pandas as pd

def preprocess(data):
    # Improved regex pattern to match WhatsApp messages properly
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}) - (.+)'

    # Extract messages along with timestamps
    matches = re.findall(pattern, data)

    # Ensure lists have equal lengths
    extracted_dates = [match[0] + ", " + match[1] for match in matches]
    messages = [match[2] for match in matches]

    # Creating a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': extracted_dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'].str.strip(), format='%d/%m/%y, %H:%M', errors='coerce')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract user and message content
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 1:  # If user name exists
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional time-based features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create time periods for analysis
    period = []
    for hour in df['hour']:
        if pd.isna(hour):  # Handle NaT values
            period.append(None)
        elif hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour + 1}")

    df['period'] = period

    return df
