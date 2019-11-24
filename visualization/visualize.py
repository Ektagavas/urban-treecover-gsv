import plotly.express as px

token = "" # put your own mapbox token here

def show_map(data):
    fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_data=["greenery"],
                            color_discrete_sequence=["fuchsia"], size='greenery', zoom=19, height=300)
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker=dict(color='#00e054'))
    fig.show()