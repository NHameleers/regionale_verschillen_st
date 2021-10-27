import geopandas
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")


cmap = plt.cm.coolwarm  # define the colormap
# extract all colors from the colormap
cmaplist = [cmap(i) for i in range(cmap.N)]
indices = [int(i) for i in np.linspace(0, len(cmaplist)-1, 7)]
newmapcolors = [cmaplist[i] for i in indices]
binnedcmap = colors.ListedColormap(newmapcolors)

beschrijving_uitkomstmaat = {'Gezondheid Algemeen': f'Percentage volwassenen (19 jaar en ouder) die een minder goede gezondheid ervaren',
'TotaleZorgkosten': 'totale zorgkosten in basisverzekering',
'nopzvwkhuisartsconsult': 'Kosten huisarts consult basisverzekering',
'GGZkosten': 'Kosten GGZ basisverzekering',
'zvwkziekenhuis': 'Kosten medisch-specialistische zorg basisverzekering',
'zvwkfarmacie': 'Kosten farmacie basisverzekering'}



# ggd_topo = alt.topo_feature('ggd_regios.geojson', 'features')


### GEO DATA
gdf_raw = (geopandas.read_file("ggd_regios.shp").rename(columns={'statnaam': 'ggd_regio'}))

# 'GDF raw'
# st.write(gdf_raw)



### ANALYSIS DATA
df = pd.read_csv('final_input_voor_tool.csv')

# 'DF'
# st.write(df.head())


'# Regionale gezondheidsverschillen'


### USER INPUT
uitkomstmaat = st.selectbox('Selecteer Uitkomstmaat:', df.uitkomstmaat.unique())
ref_regio = st.selectbox('Selecteer referentie GGD regio:', df.ggd_regio.unique())



### DATA FOR PLOTTING PREPARATION BASED ON INPUTS
verschil_M1 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 1), ['ggd_regio', 'verschil']].copy()
verschil_M1 = verschil_M1.rename(columns={'verschil': 'verschil_M1'})

verschil_M6 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 6), ['ggd_regio', 'verschil']].copy()
verschil_M6 = verschil_M6.rename(columns={'verschil': 'verschil_M6'})

gdf = gdf_raw.merge(verschil_M1, on='ggd_regio', how='left').merge(verschil_M6, on='ggd_regio', how='left')


# st.write([reg for reg in df.ggd_regio if reg not in gdf.ggd_regio])
# 'GDF'
# st.write(gdf)


if 'kosten' not in uitkomstmaat.lower():
    titeltekst = f"### {uitkomstmaat} per regio, ten opzichte van {ref_regio}."
elif 'kosten' in uitkomstmaat.lower():
    titeltekst = f"### Marginale {uitkomstmaat} in euro's per regio, ten opzichte van {ref_regio}."

st.write(titeltekst)


### PLOTTING

# Center of colormap should be zero
divnorm=colors.TwoSlopeNorm(vmin=df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].min(), vcenter=0, vmax=df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].max())

fig1, ax1 = plt.subplots(figsize=(6,6))

divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size="5%", pad=0.1)

ax1 = gdf.plot(column='verschil_M1',
                ax=ax1,
                cmap=binnedcmap,
                legend=True,
                cax=cax1,
                legend_kwds={'label': f'Verschil {uitkomstmaat}\n met regio: {ref_regio}',
                            'orientation': "horizontal"},
                norm=divnorm,
                edgecolor="black",
                linewidth=.2)
ax1.set_axis_off()
# fig1.set_facecolor('black')


fig2, ax2 = plt.subplots(figsize=(6,6))
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size="5%", pad=0.1)

ax2 = gdf.plot(column='verschil_M6',
                ax=ax2,
                cmap=binnedcmap,
                legend=True,
                cax=cax2,
                legend_kwds={'label': f'Verschil {uitkomstmaat}\nmet regio: {ref_regio}',
                            'orientation': "horizontal"},
                norm=divnorm,
                edgecolor="black",
                linewidth=.2)
ax2.set_axis_off()
# fig2.set_facecolor('black')


# '## Hieronder 2 figuren, blabla'
# '## Links zonder correctie, rechts na (met?) correctie voor demografie, SES, eenzaamheid, leefstijl, ervaren gezondheid etc (TODO)'

col1, col2, col3 = st.columns((1, 1, 2))
col3.write(f'''### Leeswijzer
De kaarten tonen de percentages (**TODO**: Dynamisch maken voor kosten) van de volwassenen (19 jaar en ouder) die {uitkomstmaat} hebben per regio. Hoe hoger het percentage, hoe meer volwassen {uitkomstmaat} hebben, hoe roder de regio kleurt. Grijze regio's verschillen niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld heeft **TODO**% van de Nederlanders {uitkomstmaat} voor correctie en **TODO**% na correctie.
''')
col1.write(f'Voor correctie')
col1.pyplot(fig1)
col2.write(f'Na correctie')
col2.pyplot(fig2)




'''### Bronverantwoording
(Uitvouwding naar pagina met uitleg en categorisering, bron etc per variabele en uitkomstmaat)
'''


import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure# Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson = gdf.to_json())

# # Create figure object.
# p = figure(title = 'Lead Levels in Water Samples, 2018', 
#            plot_height = 600 ,
#            plot_width = 950, 
#            toolbar_location = 'below',
#            tools = "pan, wheel_zoom, box_zoom, reset")
# p.xgrid.grid_line_color = None
# p.ygrid.grid_line_color = None
# # Add patch renderer to figure.
# states = p.patches('xs','ys', source = geosource,
#                    fill_color = None,
#                    line_color = 'gray', 
#                    line_width = 0.25, 
#                    fill_alpha = 1)
# # Create hover tool
# p.add_tools(HoverTool(renderers = [states],
#                       tooltips = [('Regio','@ggd_regio'),
#                                 ('Verschil','@verschil_M1')]))



# Define color palettes
palette = ['#3b4cc0', '#6f92f3', '#aac7fd', '#dcdddd', '#f7b89c', '#e8765c', '#b40426']
# palette = palette[::-1] # reverse order of colors so higher values have darker colors# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].min(), high = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].max())# Define custom tick labels for color bar.
tick_labels = {'0': '0', '5000000': '5,000,000',
 '10000000':'10,000,000', '15000000':'15,000,000',
 '20000000':'20,000,000', '25000000':'25,000,000',
 '30000000':'30,000,000', '35000000':'35,000,000',
 '40000000':'40,000,000+'}# Create color bar.
color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal')
                     # ,
                     # major_label_overrides = tick_labels)# Create figure object.
p = figure(title = 'Voor correctie', 
           plot_height = 600 ,
           plot_width = 470, 
           toolbar_location = 'below',
           tools = "wheel_zoom, reset")
p.axis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs','ys', source = geosource,
                   fill_color = {'field': 'verschil_M1', 'transform': color_mapper},
                   line_color = 'gray', 
                   line_width = 0.25, 
                   fill_alpha = 1)
# Create hover tool
p.add_tools(HoverTool(renderers = [states],
                      tooltips = [('Regio','@ggd_regio'),
                                ('Verschil','@verschil_M1')]))
# p.add_layout(color_bar, 'below')show(p)

st.bokeh_chart(p)





geosource2 = GeoJSONDataSource(geojson = gdf.to_json())
# Define color palettes
palette = ['#3b4cc0', '#6f92f3', '#aac7fd', '#dcdddd', '#f7b89c', '#e8765c', '#b40426']
# palette = palette[::-1] # reverse order of colors so higher values have darker colors# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper2 = LinearColorMapper(palette = palette, low = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].min(), high = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].max())# Define custom tick labels for color bar.

p2 = figure(title = 'Na correctie', 
           plot_height = 600 ,
           plot_width = 470, 
           toolbar_location = 'below',
           tools = "wheel_zoom, reset")
p2.axis.visible = False
p2.xgrid.grid_line_color = None
p2.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p2.patches('xs','ys', source = geosource2,
                   fill_color = {'field': 'verschil_M6', 'transform': color_mapper2},
                   line_color = 'gray', 
                   line_width = 0.25, 
                   fill_alpha = 1)
# Create hover tool
p2.add_tools(HoverTool(renderers = [states],
                      tooltips = [('Regio','@ggd_regio'),
                                ('Verschil','@verschil_M6')]))
# p.add_layout(color_bar, 'below')show(p)

st.bokeh_chart(p2)

