import os
import subprocess
import datetime
import socket
import requests

def main():
    # Execute the Autoruns
    custom_file_name = generate_custom_filename()
    autoruns_file_name = custom_file_name + "_autoruns.csv"
    with open(autoruns_file_name, 'wb') as output_file:
        subprocess.run(["./tools/autorunsc.exe","-accepteula","-nobanner","-a","*","-h","-s","-t","-c"], stdout=output_file)

    # Azure Blob Storage Config
    sas_token = "sas_toek"
    storage_account = "storage_account"
    container_name = "container"
    #Upload Autoruns to blob Storage
    upload_to_azure(autoruns_file_name, storage_account, sas_token, container_name)
    
    # Execute Sysinternals netstat equivalent
    netstat_file_name = custom_file_name + "_netstat.csv"
    with open(netstat_file_name, 'wb') as output_file:
        subprocess.run(["./tools/tcpvcon.exe", "-accepteula", "-a", "-n","-c"], stdout=output_file)
    upload_to_azure(netstat_file_name, storage_account, sas_token, container_name)
    
    # Execute Sysinfo 
    sysinfo_file_name = custom_file_name + "_sysinfo.csv"
    with open(sysinfo_file_name, 'wb') as output_file:
        subprocess.run(["systeminfo", "/FO", "CSV"], stdout=output_file)
    upload_to_azure(sysinfo_file_name, storage_account, sas_token, container_name)

def generate_custom_filename():
    hostname = socket.gethostname()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"{hostname}-{current_date}"


def upload_to_azure(blob_name, storage_account, sas_token, container_name):
    requests.put(f"https://{storage_account}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}", data=open(f"{blob_name}", "rb"), headers={"x-ms-blob-type": "BlockBlob"})

    print("File uploaded successfully.")


if __name__ == "__main__":
    main()
