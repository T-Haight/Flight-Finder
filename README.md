# Gradio Flight App

This project is a Gradio application that allows users to search for flights based on their input parameters. It utilizes the Playwright library to interact with flight search websites and retrieve the cheapest flight options.

## Project Structure

```
gradio-flight-app
├── src
│   ├── flight_PW.py       # Contains the flight search functionality using Playwright
│   └── app.py          # Gradio app implementation for user interface
├── requirements.txt     # Lists the dependencies required for the project
└── README.md            # Documentation for the project
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd gradio-flight-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Running the Application

To run the Gradio app, execute the following command:

```
python src/app.py
```

This will start the Gradio interface in your web browser.

## Usage

1. Enter the departure airport code (e.g., "cmh").
2. Enter the destination airport code (e.g., "sxm").
3. Select the departure date and return date.
4. Enter the max amount of total time (hours) that you are willing to travel per trip.  
5. Click the "Search" button to find the cheapest flight.

The app will display the results, including the cheapest nonstop or 1-stop flight, along with their details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.
