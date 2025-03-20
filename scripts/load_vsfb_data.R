#' Load VSFB deployment information and match with wind data files
#' 
#' @param deployments_path Path to the deployments2023.csv file
#' @param raw_data_dir Path to directory containing raw data files
#' @return A dataframe containing all wind data from matching files
load_vsfb_wind_data <- function(deployments_path, raw_data_dir = "../raw_data") {
  # Load required packages
  if (!requireNamespace("tidyverse", quietly = TRUE)) {
    stop("Package tidyverse is required. Please install it first.")
  }
  if (!requireNamespace("RSQLite", quietly = TRUE)) {
    stop("Package RSQLite is required. Please install it first.")
  }
  
  library(tidyverse)
  library(RSQLite)
  
  # Read deployment information
  deployments <- read_csv(deployments_path)
  
  # Extract unique wind meter names, removing NA values
  wind_meter_names <- deployments %>%
    filter(!is.na(wind_meter_name)) %>%
    pull(wind_meter_name) %>%
    unique()
  
  # Get a list of available raw data files
  raw_files <- list.files(raw_data_dir, pattern = "\\.s3db$", full.names = TRUE)
  raw_file_names <- basename(raw_files) %>% 
    tools::file_path_sans_ext()
  
  # Check if all wind meter names exist in raw files
  missing_files <- wind_meter_names[!wind_meter_names %in% raw_file_names]
  if (length(missing_files) > 0) {
    stop("The following wind meter files are missing: ", 
         paste(missing_files, collapse = ", "))
  }
  
  # Filter for only the files we need
  needed_files <- raw_files[raw_file_names %in% wind_meter_names]
  
  # Function to read a SQLite database file
  read_s3db <- function(file) {
    wind_meter_name <- tools::file_path_sans_ext(basename(file))
    
    # Connect to the database
    con <- dbConnect(SQLite(), file)
    
    # Get list of tables
    tables <- dbListTables(con)
    
    # Initialize empty dataframe
    data <- tibble()
    
    # Check if Wind table exists
    if ("Wind" %in% tables) {
      # Read the Wind table
      data <- dbReadTable(con, "Wind") %>%
        as_tibble() %>%
        # Add wind meter name as a source column
        mutate(wind_meter_name = wind_meter_name)
      
      message("Loaded ", nrow(data), " rows from Wind table in ", basename(file))
    } else {
      warning("No Wind table found in ", file)
    }
    
    # Close the connection
    dbDisconnect(con)
    
    return(data)
  }
  
  # Read all needed SQLite files and combine into one dataframe
  all_data <- map_dfr(needed_files, read_s3db)
  
  return(all_data)
}