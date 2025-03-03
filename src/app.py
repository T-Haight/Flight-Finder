from gradio import Interface
import gradio as gr
from flight_PW import run_flight_search

def flight_search(where_from, where_to, departure_date, return_date, max_time):
    results = run_flight_search(where_from, where_to, departure_date, return_date, max_time)
    return results

iface = Interface(
    fn=flight_search,
    inputs=[
        gr.Textbox(label="3-Letter Airport Code For Where You Are Flying From (eg. 'CMH')?"),
        gr.Textbox(label="3-Letter Airport Code For Where You Are Flying To? (eg. 'LAX')"),
        gr.Textbox(label="Departure Date (MM/DD/YYYY)"),
        gr.Textbox(label="Return Date (MM/DD/YYYY)"),
        gr.Number(label="Max Travel Duration (hours) willing to spend")
    ],
    outputs=[gr.Textbox(label="URL"), 
             gr.Textbox(label="Cheapest Flight Cost"), 
             gr.Textbox(label="Departure Airline"),
             gr.Textbox(label="Total Duration to Destination"),
             gr.Textbox(label="Departure Time"),
             gr.Textbox(label="Arrival Time"),
             gr.Textbox(label="Total Duration"),
             gr.Textbox(label="Return Airline"),
             gr.Textbox(label="Total Duration to Return"),
             gr.Textbox(label="Departure Time"),
             gr.Textbox(label="Arrival Time")],
    title="Flight Search App",
    description="Enter your flight search details to find the cheapest flights."
)

if __name__ == "__main__":
    iface.launch()