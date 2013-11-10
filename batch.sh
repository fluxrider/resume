#!/bin/sh

# Generate the resume files in all formats and languages
./resume2.py resume.xml 0 text True utf-8 > davidLareau_utf8.txt
./resume2.py resume.xml 1 text True utf-8 > davidLareau_fr_utf8.txt
./resume2.py resume.xml 0 text True iso8859-15 > davidLareau_iso8859-15.txt
./resume2.py resume.xml 1 text True iso8859-15 > davidLareau_fr_iso8859-15.txt
./resume2.py resume.xml 0 html True utf-8 > davidLareau.html
./resume2.py resume.xml 1 html True utf-8 > davidLareau_fr.html
./resume2.py resume.xml 0 fodt True utf-8 > davidLareau.fodt
./resume2.py resume.xml 1 fodt True utf-8 > davidLareau_fr.fodt
./resume2.py resume.xml 0 text False utf-8 > davidLareau_full_utf8.txt
./resume2.py resume.xml 1 text False utf-8 > davidLareau_full_fr_utf8.txt
./resume2.py resume.xml 0 text False iso8859-15 > davidLareau_full_iso8859-15.txt
./resume2.py resume.xml 1 text False iso8859-15 > davidLareau_full_fr_iso8859-15.txt
./resume2.py resume.xml 0 html False utf-8 > davidLareau_full.html
./resume2.py resume.xml 1 html False utf-8 > davidLareau_full_fr.html
./resume2.py resume.xml 0 fodt False utf-8 > davidLareau_full.fodt
./resume2.py resume.xml 1 fodt False utf-8 > davidLareau_full_fr.fodt

# convert the fodt to pdf
#unoconv -f pdf davidLareau_full.fodt
#unoconv -f pdf davidLareau_full_fr.fodt
#unoconv -f pdf davidLareau.fodt
#unoconv -f pdf davidLareau_fr.fodt
soffice --nologo --invisible --convert-to pdf davidLareau.fodt
soffice --nologo --invisible --convert-to pdf davidLareau_fr.fodt
soffice --nologo --invisible --convert-to pdf davidLareau_full.fodt
soffice --nologo --invisible --convert-to pdf davidLareau_full_fr.fodt

# convert the utf-8 text files to western iso-8859-15 because some browser (e.g. Chrome) doesn't detect utf-8 correctly
iconv -f UTF-8 -t ISO-8859-15 -o davidLareau_full.txt davidLareau_full_utf8.txt
iconv -f UTF-8 -t ISO-8859-15 -o davidLareau_full_fr.txt davidLareau_full_fr_utf8.txt
iconv -f UTF-8 -t ISO-8859-15 -o davidLareau.txt davidLareau_utf8.txt
iconv -f UTF-8 -t ISO-8859-15 -o davidLareau_fr.txt davidLareau_fr_utf8.txt
