# DNA Expense Data Visualization UI (User Interface) App

## Overview
#### This repository contains a Dash-based web application for visualizing DNA-related expenses across different departments, such as Biop, QC, and Operations. The app allows users to interactively explore spending data on Reagents, Consumables, and Equipment by selecting different expense categories and departments. The visualizations are created using Plotly for dynamic and intuitive data insights.

## vFeatures
- Interactive Dropdowns: Users can select different expense categories and departments to generate custom visualizations.
- Bar Chart Visualization: Displays expense data categorized by spending category and department using a grouped bar chart.
- Dynamic Filtering: The app updates the plot in real-time based on user input from the dropdown menus.

## Application Structure
* app.py: Main application script. It contains the layout and functionality for rendering the expense data visualization.

* Loads and processes spending data.
Creates an interactive dropdown for expense categories.
Generates a grouped bar chart showing expenses across departments.
Data (example dataset):

* Categories: Reagents, Consumables, Equipment.
Departments: Biop, QC, Operations.
Spending Data: Displays the corresponding expenses for each department and category.
