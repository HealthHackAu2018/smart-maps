Installation requirements:
- PHP version 7.2
- run Composer to install the composer libaries (run composer install)
- install pdftotext on the server, set the installation directory in:
vendor/spatie/pdf-to-text/src/Pdf.php line 19


Use:
Upload 19 files at a time 
Copy the text in the browser and save in a text editor as .csv

Restrictions (Check with server hosting):
Depending on the server that is hosting this site the upload is restricted to:
- Maximum upload size for page (default 8Mb)
- Maximum number of files that can be uploaded (default 20)
- Maximum size of each file that can be uploaded (defaul 128Mb)
