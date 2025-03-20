#' Inspect a SQLite database file
#' 
#' @param file_path Path to SQLite database file
#' @return Information about the database structure
inspect_sqlite_db <- function(file_path) {
  library(RSQLite)
  library(tidyverse)
  
  # Connect to the database
  con <- dbConnect(SQLite(), file_path)
  
  # Get the list of tables
  tables <- dbListTables(con)
  cat("Tables in the database:\n")
  print(tables)
  
  # For each table, get column information and a sample of data
  results <- list()
  
  for (table_name in tables) {
    cat("\n===== Table:", table_name, "=====\n")
    
    # Get column information
    columns <- dbListFields(con, table_name)
    cat("Columns:\n")
    print(columns)
    
    # Get a sample of data (first 5 rows)
    if (dbGetQuery(con, paste0("SELECT COUNT(*) FROM ", table_name)) > 0) {
      sample_data <- dbGetQuery(con, paste0("SELECT * FROM ", table_name, " LIMIT 5"))
      cat("\nSample data:\n")
      print(sample_data)
      
      # Store in results list
      results[[table_name]] <- list(
        columns = columns,
        sample = sample_data
      )
    } else {
      cat("Table is empty\n")
      results[[table_name]] <- list(
        columns = columns,
        sample = NULL
      )
    }
  }
  
  # Close the connection
  dbDisconnect(con)
  
  return(results)
}