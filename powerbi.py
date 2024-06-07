import pandas as pd

# Define chunk size
chunksize = 1000000  # Set your desired chunk size

# Load data in chunks
chunks = []
for i in range(0, len(dataset), chunksize):
    chunk = dataset[i:i+chunksize]
    print(chunk)
    chunks.append(chunk)

data = pd.concat(chunks, ignore_index=True)

# Concatenate chunks into a single DataFrame
data = pd.concat(chunks, ignore_index=True)

# Convert 'frame_ts' to datetime
data['frame_ts'] = pd.to_datetime(data['frame_ts'], unit='ms')

# Extract 'day' and 'hour' from 'frame_ts'
data['day'] = data['frame_ts'].dt.date
data['hour'] = data['frame_ts'].dt.hour
data['hour_group'] = data['frame_ts'].dt.hour

# Clean 'split_name'
data['split_name'] = data['split_name'].str.strip().str.lower()

# Group by 'day' and 'hour' and count frames
grouped_data = data.groupby(['day', 'hour']).size().reset_index(name='frame_count')

# Pivot data
pivot_data = grouped_data.pivot(index='hour', columns='day', values='frame_count').fillna(0)

# Count frames per hour
frame_counts = data.groupby('hour_group').size().reset_index(name='frame_count')

# Filter bridged data
bridged_data = data[data['bridged'] == True]

# Count bridged frames per hour
bridged_hourly_counts = bridged_data.groupby('hour_group').size().reset_index(name='bridged_count')

# Count camera usage per hour
camera_hourly_counts = data.groupby(['hour_group', 'camera_name']).size().unstack(fill_value=0)
camera_hourly_counts.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='tab20')
camera_usage = camera_hourly_counts.reset_index()
