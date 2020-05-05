from bs4 import BeautifulSoup
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import json


"""Check CRAN site"""
names_cran = []
url = "https://cran.r-project.org/web/packages/available_packages_by_name.html"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, "html.parser")

for a in soup.find_all('a', href=True):
    try:
        names_cran.append(a.get('href').split('/')[-2])
    except IndexError:
        None


"""Check Bioconductor site"""
names_bio = []
packages = requests.get('https://www.bioconductor.org/packages/json/3.11/bioc/packages.js')
packages = packages.text
packages = packages.split('var bioc_packages = ')[-1][:-1]
packages = json.loads(packages).get('content')

for package in packages:
    names_bio.append(package[0])


"""Combine to one list"""
names_bio = [x.lower() for x in names_bio]
names_cran = [x.lower() for x in names_cran]
names = list(set(names_bio) | set(names_cran))


"""Setup DASH"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1(
            children="CRAN and Bioconductor package name checker",
        ),

        dcc.Input(
            id="package_name",
            type="text",
            value="package_name",
        ),

        html.Div(
            id='output_div'
        )

    ],
    style={'textAlign': 'center'}
)

@app.callback(Output('output_div', 'children'),
              [Input('package_name', 'value')],
              )
def update_output_div(input_value):
    input_value_lc = input_value.lower()
    if input_value_lc in names:
        return f"{input_value} is already a named package on CRAN or Bioconductor"
    else:
        return f"{input_value} is available as a package name"


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)