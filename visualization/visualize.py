import plotly.express as px
from plotly.offline import iplot

token = '' # You should put your token here
px.set_mapbox_access_token(token)

def show_map(data, col):
    fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_data=[col],
                            color_discrete_sequence=["fuchsia"], size=col, zoom=15, height=500)
    fig.update_layout(mapbox_style="dark")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker=dict(color='#00e054'))
    iplot(fig)