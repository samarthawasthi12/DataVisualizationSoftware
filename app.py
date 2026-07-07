from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

df = None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    global df

    file = request.files['file']

    if file:
        df = pd.read_csv(file)
        tables = df.to_html(classes='table table-bordered')

        return render_template(
            'dashboard.html',
            tables=tables,
            columns=df.columns
        )


@app.route('/chart', methods=['POST'])
def chart():

    global df

    chart_type = request.form['chart']
    x = request.form['x']
    y = request.form['y']

    if chart_type == "bar":
        fig = px.bar(df, x=x, y=y)

    elif chart_type == "line":
        fig = px.line(df, x=x, y=y)

    elif chart_type == "pie":
        fig = px.pie(df, names=x, values=y)

    elif chart_type == "scatter":
        fig = px.scatter(df, x=x, y=y)

    elif chart_type == "histogram":
        fig = px.histogram(df, x=x)

    graph = fig.to_html(full_html=False)

    return render_template("charts.html", graph=graph)


if __name__ == "__main__":
    app.run(debug=True)