## ---------------------------------------------------------------------------------------------------------------------------------
load("precipitation_00-03.Rdata")


## ---------------------------------------------------------------------------------------------------------------------------------

library(tidyr)
library(dplyr)

combined_df <- do.call(rbind, list_year)


PRCP_WA_data = merge(combined_df, stations_wa, by.x = 'station', by.y = 'id', all.x= TRUE, all.y = FALSE)
PRCP_WA_data$date <- as.Date(PRCP_WA_data$date, format = "%Y-%m-%dT%H:%M:%S")
PRCP_WA_data <-PRCP_WA_data %>% drop_na()

PRCP_WA_data$month <- as.numeric(format(PRCP_WA_data$date, "%m"))
PRCP_WA_data$year <- as.numeric(format(PRCP_WA_data$date, "%Y"))
PRCP_WA_data <- PRCP_WA_data %>% select(-date)

PRCP_WA_data



## ---------------------------------------------------------------------------------------------------------------------------------
library(shiny)
library(leaflet)
library(RColorBrewer)
library(plotly)
library(ggplot2)
library(rsconnect)


ui <- fluidPage(
  titlePanel("Precipitation in Washington State"),
  theme = bslib::bs_theme(bootswatch = "darkly"),
  
  
  sidebarLayout(
    sidebarPanel(
      selectInput("selected_year", "select a year", choices = c(2000:2003)),
      sliderInput("selected_month", "Select a Month", min = 1, max = 12, value = 1),
      plotlyOutput("barPlot"),

      ),
    mainPanel(

      leafletOutput("map",width = "85%", height =500)
      )
  )
)


server <- function(input, output) {
  filteredData <- reactive({
    PRCP_WA_data[PRCP_WA_data$year %in% input$selected_year & PRCP_WA_data$month %in% input$selected_month, ]
  })
  
  custom_palette <- brewer.pal(9, "Blues")[c(1,5,7)]
  add_palette <- c("#051E78", "#180563")
  final_palette <- c(custom_palette, add_palette)
  
  output$map <- renderLeaflet({
    pal <- colorNumeric(palette = final_palette, 
                        domain = PRCP_WA_data$value,
                        )
  
    leaflet() %>% 
      addTiles() %>% 
      setView(
        lng=-120.740135, 
        lat=47.401076, 
        zoom = 7)%>% 
      addCircles(data = filteredData(),
                 lng = ~longitude, 
                 lat = ~latitude, 
                 weight = 1, 
                 radius = 7500, 
                 fillOpacity  = 0.8,
                 popup = ~paste("Name:", name, "<br>Value:", value), 
                 fillColor  = ~pal(value)) %>%
      addLegend(position = "bottomright",
                pal = pal,
                values = (PRCP_WA_data$value),
                title = "value",
                opacity = 1)
    
    }) 
  output$barPlot <- renderPlotly({

    pal <- colorNumeric(palette = final_palette, 
                        domain = PRCP_WA_data$value,
                        )   
    top_5_largest <- head(arrange(filteredData(), desc(value)), 5)
    
    plot_ly(top_5_largest, x = ~name, y = ~top_5_largest$value, type = "bar",marker = list(color =  ~pal(value)), showlegend = FALSE)%>%
      plotly::layout( xaxis = list(categoryorder = "total descending",showticklabels = FALSE))

  })
  
}

shinyApp(ui, server)



