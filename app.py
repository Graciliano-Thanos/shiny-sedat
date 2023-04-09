from htmltools import css
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, reactive_read, register_widget
import ipyleaflet as L

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
    @output
    @render.table
    def table():
        db, filters = find_db(input.db())

        #UPDATE FILTERS BASED ON DB
        for i in range(1,len(filters)+1):
            ui.update_select(
            f"filter_{i}",
            label=f"Select {filters[i-1]}",
            choices=list(db[filters[i-1]].unique()),
            selected=None,)

        # SET filters

        indx_cou = db[filters[0]].isin(input.filter1())
        indx_loc = db[filters[1]].isin(input.filter2())
        indx_cap = db[filters[2]].isin(input.filter3())
        indx_tec = db[filters[3]].isin(input.filter4())
        indx_pla = db[filters[-1]].isin(input.filter5())
        
        sub_db = db[indx_cou & indx_loc & indx_cap & indx_tec & indx_pla]

        return sub_db.to_html()
    
    map = L.Map(center=(51.476852, -0.000500), zoom=12, scroll_wheel_zoom=True)
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    # When zooming directly on the map, update the slider's value (2 and 3)
    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

app = App(app_ui, server)


# Deploy ::
# rsconnect deploy shiny PATH --NAME --APP