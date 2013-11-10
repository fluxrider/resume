python resume2.py resume.xml 0 text True utf-8 > davidLareau_utf-8.txt
python resume2.py resume.xml 1 text True utf-8 > davidLareau_fr_utf-8.txt
python resume2.py resume.xml 0 text True iso8859-15 > davidLareau_iso8859-15.txt
python resume2.py resume.xml 1 text True iso8859-15 > davidLareau_fr_iso8859-15.txt
python resume2.py resume.xml 0 html True utf-8 > davidLareau.html
python resume2.py resume.xml 1 html True utf-8 > davidLareau_fr.html
python resume2.py resume.xml 0 fodt True utf-8 > davidLareau.fodt
python resume2.py resume.xml 1 fodt True utf-8 > davidLareau_fr.fodt
python resume2.py resume.xml 0 text False utf-8 > davidLareau_full_utf-8.txt
python resume2.py resume.xml 1 text False utf-8 > davidLareau_full_fr_utf-8.txt
python resume2.py resume.xml 0 text False iso8859-15 > davidLareau_full_iso8859-15.txt
python resume2.py resume.xml 1 text False iso8859-15 > davidLareau_full_fr_iso8859-15.txt
python resume2.py resume.xml 0 html False utf-8 > davidLareau_full.html
python resume2.py resume.xml 1 html False utf-8 > davidLareau_full_fr.html
python resume2.py resume.xml 0 fodt False utf-8 > davidLareau_full.fodt
python resume2.py resume.xml 1 fodt False utf-8 > davidLareau_full_fr.fodt
"C:\Apps\LibreOffice 3.6\program\soffice.exe" --nologo --invisible --convert-to pdf davidLareau.fodt
"C:\Apps\LibreOffice 3.6\program\soffice.exe" --nologo --invisible --convert-to pdf davidLareau_fr.fodt
"C:\Apps\LibreOffice 3.6\program\soffice.exe" --nologo --invisible --convert-to pdf davidLareau_full.fodt
"C:\Apps\LibreOffice 3.6\program\soffice.exe" --nologo --invisible --convert-to pdf davidLareau_full_fr.fodt