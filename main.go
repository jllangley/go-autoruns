
package main

import (
    "context"
    "embed"
    "fmt"
    "io"
    "net/http"
    "net/url"
    "os"
    "os/exec"
    "time"

    "github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
)

//go:embed autorunsc
var autorunsc []byte

func main() {
    // Write the embedded autorunsc.exe to a file
    err := os.WriteFile("autorunsc.exe", autorunsc, 0755)
    if err != nil {
        panic(err)
    }

    // Generate custom filename
    hostname, err := os.Hostname()
    if err != nil {
        panic(err)
    }
    currentDate := time.Now().Format("2006-01-02")
    customFileName := fmt.Sprintf("%s_autoruns_%s.xml", hostname, currentDate)

    // Execute the command
    cmd := exec.Command("./autorunsc.exe", "-x")
    outputFile, err := os.Create(customFileName)
    if err != nil {
        panic(err)
    }
    defer outputFile.Close()

    cmd.Stdout = outputFile
    err = cmd.Run()
    if err != nil {
        panic(err)
    }

    // Upload to Azure Blob Storage
    sasToken := "sas-token"
    blobStorageURL := "blob-url"
    err = uploadToAzure(customFileName, blobStorageURL, sasToken)
    if err != nil {
        panic(err)
    }
}

func uploadToAzure(filePath, blobStorageURL, sasToken string) error {
    // Construct the full URL
    fullURL := fmt.Sprintf("%s/%s%s", blobStorageURL, filePath, sasToken)

    // Parse the SAS token
    credential, err := azblob.NewAnonymousCredential()
    if err != nil {
        return err
    }

    // Create a pipeline
    p := azblob.NewPipeline(credential, azblob.PipelineOptions{})

    // Parse the URL
    URL, err := url.Parse(fullURL)
    if err != nil {
        return err
    }

    // Create a BlobClient
    blobClient, err := azblob.NewBlockBlobClient(*URL, p)
    if err != nil {
        return err
    }

    // Open the file
    file, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer file.Close()

    // Upload the file
    _, err = blobClient.Upload(context.TODO(), file, nil)
    if err != nil {
        return err
    }

    fmt.Println("File uploaded successfully.")
    return nil
}
