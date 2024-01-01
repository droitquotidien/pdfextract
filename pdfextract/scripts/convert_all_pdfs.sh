#!/bin/bash

# dans le terminal, run chmod +x convert_all_pdfs.sh
#./convert_all_pdfs.sh

DOCKER_IMAGE="pdftools"
INPUT_DIR=$(pwd)/exemples
OUTPUT_DIR=$(pwd)/output

# Vérifier que les directory pour les output (= les .txt issus de la conversion des .pdf) existent, ou les créer
mkdir -p $OUTPUT_DIR

# Boucle pour récupérer tous les fichiers .pdf dans le dossier input
for PDF_FILE in $INPUT_DIR/*.pdf; do
    # Récupérer le nom du fichier sans extension
    FILE_NAME=$(basename -- "$PDF_FILE")
    FILE_NAME_NO_EXT="${FILE_NAME%.*}"

    # Run Docker container et executer pdftotext
    docker run -v $INPUT_DIR:/data -v $OUTPUT_DIR:/output -it $DOCKER_IMAGE /usr/bin/pdftotext -layout /data/$FILE_NAME /output/$FILE_NAME_NO_EXT.txt

    # Print un message nous assurant que la conversion a été effectuée pour tous nos fichiers
    echo "Conversion complete for $FILE_NAME. Text file generated: $OUTPUT_DIR/$FILE_NAME_NO_EXT.txt"
done

echo "All PDF files processed."

