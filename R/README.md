## How to scrape IDEXX Laboratories haematology pdf reports using R/RStudio

### Requirements

You must have `pdftools` and `tidyverse` packages installed.

`find.package("pdftools")`

`find.package("tidyverse")`

If not, run:

`install.packages("pdftools")`

`install.packages("tidyverse")`

### Steps

1.  Clone or download the [smart-maps](https://github.com/HealthHackAu2018/smart-maps) repository. Alternatively, download and save the file "scrape_pdfs.R": right click the "scrape_pdfs.R" file from the smart-maps [R folder](https://github.com/HealthHackAu2018/smart-maps/tree/master/R), choose "Save Link As", then choose "All Files" for "Save as type" from the drop down menu.

2. In R/RStudio, run: `source("path_R")`, where "path_R" is the character string giving the full/relative path name of the "scrape_pdfs.R" file location.

3. In R/RStudio, run: `clean_pdf("path_pdfs")`, where "path_pdfs" is the character string giving the full/relative path name of the directory that contains one or more pdf files that need to be scraped. Once complete, the results, a "scraped_pdfs.csv" file will appear in your working directory.

### Sample code

Using relative paths:

`source("../scripts/scrape_pdfs.R")`

`clean_pdf("../sample-data/")`

Using full paths:

`source("C:/Users/Bob/Documents/GitHub/smart-maps/R/scrape_pdfs.R")`

`source("C:/Users/Bob/Documents/IndexxPdfs/2018_08")`

### Notes and assumptions

To scrape a pdf, it MUST be in the format such as `B1705_2000606271.pdf`, [available here](https://github.com/HealthHackAu2018/smart-maps/tree/master/sample-data). The `clean_pdf` function has the capability to scrape pdfs over two pages, such as `B1705_2000604358.pdf`. However, the pdf cannot be in a two-column format such as `B1705_2000609034_V2.pdf`.

Code development and testing has been documented in the file [`scrapeheartpdf.Rmd`](https://github.com/HealthHackAu2018/smart-maps/blob/master/R/scrapeheartpdf.Rmd).
