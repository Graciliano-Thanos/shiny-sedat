from htmltools import css, HTML
from shiny import App, render, ui, reactive
from shinywidgets import output_widget, reactive_read, register_widget
from ipyleaflet import Map, Marker, Popup,leaflet

from read_db import find_db,info_from_db,plot_location,plot_capacity

app_ui = ui.page_fluid(
    
    ui.layout_sidebar(
        ui.panel_sidebar(
    ui.input_select("db","Choose a database:",["USA","Global"]),
    # Filters for both databases
    ui.input_selectize("filter_1", "Select Size", [],multiple=True),
    ui.input_selectize("filter_2", "Select Technology", [],multiple=True),
    ui.input_selectize("filter_3", "Select Plant Type", [],multiple=True),
    ui.input_slider("zoom", "Map zoom level", value=3, min=1, max=18),
    ui.input_action_button("run","Run Filtered Database")
    ),
    ui.panel_main(
    ui.div(ui.output_ui("map_bounds"),
    output_widget("map")
    ),
    ui.div(ui.output_plot("cap_graph"),
           ui.output_plot("location_graph"),
           style=css(
            display="flex", justify_content="bottom", align_items="center")
        )
    ,
    style=css(
            display="flex-column", align_items="flex-start", gap="2rem"))
),
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

    @reactive.Effect
    def _():
        db, filters = find_db(input.db())

        #UPDATE FILTERS BASED ON DB
        for i in range(1,len(filters)+1):
            ui.update_select(
            f"filter_{i}",
            choices=list(db[filters[i-1]].unique()),
            selected=None,)

    @reactive.Effect
    @reactive.event(input.run)
    def _():
        db, filters = find_db(input.db())

        filter_table = [input.filter_1(),input.filter_2(),input.filter_3()]

        for i in range(len(filters)):
            if filter_table[i] != ():
                db = db[db[filters[i]] == filter_table[i][0]]

        for ind in db.index:
           marker = Marker(location=(db['Latitude'][ind], db['Longitude'][[ind]]),draggable=False)
           message = Popup()
           message.value = "Description of Dessal:"
           message.description = info_from_db("dessal")
           map.add_layer(marker)
           marker.popup = message

        return db
    
    @output
    @render.plot
    @reactive.event(input.run)
    def location_graph():
        db,filters = find_db(input.db())
        plot_location(db,input.db())

    @output
    @render.plot
    @reactive.event(input.run)
    def cap_graph():
        db,filters = find_db(input.db())
        plot_capacity(db,input.db())


app = App(app_ui, server)


# Deploy ::
# rsconnect deploy shiny PATH --NAME --APP