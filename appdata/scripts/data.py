import pandas as pd
import plotly.graph_objs as go
from collections import OrderedDict
import requests


def get_defaults():
    defaults_countries = [
        ('Canada', 'CAN'), ('United States', 'USA'), ('Brazil', 'BRA'), ('France', 'FRA'), ('India', 'IND'),
        ('Italy', 'ITA'), ('Germany', 'DEU'), ('United Kingdom', 'GBR'), ('China', 'CHN'), ('Japan', 'JPN'),
        ('South Asia', 'SAS'), ("Pakistan", "PAK"), ("New Zealand", "NZL"), ("Mexico", "MEX"), ("Switzerland", "CHE")
    ]

    return OrderedDict(defaults_countries)


def get_data_frame(countries):
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    indicators = ['AG.LND.ARBL.HA.PC', 'SP.RUR.TOTL.ZS', 'SP.RUR.TOTL.ZS', 'AG.LND.FRST.ZS']

    data_frames = []
    urls = []

    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/' \
              + country_filter \
              + '/indicators/' + indicator \
              + '?date=1980:2015&per_page=1000&format=json'

        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()[1]
        except:
            print('could not load data ', indicator)

        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        data_frames.append(data)

    return data_frames


def return_figures(countries=None):
    if not bool(countries):
        countries = get_defaults()

    df = get_data_frame(countries)

    # First Graph
    graph_one = []
    df_one = pd.DataFrame(df[0])

    countrylist = df_one.country.unique().tolist()
    df_one.sort_values(['date'], ascending=True, inplace=True)

    for country in countrylist:
        x_val = df_one[df_one['country'] == country].date.tolist()
        y_val = df_one[df_one['country'] == country].value.tolist()
        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country,
            )
        )

    layout_one = dict(title=dict(text='Change in Hectares Arable Land<br>per Person (1990 to 2015)',
                                 ),
                      xaxis=dict(title='Year',
                                 autotick=False, tick0=1980, dtick=5,
                                 ),
                      yaxis=dict(title='Hectares',)
                      )

    # Second Graph
    graph_two = []
    df_one.sort_values('value', ascending=False, inplace=True)
    df_one = df_one[df_one['date'] == '2015']

    graph_two.append(
        go.Bar(
            x=df_one.country.tolist(),
            y=df_one.value.tolist(),
            marker={'color': 'rgba(26, 118, 255, 0.5)',
                    'line': {
                        'color': 'rgb(8,48,107)',
                        'width': 1.5,
                    }
                    }
        )
    )

    layout_two = dict(title='Hectares Arable Land per Person in 2015',
                      xaxis=dict(title='Country', ),
                      yaxis=dict(title='Hectares per person'),
                      )

    # Third Graph
    graph_three = []
    df_three = pd.DataFrame(df[1])
    df_three.sort_values('date', ascending=True, inplace=True)

    for country in countrylist:
        x_val = df_three[df_three['country'] == country].date.tolist()
        y_val = df_three[df_three['country'] == country].value.tolist()
        graph_three.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_three = dict(title='Change in Rural Population<br>(Percent of Total Population)',
                        xaxis=dict(title='Year',
                                   autotick=False, tick0=1990, dtick=5),
                        yaxis=dict(title='Percent'),
                        )

    # Forth Graph
    graph_four = []
    df_four_a = pd.DataFrame(df[2])
    df_four_a = df_four_a[['country', 'date', 'value']]

    df_four_b = pd.DataFrame(df[3])
    df_four_b = df_four_b[['country', 'date', 'value']]

    df_four = df_four_a.merge(df_four_b, on=['country', 'date'])
    df_four.sort_values('date', ascending=True, inplace=True)

    for i, country in enumerate(countrylist):

        x_val = df_four[df_four['country'] == country].value_x.tolist()
        y_val = df_four[df_four['country'] == country].value_y.tolist()
        years = df_four[df_four['country'] == country].date.tolist()
        country_label = df_four[df_four['country'] == country].country.tolist()

        text = []
        for country, year in zip(country_label, years):
            text.append(str(country) + ' ' + str(year))

        graph_four.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines+markers',
                text=text,
                name=country,
            )
        )

    layout_four = dict(title='Rural Population versus<br>Forested Land (1990-2015)',
                       xaxis=dict(title='Rural Population Percentage', range=[0, 100], dtick=10),
                       yaxis=dict(title='Forest Area Percentage', range=[0, 100], dtick=10),
                       )

    # Fifth Graph
    graph_five = []

    df_five = pd.DataFrame(df[2])

    df_five.sort_values(['value'], ascending=True, inplace=True)
    df_five = df_five[df_five['date'] == '2015']

    graph_five.append(
        go.Bar(
            x=df_five.country.tolist(),
            y=df_five.value.tolist(),
        )
    )
    layout_five = dict(title='Rural Population in 2015',
                       xaxis=dict(title='Country', ),
                       yaxis=dict(title='Rural Population', ))

    # append all charts
    figures = list()
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures
