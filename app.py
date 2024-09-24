import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Create a larger default dataset (500 data points)
np.random.seed(42)  # For reproducibility

categories = ['Reagents', 'Consumables', 'Equipment']
departments = ['Biop', 'QC', 'Operations']

# Generate random data
default_data = {
    'Expense Category': np.random.choice(categories, 1000),
    'Department': np.random.choice(departments, 1000),
    'Amount': np.random.randint(500, 5000, 1000)  # Random amounts between 500 and 5000
}

# Convert to DataFrame
df_default = pd.DataFrame(default_data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("DNA-related Expense Data Visualization"),

    # File Upload Section
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Button('Browse...'),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'marginBottom': '20px',  # Adjust margin for spacing
            },
            multiple=False  # Only allow a single file upload
        ),
        html.Div([
            html.Button('Upload User Data', id='upload-button', n_clicks=0, style={'margin': '10px'}),
            html.Button('Use Default Dataset', id='default-button', n_clicks=0, style={'margin': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        html.Div(id='output-data-upload', style={'marginTop': '10px'}),
    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top'}),

    # Sidebar for inputs
    html.Div([
        html.Label('Which expense category would you like to plot?'),
        dcc.Dropdown(
            id='expense-category-dropdown',
            options=[],
            value='Reagents'  # Default value
        ),

        html.Br(),  # Add spacing between dropdowns

        html.Label('Which department would you like to facet by?'),
        dcc.Dropdown(
            id='department-dropdown',
            options=[],
            value='Biop'  # Default value
        ),
        
        html.Br(),  # Add spacing between dropdown and slider

        html.Label('Number of Bins'),
        dcc.Slider(
            id='bins-slider',
            min=5,
            max=50,
            value=20,
            marks={i: str(i) for i in range(5, 51, 5)}
        ),
        
        html.Br(),  # Add spacing for the Update button

        html.Button('Update Plots', id='update-plots', n_clicks=0, style={'marginTop': '10px'})
    ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'paddingLeft': '20px'}),

    # Plots and Summaries
    html.Div([
        html.H3("Summaries"),
        html.Div(id='summary-table'),

        html.H3("Boxplot"),
        dcc.Graph(id='boxplot'),

        html.H3("Histogram"),
        dcc.Graph(id='histogram')
    ], style={'width': '65%', 'display': 'inline-block', 'padding-left': '5%'})
])

# Helper function to parse uploaded file
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = io.StringIO(io.BytesIO(base64.b64decode(content_string)).read().decode('utf-8'))
    return pd.read_csv(decoded)

# Callback to handle file upload and default dataset selection
@app.callback(
    [Output('expense-category-dropdown', 'options'),
     Output('department-dropdown', 'options'),
     Output('output-data-upload', 'children')],
    [Input('upload-button', 'n_clicks'),
     Input('default-button', 'n_clicks')],
    [State('upload-data', 'contents')]
)
def update_data(upload_clicks, default_clicks, uploaded_file):
    ctx = dash.callback_context

    # Check which button was clicked (upload or default)
    if not ctx.triggered:
        return [], [], "No data selected."
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'upload-button' and uploaded_file is not None:
        # Parse uploaded file
        df_uploaded = parse_contents(uploaded_file)

        # Update dropdowns based on the uploaded data
        expense_options = [{'label': col, 'value': col} for col in df_uploaded['Expense Category'].unique()]
        department_options = [{'label': dep, 'value': dep} for dep in df_uploaded['Department'].unique()]
        
        return expense_options, department_options, "User data uploaded successfully."
    
    elif button_id == 'default-button':
        # Use the default dataset
        expense_options = [{'label': cat, 'value': cat} for cat in df_default['Expense Category'].unique()]
        department_options = [{'label': dep, 'value': dep} for dep in df_default['Department'].unique()]
        
        return expense_options, department_options, "Default dataset loaded successfully."

    return [], [], "No data selected."

# Callback to update the plots and summary table
@app.callback(
    [Output('boxplot', 'figure'),
     Output('histogram', 'figure'),
     Output('summary-table', 'children')],
    [Input('expense-category-dropdown', 'value'),
     Input('department-dropdown', 'value'),
     Input('bins-slider', 'value')]
)
def update_plots(expense_category, department, bins):
    # Filter data based on selected expense category and department
    filtered_df = df_default[(df_default['Expense Category'] == expense_category) & (df_default['Department'] == department)]
    
    # If no data, return empty
    if filtered_df.empty:
        return {}, {}, "No data available for the selected category and department."

    # Create boxplot and histogram
    boxplot = px.box(filtered_df, y='Amount')
    histogram = px.histogram(filtered_df, x='Amount', nbins=bins)

    # Create summary table
    summary_stats = filtered_df['Amount'].describe().round(2)
    summary_table = html.Table([
        html.Tr([html.Th(col) for col in summary_stats.index]),
        html.Tr([html.Td(summary_stats[col]) for col in summary_stats.index])
    ])

    return boxplot, histogram, summary_table

if __name__ == '__main__':
    app.run_server(debug=True)
