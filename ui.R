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

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Yelper Restaurant Dashboard"),
  
  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    sidebarPanel(
      fileInput('file1', 'Choose file to upload',
                accept = c(
                  'text/csv',
                  'text/comma-separated-values',
                  'text/tab-separated-values',
                  'text/plain',
                  '.csv',
                  '.tsv'
                )),
      radioButtons("radio", "Filter based on rating",
                   choices = list("Yes" = 1, "No" = 0), 
                   selected = 1),
      sliderInput("price_tier",
                  "Choose your price tier",
                  min = 0,
                  max = 40,
                  value = 0,
                  step = 10),
      actionButton("button_generate", "Generate",
                   icon = icon("play-circle"))
    ),
    
    # Show a plot of the generated distribution
    mainPanel(
      leafletOutput("filtered.lflt")
    )
  )
))