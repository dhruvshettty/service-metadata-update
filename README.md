# service-metadata-update


<!-- ABOUT THE PROJECT -->
## About The Project

**Bash and Python script files used to update service metadata for a given organization.<br>**


<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dhruvshettty/service-metadata-update.git
   ```
2. Install dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```
3. Set the path for the project in the `metadata-update.sh`
   ```
   path_to_project = <local_path>
   ```
4. Google Drive API:
   1.  Enable [Google Drive API](https://developers.google.com/drive/api/v3/enable-drive-api) on the GCP Console.
   2.  Set up [OAuth 2.0](https://developers.google.com/drive/api/v3/about-auth) flow. (OAuth consent screen + Credentials)
   3.  Download the Client ID and Client secret (as `credentials.json`) and store in `path_to_project` directory.
   

<!-- USAGE EXAMPLES -->
## Usage

1. Switch to to project repository. (`path_to_project`)
2. The Drive API stores the media contents in a `media_files` directory with sub-folders having the same name as the service published on the Ethereum blockchain <br>
   **Example:**
   ```
   project_path/
   |-- media_files/
       |-- example_service_1
           |-- Media Gallery Content
              |-- test1.jpg
              |-- test2.mp4
   ```
3. In the download_media.py module, enter the unique shared driveID to download from.
   ```python
    folder = service.files().list(
         corpora='drive',
         driveId='<Enter Shared Drive ID>',
         ...
   ```
4. Run the bash script.
   ```sh
   ./metadata-update.sh <org-id> <excel-file>
   ```
   `org-id`: The Organization ID of the services metadata that needs to be updated.<br>
   `excel-file`: The .xlsx file containing the information of the media ready to be uploaded.
5. The OAuth flow created earlier is used to authenticate the user through a Google Sign-In before accessing the shared drive. 
6. Ready-to-publish service metadata JSON files are stored in the `json_files` directory under the `<service-name>.json` file format.

## Issues

1. Dependency on existing snet-cli's adding to IPFS restricts file size to 1MB. Object decoding error is raised for larger files.
2. Existing IPFS add [prints error](https://github.com/singnet/snet-cli/blob/f587902d49225ba166c4b133a1adcfcec8ce2b62/packages/snet_cli/snet/snet_cli/utils/ipfs_utils.py#L22) rather than raising an exception. This causes `null` values to be added in `url` of media.


## License  
  
This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/snet-cli/blob/master/LICENSE) file for details.
