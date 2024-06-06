data = Csv.Document(Web.Contents("https://spo.bhpbilliton.com/sites/TechIROCCV/Shared%20Documents/General/PowerBI/iroccv_t25_bridge_dataset.csv"),[Delimiter=",", Columns=21, Encoding=1252, QuoteStyle=QuoteStyle.None])
data['frame_ts'] = pd.to_datetime(data['frame_ts'], unit='ms')
data['day'] = data['frame_ts'].dt.date
data['hour'] = data['frame_ts'].dt.hour
data['hour_group'] = data['frame_ts'].dt.hour
grouped_data = data.groupby(['day', 'hour']).size().reset_index(name='frame_count')
pivot_data = grouped_data.pivot(index='hour', columns='day', values='frame_count').fillna(0)
bridged_data = data[data['bridged'] == True]
bridged_hourly_counts = bridged_data.groupby('hour_group').size().reset_index(name='bridged_count')
camera_hourly_counts = data.groupby(['hour_group', 'camera_name']).size().unstack(fill_value=0)
camera_hourly_counts.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='tab20')
camera_usage = camera_hourly_counts.reset_index()
