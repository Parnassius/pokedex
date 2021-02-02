import csv
import os
from read_swsh import TextFile

# data_path contains the countents of the `message` folder found in sword/shield's romfs:/bin/
if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    letsgo_data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "..", "letsgo_data")
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "..", "data")
    csv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "..", "pokedex", "data", "csv")

    languages = {
        "JPN": 1,
        "Korean": 3,
        "Trad_Chinese": 4,
        "French": 5,
        "German": 6,
        "Spanish": 7,
        "Italian": 8,
        "English": 9,
        "JPN_KANJI": 11,
        "Simp_Chinese": 12,
    }

    PIKACHU = 31
    EEVEE = 32
    SWORD = 33
    SHIELD = 34

    header = ["species_id", "version_id", "language_id", "flavor_text"]
    entries = []

    # pre-letsgo
    with open(os.path.join(csv_path, "pokemon_species_flavor_text.csv"), "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        for row in reader:
            if row[1].isnumeric() and int(row[1]) not in (PIKACHU, EEVEE, SWORD, SHIELD):
                entries.append([int(row[0]), int(row[1]), int(row[2]), row[3]])

    with open(os.path.join(csv_path, "pokemon_species_flavor_text.csv"), "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",", lineterminator="\n")
        for language_dir, language_id in languages.items():
            try:
                # Parse through the .dat and .tbl
                textfiles = {
                    (PIKACHU, EEVEE): TextFile(
                        os.path.join(letsgo_data_path, language_dir, "common", "zukan_comment_A.dat"),
                        os.path.join(letsgo_data_path, language_dir, "common", "zukan_comment_A.tbl"),
                    ),
                    (SWORD,): TextFile(
                        os.path.join(data_path, language_dir, "common", "zukan_comment_A.dat"),
                        os.path.join(data_path, language_dir, "common", "zukan_comment_A.tbl"),
                    ),
                    (SHIELD,): TextFile(
                        os.path.join(data_path, language_dir, "common", "zukan_comment_B.dat"),
                        os.path.join(data_path, language_dir, "common", "zukan_comment_B.tbl"),
                    )
                }
            except UserWarning as error:
                print(error)

            try:
                for version_ids, textFile in textfiles.items():
                    dictionary = textFile.GetDict()
                    if len(dictionary) == 0:
                        raise UserWarning("Error: the files returned no data")

                    # Loop through the text file's dictionary and append the parsed data into the list
                    for label, text in dictionary.items():
                        pokemon_id, form_id = (int(i) for i in label[0].split("_")[-2:])
                        if pokemon_id == 0:
                            continue
                        if form_id != 0:  # skip descriptions of non-default forms
                            continue
                        if not text.strip():
                            continue
                        for version_id in version_ids:
                            entries.append([pokemon_id, version_id, language_id, text])

            except UserWarning as error:
                print(error)

        # Sort the list based on species id
        writer.writerow(header)
        entries.sort()
        writer.writerows(entries)
        print("Done")
