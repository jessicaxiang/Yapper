library(dplyr)
library(ggplot2)
library(htmlwidgets)
library(leaflet)
library(geosphere)
library(htmltools)
library(KernSmooth)
library(raster)
library(ggmap)
library(shiny)

#---------------------------------------------------------------------

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  #fileinput - reactive function 
  restaurant.dt <- reactive({
    if (is.null(input$file1)) {
      return (NULL) 
    } else {
      read.csv(input$file1$datapath, stringsAsFactors = FALSE)
    }
  })
  
  filtered.dt <- reactive({
    filtered.dt <- restaurant.dt() %>%
      filter(price_tier <= input$price_tier) %>%
      filter(return == input$radio)
  })
  
  filtered.lflt <- eventReactive(
    input$button_generate,
    {
      req(restaurant.dt())
      
      lines.ls <-
        lapply(
          1:nrow(filtered.dt()),
          function(i) {
            data.frame(
              lng = c(filtered.dt()$request_long[i], filtered.dt()$business_long[i]),
              lat = c(filtered.dt()$request_lat[i], filtered.dt()$business_lat[i]),
              dist = c(distGeo(
                p1 = as.matrix(filtered.dt()[i, c('request_long', 'request_lat')]),
                p2 = as.matrix(filtered.dt()[i, c('business_long', 'business_lat')])
              ))
            )
          }
        )
      
      map <- leaflet() %>%
        addProviderTiles('Stamen.Toner')
      
      for (i in 1:nrow(filtered.dt())) {
        map <- map %>%
          addPolylines(
            data = lines.ls[[i]],
            lat = ~lat,
            lng = ~lng,
            color="red",
            weight = 2
          ) %>%
          addCircleMarkers(
            data = filtered.dt()[i,],
            lat = ~request_lat,
            lng = ~request_long,
            radius = 4,
            stroke = NA,
            fillColor = "blue",
            fillOpacity = 1,
            weight = 5
          ) %>%
          addCircleMarkers(
            data = filtered.dt()[i,],
            lat = ~business_lat,
            lng = ~business_long,
            radius = 4,
            stroke = NA,
            fillColor = "green",
            fillOpacity = 1,
            weight = 5
          )
      }
      map
      
    })
  output$filtered.lflt <- renderLeaflet({filtered.lflt()})
  cat("rendering")
  
}