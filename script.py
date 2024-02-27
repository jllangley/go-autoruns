import os
import subprocess
import datetime
import socket
import requests

def main():
    # Execute the command
    custom_file_name = generate_custom_filename()
    with open(custom_file_name, 'wb') as output_file:
        subprocess.run(["./tools/autorunsc.exe", "-x"], stdout=output_file)

    # Upload to Azure Blob Storage
    sas_token = "sas_token"
    storage_account = "storage_name"
    container_name = "container_name"
    upload_to_azure(custom_file_name, storage_account, sas_token, container_name)


def generate_custom_filename():
    hostname = socket.gethostname()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"{hostname}-{current_date}_autoruns.csv"


def upload_to_azure(blob_name, storage_account, sas_token, container_name):
    requests.put(f"https://{storage_account}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}", data=open(f"{blob_name}", "rb"), headers={"x-ms-blob-type": "BlockBlob"})

    print("File uploaded successfully.")


if __name__ == "__main__":
    main()
