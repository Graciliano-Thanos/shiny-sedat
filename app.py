from shiny import App, render, ui
from read_db import find_db

app_ui = ui.page_fluid(
    ui.input_select("db","Choose a database:",["CityWaterCosts","countries_generalized","Desalplants","global_desal","roads_proxy","TexasCountyWaterPrices","tx_county_water_prices","us_county","USAWeatherStations"]),
    ui.output_table("table"),
)


def server(input, output, session):
    @output
    @render.table
    def table():
        db = find_db(input.db())
        return db

app = App(app_ui, server)