import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt

# Step 1: Load CSV data from SharePoint URL
url = "https://spo.titan.com/sites/TechIROCCV/Shared%20Documents/General/PowerBI/iroccv_t25_bridge_dataset.csv"
response = requests.get(url)
data = pd.read_csv(StringIO(response.text), delimiter=",", encoding='cp1252')

# Step 2: Parse and transform datetime column
data['frame_ts'] = pd.to_datetime(data['frame_ts'], unit='ms')
data['day'] = data['frame_ts'].dt.date
data['hour'] = data['frame_ts'].dt.hour

# Step 3: Group and pivot data
grouped_data = data.groupby(['day', 'hour']).size().reset_index(name='frame_count')
pivot_data = grouped_data.pivot(index='hour', columns='day', values='frame_count').fillna(0)

# Step 4: Process bridged data
bridged_data = data[data['bridged'] == True]
bridged_hourly_counts = bridged_data.groupby('hour').size().reset_index(name='bridged_count')

# Step 5: Process camera hourly counts and plot
camera_hourly_counts = data.groupby(['hour', 'camera_name']).size().unstack(fill_value=0)
camera_hourly_counts.plot(kind='bar', stacked=True, colormap='tab20', figsize=(12, 8))
plt.title('Camera Usage by Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Frame Count')
plt.legend(title='Camera Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Step 6: Reset index for camera usage
camera_usage = camera_hourly_counts.reset_index()

# Display the first few rows of the processed data (optional)
print(camera_usage.head())
