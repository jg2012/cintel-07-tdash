import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

df = palmerpenguins.load_penguins()

ui.page_opts(title="Jose Guzman's Penguins Dashboard 🐧🐧🐧", fillable=True)

#Sidebar Menu 
with ui.sidebar(title="🐧Penguin controls"):
    #Slider for user to input Mass desired. 
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    #Checbox to allow user to check off the type of species. 
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/jg2012/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/jg2012/cintel-07-tdash/blob/main/app/app.py",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/jg2012/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    #Shows Number of Penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]
    #Shows Average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"
    #Shows Average bill depth  
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"



with ui.layout_columns():
    # Plots Bill Length and depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
                style="species",  # Add markers based on species
                markers=["o", "s", "D"]  # Specify markers for each species
            )
    # Data Table
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)



#ui.include_css(app_dir / "styles.css")

#Filters data and reacts to user input. 
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
