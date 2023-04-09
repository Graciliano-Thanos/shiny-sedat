from shiny import App, render, ui, reactive
from read_db import find_db

app_ui = ui.page_fluid(
    ui.input_select("db","Choose a database:",["Desalplants","global_desal"]),
    
    # Filters for both databases
    ui.input_select("filter_1", "Filter 1", [],multiple=True),
    ui.input_select("filter_2", "Filter 2", [],multiple=True),
    ui.input_select("filter_3", "Filter 3", [],multiple=True),
    ui.input_select("filter_4", "Filter 4", [],multiple=True),
    ui.input_select("filter_5", "Filter 5", [],multiple=True),

    ui.output_table("table"),
)

def server(input, output, session):
    @output
    @render.table
    @reactive.Effect()
    def table():
        db, filters = find_db(input.db())

        #UPDATE FILTERS BASED ON DB
        for i in range(1,len(filters)+1):
            ui.update_select(
            f"filter_{i}",
            label=f"Select {filters[i-1]}",
            choices=db[filters[i-1]],
            selected=None,)

        # SET filters

        indx_cou = db["Country"].isin(input.filter1())
        indx_loc = db["Location"].isin(input.filter2())
        indx_cap = db["Location"].isin(input.filter3())
        indx_tec = db["Location"].isin(input.filter4())
        indx_pla = db[filters[-1]].isin(input.filter5())
        
        sub_db = db[indx_cou & indx_loc & indx_cap & indx_tec & indx_pla]

        return sub_db

app = App(app_ui, server)