from shiny import App, render, ui, reactive
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("C:/Users/Lenovo/Documents/GitHub/student30538/DAP-II-Final-project-Polio-trends-/final_polio_vis_data.csv")

# UI setup
app_ui = ui.page_fluid(
    ui.input_select(id = 'country', label = 'Choose a country:',
    choices = data['country_name'].unique().tolist()),
    ui.input_radio_buttons(id = 'outcome', label = 'Choose an outcome:', choices = ["Immunisation Percentage", "Estimated Polio Cases", "Defecation Rate"]),
    ui.output_plot('ts'),
    ui.output_table("subsetted_data_table")
)

# Server setup
def server(input, output, session):
    @reactive.calc
    def full_data():
        return data

    @reactive.calc
    def subsetted_data():
        df = full_data()
        return df[df['country_name'] == input.country()]

    @render.table()
    def subsetted_data_table():
        return subsetted_data()

    @render.plot
    def ts():
        df = subsetted_data()
        if input.outcome() == "Immunisation Percentage":
            series = df['immunisation_percentage']
        elif input.outcome() == "Estimated Polio Cases":
            series = df['estimated_polio_cases']
        elif input.outcome() == "Defecation Rate":
            series = df['defecation_rate']
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(df['year'], series)
        ax.set_xlabel('Year')
        ax.set_ylabel(input.outcome())
        ax.set_title(f'{input.outcome()} in {input.country()}')
        return fig

# Create and run the app
app = App(app_ui, server)
app.run(port=8000)