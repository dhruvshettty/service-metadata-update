#!/bin/bash

org_id=$1
excel_file=$2
path_to_project=/home/$(whoami)/SingularityNET/metadata-update

if [ -z "${org_id}" ]; then
  echo "Error: Enter the first positional parameter for Organization ID."
  exit 125
fi
if [ -z "${excel_file}" ]; then
  echo "Error: Enter the second positional parameter for the Excel file."
  exit 125
fi

function loader {
  spin='-\|/'
  i=0
  while kill -0 "$pid" 2>/dev/null
  do
    i=$(( (i+1) %4 ))
    printf "\r%s" "${spin:$i:1}"
    sleep .1
  done
}

echo "Getting all the services for the Organization ID: '${org_id}'"
snet organization list-services "$org_id" > "${org_id}"_services.txt &
pid=$!
loader $pid
printf "\nCleaned and stored in %s_services.txt" "$org_id"
python clean_services.py "${org_id}"_services.txt
printf "\nCleaning '%s'\n" "$excel_file"
python clean_services.py "$excel_file"
echo "Checking media metadata to be downloaded..."
python -c "from clean_services import metadata_to_download; metadata_to_download('${org_id}_services.txt')"

input="${path_to_project}/${org_id}_services.txt"
output="${path_to_project}/json_files"
if [ -f "$input" ]
then
  if [ ! -d "$output" ]
  then
    mkdir "$output"
  fi
  echo "Getting metadata for services present in '${org_id}_services.txt'"
  while IFS= read -r line
  do
    snet service print-metadata "$org_id" "$line" > "${output}/${line}.json"
  done < "$input" &
  pid=$!
  loader $pid
  printf "\nAll service metadata stored in %s/json_files\n" "$path_to_project"
fi
cd "${path_to_project}"/json_files || { echo "Path ${path_to_project}/json_files was not found"; exit 1; }
for file in *
do
  full_filename=$(basename -- "$file")
  filename="${full_filename%.*}"
  cd /home/dhruvshetty/SingularityNET/metadata-update/media_files/${filename}/
  if [ $? -eq 0 ]
  then
    for media in *
    do
      echo "Adding ${media} to ${filename} service"
      snet service metadata-add-media $(basename -- "$media") --metadata-file "${output}/${full_filename}"
    done
  else
    continue
  fi
done
echo "If File error, file size too big (> 1MB)"
echo "Task complete."