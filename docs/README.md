# Streamlit Cash Flow Waterfall Project

This project is a Streamlit application that visualizes cash flow data using a waterfall chart. It allows users to filter the data based on cash category classifications (such as Financing and Operational) and detailed categories (like Revenues, debts, credit card, etc.). The application provides an interactive interface for analyzing cash flow trends.

## Project Structure

```
streamlit-cashflow-waterfall
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   └── utils.py        # Utility functions for data processing
├── data
│   └── cashflow.csv    # CSV file containing cash flow data
├── requirements.txt     # List of dependencies for the project
└── README.md            # Documentation for the project
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd streamlit-cashflow-waterfall
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run src/app.py
```

This will start the Streamlit server and open the application in your default web browser.

## Features

- **Waterfall Chart Visualization**: Displays cash flow data in a waterfall format, allowing users to see how different categories contribute to the overall cash flow.
- **Filters**: Users can filter the data by cash category classifications (Financing, Operational) and detailed categories (Revenues, debts, credit card, etc.).
- **Dynamic Table**: A table that updates according to the applied filters, providing detailed insights into the cash flow data.

## Data Source

The cash flow data is stored in `data/cashflow.csv`. Ensure that this file is properly formatted and contains the necessary categories for the application to function correctly.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.