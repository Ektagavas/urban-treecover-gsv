import plotly.express as px
from plotly.offline import iplot

token = 'pk.eyJ1IjoiZWt0YWdhdmFzIiwiYSI6ImNrM2EyNWt6NjAzeHozY28xMWN2a3FxcGUifQ.2n6gJ2YjG_0TUF_MrcQrjg' # You should put your token here
px.set_mapbox_access_token(token)

def show_map(data, col):
    """
    Visualize green, urban and water cover using mapbox api
    Arguments:
    data: Dataframe of results of detected cover (in percent)
    col: column name of dataframe to plot ('greenery' or 'water' or 'urban')
    """
    
    fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_data=[col],
                            color_discrete_sequence=["fuchsia"], size=col, zoom=15, height=500)
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker=dict(color='#00e054'))
    iplot(fig)