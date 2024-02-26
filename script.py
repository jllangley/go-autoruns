import os
import subprocess
import datetime
import azure.storage.blob as azure_blob

def main():
    # Execute the command
    custom_file_name = generate_custom_filename()
    with open(custom_file_name, 'wb') as output_file:
        subprocess.run(["./autorunsc.exe", "-x"], stdout=output_file)

    # Upload to Azure Blob Storage
    sas_token = "sas-token"
    blob_storage_url = "blob-url"
    upload_to_azure(custom_file_name, blob_storage_url, sas_token)


def generate_custom_filename():
    hostname = os.uname()[1]
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"{hostname}_autoruns_{current_date}.xml"


def upload_to_azure(file_path, blob_storage_url, sas_token):
    blob_service_client = azure_blob.BlobServiceClient(account_url=blob_storage_url, credential=sas_token)
    blob_client = blob_service_client.get_blob_client(container="your-container-name", blob=file_path)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

    print("File uploaded successfully.")


if __name__ == "__main__":
    main()
