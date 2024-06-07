-- Add calculated columns for 'day' and 'hour'
IROCCV_T25_Bridge_Dataset[day] = FORMAT(IROCCV_T25_Bridge_Dataset[frame_ts], "yyyy-MM-dd")
IROCCV_T25_Bridge_Dataset[hour] = HOUR(IROCCV_T25_Bridge_Dataset[frame_ts])

-- Add a calculated column for cleaned 'split_name'
IROCCV_T25_Bridge_Dataset[split_name_clean] = LOWER(TRIM(IROCCV_T25_Bridge_Dataset[split_name]))

-- Group by 'day' and 'hour' and count frames
GroupedData = 
SUMMARIZE(
    IROCCV_T25_Bridge_Dataset,
    IROCCV_T25_Bridge_Dataset[day],
    IROCCV_T25_Bridge_Dataset[hour],
    "FrameCount", COUNT(IROCCV_T25_Bridge_Dataset[frame_ts])
)


-- Measure to count frames for a specific day
FrameCount = COUNT(IROCCV_T25_Bridge_Dataset[frame_ts])

-- Measures to count frames for each specific day
-- Example for a specific day, repeat for each day you need
FrameCount_2023_01_01 = CALCULATE([FrameCount], IROCCV_T25_Bridge_Dataset[day] = "2023-01-01")

-- Pivot table visual can be created in Power BI using these measures

-- Group by 'hour' and count frames
FrameCountsPerHour = 
SUMMARIZE(
    IROCCV_T25_Bridge_Dataset,
    IROCCV_T25_Bridge_Dataset[hour],
    "FrameCount", COUNT(IROCCV_T25_Bridge_Dataset[frame_ts])
)

-- Create a filtered table for bridged data
BridgedData = 
FILTER(
    IROCCV_T25_Bridge_Dataset,
    IROCCV_T25_Bridge_Dataset[bridged] = TRUE()
)

-- Group by 'hour' and count bridged frames
BridgedFrameCountsPerHour = 
SUMMARIZE(
    BridgedData,
    BridgedData[hour],
    "BridgedCount", COUNT(BridgedData[frame_ts])
)

-- Group by 'hour' and 'camera_name' and count usage
CameraHourlyCounts = 
SUMMARIZE(
    IROCCV_T25_Bridge_Dataset,
    IROCCV_T25_Bridge_Dataset[hour],
    IROCCV_T25_Bridge_Dataset[camera_name],
    "UsageCount", COUNT(IROCCV_T25_Bridge_Dataset[frame_ts])
)

-- Create a matrix visual in Power BI to display the counts


































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
