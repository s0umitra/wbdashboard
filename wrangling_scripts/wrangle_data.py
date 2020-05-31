import pandas as pd
import plotly.graph_objs as go


def cleandata(dataset, keepcolumns=['Country Name', '1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015'],
              value_variables=['1980', '1985', '1990', '1995', '2000', '2005', '2010', '2015']):
    
    df = pd.read_csv(dataset, skiprows=4)

    df = df[keepcolumns]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil',
                    'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]

    df_melt = df.melt(id_vars='Country Name', value_vars=value_variables)
    df_melt.columns = ['country', 'year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    return df_melt


def return_figures():

    graph_one = []
    df = cleandata('data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv')
    df.columns = ['country', 'year', 'hectaresarablelandperperson']


    countrylist = df.country.unique().tolist()

    df.sort_values(['year'], ascending=True, inplace=True)
    for country in countrylist:
        x_val = df[df['country'] == country].year.tolist()
        y_val = df[df['country'] == country].hectaresarablelandperperson.tolist()
        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines + markers',
                name=country
            )
        )
    layout_one = dict(title=dict(text='Change in Hectares Arable Land<br>per Person 1980 to 2015',),
                      xaxis=dict(title='Year',
                                 autotick=False, tick0=1980, dtick=5),
                      yaxis=dict(title='Hectares'),
                      )

    graph_two = []
    df = cleandata('data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv')
    df.columns = ['country', 'year', 'hectaresarablelandperperson']
    df.sort_values(['hectaresarablelandperperson'], ascending=False, inplace=True)
    df = df[df['year'] == 2015]

    graph_two.append(
        go.Bar(
            x=df.country.tolist(),
            y=df.hectaresarablelandperperson.tolist(),
        )
    )

    layout_two = dict(title='Hectares Arable Land per Person in 2015',
                      xaxis=dict(title='Country', ),
                      yaxis=dict(title='Hectares per person'),
                      )

    graph_three = []
    df = cleandata('data/API_SP.RUR.TOTL.ZS_DS2_en_csv_v2_9948275.csv')
    df.columns = ['country', 'year', 'percentrural']
    df.sort_values(['year'], ascending=True, inplace=True)

    for country in countrylist:
        x_val = df[df['country'] == country].year.tolist()
        y_val = df[df['country'] == country].percentrural.tolist()
        graph_three.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines + markers',
                name=country
            )
        )

    layout_three = dict(title='Change in Rural Population<br>(Percent of Total Population)',
                        xaxis=dict(title='Year',
                                   autotick=False, tick0=1980, dtick=5),
                        yaxis=dict(title='Percent'),
                        )

    graph_four = []

    valuevariables = [str(x) for x in range(1980, 2016)]
    keepcolumns = [str(x) for x in range(1980, 2016)]
    keepcolumns.insert(0, 'Country Name')

    df_one = cleandata('data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv', keepcolumns, valuevariables)
    df_two = cleandata('data/API_AG.LND.FRST.K2_DS2_en_csv_v2_9910393.csv', keepcolumns, valuevariables)

    df_one.columns = ['country', 'year', 'variable']
    df_two.columns = ['country', 'year', 'variable']

    df = df_one.merge(df_two, on=['country', 'year'])

    for country in countrylist:
        x_val = df[df['country'] == country].variable_x.tolist()
        y_val = df[df['country'] == country].variable_y.tolist()
        year = df[df['country'] == country].year.tolist()
        country_label = df[df['country'] == country].country.tolist()

        text = []
        for country, year in zip(country_label, year):
            text.append(str(country) + ' ' + str(year))

        graph_four.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='markers',
                text=text,
                name=country,
                textposition='top'
            )
        )

    layout_four = dict(title='Rural Population versus<br>Forested Area (Square Km) 1990-2015',
                       xaxis=dict(title='Rural Population'),
                       yaxis=dict(title='Forest Area (square km)'),
                       )

    graph_five = []
    df_five = cleandata('data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv', ['Country Name', '2015'], ['2015'])

    df_five.columns = ['country', 'year', 'ruralpopulation']
    df_five.sort_values(['year'], ascending=True, inplace=True)

    graph_five.append(
        go.Bar(
            x=df_five.country.tolist(),
            y=df_five.ruralpopulation.tolist(),
        )
    )

    layout_five = dict(title='Rural Population in 2015',
                       xaxis=dict(title='Country', ),
                       yaxis=dict(title='Rural Population',))

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures
