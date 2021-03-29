# service-metadata-update


<!-- ABOUT THE PROJECT -->
## About The Project

**Bash and Python script files used to update service metadata for a given organization**


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
   

<!-- USAGE EXAMPLES -->
## Usage

1. Switch to to project repository.
2. Store all the media contents in a `media_files` directory with sub-folders having the same name as the service published on the Ethereum blockchain (structure maintained as per Google Drive format).<br>
   **Example:**
   ```
   project_path/
   |-- media_files/
       |-- example_service_1
           |-- test1.jpg
           |-- test2.mp4
   ```
3. Run bash script
   ```sh
   ./metadata-update.sh <org-id> <excel-file>
   ```
   `org-id`: The Organization ID of the services metadata that needs to be updated.<br>
   `excel-file`: The .xlsx file containing the information of the media ready to be uploaded.
4. Ready-to-publish service metadata JSON files are stored in the `json_files` directory under the `<service-name>.json` file format.

## Issues

1. Dependency on existing snet-cli's adding to IPFS restricts file size to 1MB. Object decoding error is raised for larger files.
2. Existing IPFS add [prints error](https://github.com/singnet/snet-cli/blob/f587902d49225ba166c4b133a1adcfcec8ce2b62/packages/snet_cli/snet/snet_cli/utils/ipfs_utils.py#L22) rather than raising an exception. This causes `null` values to be added in `url` of media.


## License  
  
This project is licensed under the MIT License - see the
[LICENSE](https://github.com/singnet/snet-cli/blob/master/snet_sdk/LICENSE) file for details.
