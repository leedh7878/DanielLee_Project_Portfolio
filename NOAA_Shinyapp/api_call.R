library(httr)
library(jsonlite)
library(dotenv)

dotenv::load_dot_env()

api_token = Sys.getenv("API_KEY") #enter your token

format_url <- function(types){
  formatted_url <- paste("https://www.ncei.noaa.gov/cdo-web/api/v2/", types, sep = "")
  
  res = GET(formatted_url, add_headers(token = api_token))
  
  return (res)
}

rawToRobj <- function(res){
  data= fromJSON(rawToChar(res$content))
  
  return (data)
}

# resp_datasets = format_url('datasets')
# 
# datasets = rawToRobj(resp_datasets)
# datasets
# 
# res_datac = format_url('datacategories?limit=100')
# 
# data_categories = rawToRobj(res_datac)
# data_categories
# 
# res_dtypes = format_url('datatypes?limit=100')
# 
# data_types = rawToRobj(res_dtypes)
# data_types  <- data_types$results[, -c(1,2)]
# data_types
# 
# resp_locc = format_url('locationcategories')
# data_locc = rawToRobj(resp_locc)
# data_locc

#stations
stations_wa_url = format_url('stations?locationid=FIPS:53&startdate=2000-01-01&enddate=2003-12-29&limit=1000')

stations_wa_obj = rawToRobj(stations_wa_url)

stations_wa =stations_wa_obj$results[,c('name','latitude','longitude', 'id')]


list_year <- list()

endpoint = 'data'

query_params <- list(
  datasetid = "GSOM",
  datatypeid = "PRCP",
  locationid = "FIPS:53",
  startdate = "2000-01-01",
  enddate = "2000-01-31",
  limit = 1000,
  offset = 1
)


for (i in 2000:2003){
  start_date = paste(as.character(i),"-01-01",sep="")
  end_date = paste(as.character(i),"-12-31",sep="")
  query_params$startdate = start_date
  query_params$enddate = end_date  
  query_params$offset = 1
  
  number_of_rows <- 1000
  
  df_year = data.frame()
  
  while(number_of_rows ==1000){
    query_string <- paste(names(query_params), query_params, sep = "=", collapse = "&")
    concat_query <- paste(endpoint, '?', query_string, sep="")
    print(concat_query)
    
    df <- rawToRobj(format_url(concat_query))
    df <- df$results
    number_of_rows <- nrow(df)

    query_params$offset <-query_params$offset + 1000
    
    df_year = rbind(df_year, df)
  }
  
  
  list_year[[paste(as.character(i),'prcp', sep="")]] = df_year
}

save(stations_wa, list_year, file = "precipitation_00-03.Rdata")


