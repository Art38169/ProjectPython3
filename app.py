import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from io import BytesIO

app = Flask(__name__)

# Directory where data files are stored
DATA_DIR = "data"

# Define a dictionary for app column indices (adjust as needed based on the CSV file structure)
app_columns = {
    "Facebook": 1,
    "Twitter": 2,
    "YouTube": 3,
    "Pinterest": 4,
    "VKontakte": 5,
    "Reddit": 6,
    "Instagram": 7,
    "LinkedIn": 8,
    "Tumblr": 9,
    "Other": 10
}

def load_data_from_file(year):
    """
    Load data from a CSV file based on the given year.
    Assumes the file is in the format `year.csv`.
    """
    file_path = os.path.join(DATA_DIR, f"{year}.csv")
    
    if not os.path.exists(file_path):
        return None  # File does not exist
    
    # Read the data from the CSV file, skipping the header
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        for row in reader:
            # Only store the row data after the header (excluding the 'Date' column)
            data.append(row)
    
    return np.array(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    year = request.form.get('year')
    
    data = load_data_from_file(year)
    if data is None:
        return f"Error: Data for {year} not found."
    
    # Get the selected apps
    selected_apps = request.form.getlist('apps')

    # Extract months and data for the selected apps
    months = data[:, 0]  # Get the months from the first column (Date column)
    app_data = {app: [] for app in selected_apps}

    for row in data:
        for app in selected_apps:
            app_index = app_columns.get(app)
            if app_index:
                try:
                    # Convert app percentage data to float
                    app_data[app].append(float(row[app_index]))
                except ValueError:
                    # Handle any data that can't be converted to float (e.g., empty cells)
                    app_data[app].append(0)

    # Generate the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.2
    x = np.arange(len(months))

    # Plot bars for each app
    for i, app in enumerate(selected_apps):
        ax.bar(x + i * bar_width, app_data[app], width=bar_width, label=app)

    # Customize the plot
    ax.set_xlabel('Months')
    ax.set_ylabel('Percentage of Users')
    ax.set_title(f'App Usage in {year} in Thailand')
    ax.set_xticks(x + (len(selected_apps) - 1) * bar_width / 2)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()

    # Save the plot to a BytesIO object and return it as an image
    img_io = BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

