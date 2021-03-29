import sys
from re import search
from pandas import read_excel


def clean_services_file():
    """Removes empty lines, '-', and '\s' character from individual service."""
    with open(file_name, 'r', encoding='utf-8') as f:
        altered_lines = [line.strip('- ') for line in f.readlines()[2:]]
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(''.join(altered_lines))


def clean_xlsx_file():
    """Creates new .xlsx file with only services that have media uploaded."""
    df = read_excel(file_name)
    altered_df = df.loc[df['Status'] == 'upload ready', :]
    altered_df.to_excel(file_name, index=False)


def metadata_to_download(file_name):
    """Updates the <org_id>_services.txt to reflect the metadata of services required to be downloaded."""
    media = []
    with open(file_name, 'r', encoding='utf-8') as f:
        all_services = f.read().splitlines()
    df = read_excel('Gallery Media Content Gathering.xlsx')
    for service in all_services:
        if service in list(df['AI Service Folder Name']):
            media.append(service)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(media))
        f.write('\n')
            
def media_not_present():
    """Finds media present in the excel file but not registered through the snet-cli."""
    media_not_present = []
    for service in list(df['AI Service Folder Name']):
        if service not in media:
            media_not_present.append(service)

if __name__ == '__main__':
    file_name = sys.argv[1]
    if search(r'.+\.xlsx$', file_name):
        clean_xlsx_file()
    else:
        clean_services_file()