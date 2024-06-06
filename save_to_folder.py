import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
from io import StringIO

# Define your SharePoint site URL and credentials
site_url = "https://your_sharepoint_site_url"
client_id = "your_client_id"
client_secret = "your_client_secret"

# Authenticate with SharePoint
ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

# Define the function to upload the DataFrame in batches
def upload_csv_in_batches(ctx, df, target_folder_url, target_file_name, batch_size):
    # Convert the DataFrame headers to a CSV string and upload the initial file
    csv_buffer = StringIO()
    df.head(0).to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    # Create the file in SharePoint
    target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
    target_folder.upload_file(target_file_name, csv_data).execute_query()
    
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]
        csv_buffer = StringIO()
        batch_df.to_csv(csv_buffer, header=False, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Append the batch to the file
        target_file = target_folder.files.get_by_url(target_file_name)
        target_file.write(csv_data, True).execute_query()
        print(f"Batch {i // batch_size + 1} uploaded")

# Create a sample DataFrame with 2 million rows
df = pd.DataFrame({
    'Column1': range(1, 2000001),
    'Column2': ['A'] * 2000000
})

# Define the target folder URL and file name
target_folder_url = "/sites/your_site_name/Shared Documents/your_folder_name"
target_file_name = "your_file_name.csv"
batch_size = 500  # Number of rows per batch

# Upload the DataFrame in batches
upload_csv_in_batches(ctx, df, target_folder_url, target_file_name, batch_size)
