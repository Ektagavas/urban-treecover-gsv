import pandas as pd
import plotly.express as px

token = "" # you will need your own token

fig = px.scatter_mapbox(data_df, lat="lat", lon="lon", hover_data=["gidx"],
                         color_discrete_sequence=["fuchsia"], size='gidx', zoom=18, height=300)
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(marker=dict(color='#00e054'))
fig.show()