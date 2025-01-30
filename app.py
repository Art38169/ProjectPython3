import os
import csv
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Add this line before importing pyplot
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from io import BytesIO
import base64
import requests

app = Flask(__name__)

# Directory where data files are stored
DATA_DIR = "data"


def load_data_from_file(year):
    """
    Load data from a CSV file based on the given year.
    Assumes the file is in the format `year.csv`.
    """
    file_path = os.path.join(DATA_DIR, f"{year}.csv")

    if not os.path.exists(file_path):
        return None, None  # File does not exist

    # Read the data from the CSV file
    data = []
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Get the header row with app names

        # Store the data rows (excluding the header)
        for row in reader:
            data.append(row)

    return np.array(data), header


@app.route("/")
def index():
    # List available years (this assumes you have files for each year like 2019.csv, 2020.csv, etc.)
    years = [f.split(".")[0] for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    return render_template("index.html", years=years)


@app.route("/select_apps", methods=["POST"])
def select_apps():
    year = request.form.get("year")
    data, header = load_data_from_file(year)
    if data is None:
        return f"Error: Data for {year} not found. Please upload the relevant file."

    # Extract the months from the data (first column)
    months = data[:, 0]

    # Prepare a list of apps to display dynamically
    apps = header[1:]  # Exclude the first column (Date)

    return render_template("select_apps.html", year=year, months=months, apps=apps)


@app.route("/generate_chart", methods=["POST"])
def generate_chart():
    year = request.form.get("year")
    selected_apps = request.form.getlist("apps")
    graph_type = request.form.get(
        "graph_type"
    )  # Get the selected graph type (bar/line)

    data, header = load_data_from_file(year)
    if data is None:
        return f"Error: Data for {year} not found. Please upload the relevant file."

    # Extract the months from the data (first column)
    months = data[:, 0]

    # Map selected apps to their corresponding column indices
    app_indices = [header.index(app) for app in selected_apps]

    # Prepare data for each selected app
    app_data = {app: [] for app in selected_apps}

    for row in data:
        for i, app in enumerate(selected_apps):
            app_index = app_indices[i]
            try:
                # Convert app percentage data to float
                app_data[app].append(float(row[app_index]))
            except ValueError:
                app_data[app].append(0)  # Handle any invalid data gracefully

    prompt = f"Generate two sentences analysis from the following rate usage application data (in percentage, January - December): {app_data} for the year {year}. Please be concise and to the point. Please include only text, no markdown or html syntax."
    print(prompt)

    api_key = "SG_3be07b4d8a88f075"
    url = "https://api.segmind.com/v1/deepseek-chat"

    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    }

    response = requests.post(url, json=data, headers={"x-api-key": api_key})
    analysis = response.json()["choices"][0]["message"]["content"]
    print(analysis)

    # Generate the chart based on the selected graph type
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(months))

    if graph_type == "bar":
        # Plot bars for each app
        bar_width = 0.15
        for i, app in enumerate(selected_apps):
            ax.bar(x + i * bar_width, app_data[app], width=bar_width, label=app)

    elif graph_type == "line":
        # Plot lines for each app
        for i, app in enumerate(selected_apps):
            ax.plot(x, app_data[app], label=app, marker="o")

    # Customize the plot
    ax.set_xlabel("Months")
    ax.set_ylabel("Percentage of Users")
    ax.set_title(f"App Usage in {year} in Thailand")
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()

    # Save the plot to a BytesIO object and convert to base64
    img_io = BytesIO()
    fig.savefig(img_io, format="png", bbox_inches="tight")
    img_io.seek(0)
    img_data = base64.b64encode(img_io.getvalue()).decode()

    plt.close(fig)  # Close the figure to free memory

    return render_template(
        "chart.html",
        year=year,
        img_data=img_data,
        selected_apps=selected_apps,
        graph_type=graph_type,
        analysis=analysis,
    )


if __name__ == "__main__":
    app.run(debug=True)
