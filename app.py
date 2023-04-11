from htmltools import css, HTML
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, reactive_read, register_widget
from ipyleaflet import Map, Marker, Popup,leaflet

from read_db import find_db

app_ui = ui.page_fluid(
    
    ui.div(
    ui.input_select("db","Choose a database:",["USA","Global"]),
    # Filters for both databases
    ui.input_selectize("filter_1", "Filter 1", [],multiple=True),
    ui.input_selectize("filter_2", "Filter 2", [],multiple=True),
    ui.input_selectize("filter_3", "Filter 3", [],multiple=True),
    ui.input_selectize("filter_4", "Filter 4", [],multiple=True),
    ui.input_selectize("filter_5", "Filter 5", [],multiple=True),
    ui.output_table("table"),
    style=css(
            display="flex", justify_content="left", align_items="center", gap="2rem"
        ),
    ),
    
    ui.div(
        ui.input_slider("zoom", "Map zoom level", value=3, min=1, max=18),
        ui.output_ui("map_bounds"),
        style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
        ),
    ),
    output_widget("map")
)

def server(input, output, session):
    
    map = Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    # When zooming directly on the map, update the slider's value (2 and 3)
    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

    @output
    def widget():
        db, filters = find_db(input.db())

        #UPDATE FILTERS BASED ON DB
        for i in range(1,len(filters)+1):
            ui.update_select(
            f"filter_{i}",
            label=f"Select {filters[i-1]}",
            choices=list(db[filters[i-1]].unique()),
            selected=None,)

        # SET filters

        for sub_filter in filters:
            db = db[db[sub_filter].isin(input.filter1())]

        for dessal in db:
            marker = Marker(location=(dessal['latitude'], dessal['longitude']))
            #message = HTML()
            #message.value = "Description of Dessal:"
            #message.description = info_from_database()   -> to be made
            map.add_layer(marker)
            #marker.popup = message
        return db.to_html()
    

app = App(app_ui, server)


# Deploy ::
# rsconnect deploy shiny PATH --NAME --APP