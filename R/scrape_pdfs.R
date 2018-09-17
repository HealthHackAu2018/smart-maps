# Description: Scrape pdfs from IDEXX Laboratories with haemotology data
# Author: Rebecca Johnston <rebecca.lea.johnston@gmail.com>

# Load required libraries
library("pdftools")
library("tidyverse")

# The only argument of the function "scrape_pdfs" is "pdfdir", which is the
# character string giving the path name of the directory containing pdfs that
# need to be scraped. The function will return a .csv file of the results in
# your current working directory. You also have the option of assigning the
# scrape_pdfs call a name, which will save the results (a dataframe) to the 
# assigned name.

scrape_pdfs <- function(pdfdir){
  # Initiate data frame with all variables required
  df <- data.frame(
    Variable = c("Animal ID", "Case ID", "Unique ID", "Sex", "Age", "Collected",
                 "Chip ID", "Reported", "RBC", "HAEMOGLOBIN", "HAEMATOCRIT",
                 "MCV", "MCH", "MCHC", "PLATELETS", "PLATELET COUNT", "WBC",
                 "NEUTROPHILS%", "NEUTROPHILS", "LYMPHOCYTES%", "LYMPHOCYTES",
                 "MONOCYTES%", "MONOCYTES", "EOSINOPHILS%", "EOSINOPHILS",
                 "BASOPHILS%", "BASOPHILS", "NUCLEATED RBCS", "PROTEIN PLASMA",
                 "FIBRINOGEN", "PLASMA APPEARANCE", "BLOOD SMEAR",
                 "EXAMINATION"))
  
  # List files that end in pdf
  files <- list.files(path = pdfdir, pattern = "*.pdf$", full.names = TRUE)
  for(i in files) {
    
    print(paste0("Scraping ", i))
    raw_table <- pdf_text(i)
    
    # If pdf has more than one page, only analyse first page
    if(length(raw_table != 1)){
      raw_table <- raw_table[1]
    }
    
    split_table <- str_split(raw_table, "\r\n", simplify = TRUE)
    
    # Collect haematology data
    table_start <- stringr::str_which(split_table, "RBC\\s{2,}")
    table_end <- stringr::str_which(split_table, "BLOOD SMEAR")
    haem_table <- split_table[1, (table_start):(table_end)] %>% 
      str_replace_all(., "\\s{2,}", "_") %>%
      str_split_fixed(., "_", n = 4) %>%
      as.data.frame() %>%
      select(V1, V2)
    
    # Collect header information for metadata
    meta_start <- stringr::str_which(split_table, "Animal ID")
    meta_end <- stringr::str_which(split_table, "Reported")
    meta_table <- split_table[1, (meta_start):(meta_end)] %>%
      str_replace_all(., "\\s{2,}", "_")
    meta_table[1] <- gsub("(^.*)(Animal ID.*$)", "\\2", meta_table[1])
    meta_table[2] <- gsub("(^.*)(Unique ID.*$)", "\\2", meta_table[2])
    meta_table[3] <- gsub("(^Collected.*)\\s(Received.*$)", "\\1_\\2",
                          meta_table[3])
    meta_table <- str_split(meta_table, "_", simplify = FALSE) %>%
      unlist(.) %>%
      str_split_fixed(., ":\\s*", n = 2) %>%
      as.data.frame()
    
    # Collect footer information
    foot_start <- stringr::str_which(split_table, "EXAMINATION")
    foot_end <- stringr::str_which(split_table, "For tests indicated by a hash")
    foot_table <- split_table[1, (foot_start):(foot_end - 1)] %>%
      str_replace_all(., "\\s{2,}", "")
    foot_table[1] <- gsub("(^EXAMINATION)(.*$)", "\\1_\\2", foot_table[1])
    foot_table <- unlist(foot_table) %>%
      stringr::str_c(., sep = "", collapse = " ") %>%
      str_split(., "_", simplify = FALSE) %>%
      unlist(.)
    foot_table <- as.data.frame(matrix(foot_table, ncol = 2, byrow = TRUE))
    
    # Save unique file name to create a unique column name
    mycolname <- str_replace(i, "(^.+/)(.*)(.pdf$)", "\\2")
    
    # Bind three tables created from same pdf together
    pdf_table <- suppressWarnings(bind_rows(meta_table, haem_table, 
                                            foot_table)) %>% 
      dplyr::rename(Variable = V1, !!mycolname := V2)
    
    # Bind pdf_table to df
    df <- suppressWarnings(full_join(df, pdf_table, by = "Variable"))
  }
  
  # Save results to file
  write.csv(df, file = "scraped_pdfs.csv", row.names = FALSE)
  return(df)
}
