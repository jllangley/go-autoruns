from azure.storage.blob import BlobServiceClient, BlobClient
import os
import pandas as pd

def process_xml_files(connection_string, source_container_name, archive_container_name):
    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=connection_string, credential=sas_token)

    # Reference to the source container
    source_container = blob_service_client.get_container_client(source_container_name)

    # Reference to the archive container
    archive_container = blob_service_client.get_container_client(archive_container_name)

    # List blobs in the source container
    blob_list = source_container.list_blobs()

    for blob in blob_list:
        # Check if the file is an XML file
        print(blob.name)
        if blob.name.endswith('xml'):
            # Download the blob
            blob_client = source_container.get_blob_client(blob)
            downloader = blob_client.download_blob()
            with open(blob.name, "wb") as download_file:
                download_file.write(downloader.readall())

            # Archive the blob in another container
            archive_blob_client = archive_container.get_blob_client(blob.name)
            with open(blob.name, "rb") as data:
                archive_blob_client.upload_blob(data, overwrite=True)

            # Call the convert_to_json function
            convert_to_json(blob.name)

            # Optionally, delete the original file after processing
            #blob_client.delete_blob()

            # Clean up the downloaded file
            #os.remove(blob.name)

def convert_to_json(xml_file):
    # Implement this function to convert XML to JSON
    df = pd.read_xml(xml_file, encoding='utf-16')
    savetojson = df.to_json(f"{xml_file[:-4]}"+".json", orient="records")
    savetojson
# Usage
connection_string = os.getenv("StorageAccountName")
source_container_name = os.getenv("AutoRunsContainer")
archive_container_name = os.getenv("AutoRunsArchiveContainer")
sas_token= os.getenv("StorageSasToken")

process_xml_files(connection_string, source_container_name, archive_container_name)

