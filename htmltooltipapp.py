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
De kaarten tonen de percentages (**TODO**: Dynamisch maken voor kosten) van de volwassenen (19 jaar en ouder) die {uitkomstmaat} hebben per regio. Hoe hoger het percentage, hoe meer volwassen {uitkomstmaat} hebben, hoe roder de regio kleurt. Grijze regio’s verschillen niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld heeft **TODO**% van de Nederlanders {uitkomstmaat} voor correctie en **TODO**% na correctie.
''')
col1.write(f'Voor correctie')
col1.pyplot(fig1)
col2.write(f'Na correctie')
col2.pyplot(fig2)




'''### Bronverantwoording
(Uitvouwding naar pagina met uitleg en categorisering, bron etc per variabele en uitkomstmaat)
'''




############# A MESS, BUT A MESS WITH TOOLTIPS!!!!!!!!!

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
from mpld3 import plugins

# Define some CSS to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""

fig, ax = plt.subplots()
ax.grid(True, alpha=0.3)

N = 50
df = pd.DataFrame(index=range(N))
df['x'] = np.random.randn(N)
df['y'] = np.random.randn(N)
df['z'] = np.random.randn(N)

# st.write(gdf.iloc[[0], :].T)



# st.write(labels)

labels = []
for i in range(N):
    label = df.iloc[[i], :].T
    label.columns = ['Row {0}'.format(i)]
    # .to_html() is unicode; so make leading 'u' go away with str()
    labels.append(str(label.to_html()))


points = ax.plot(df.x, df.y, 'o', color='b',
                 mec='k', ms=15, mew=1, alpha=.6)

st.write(ax2)


ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('HTML tooltips', size=20)

tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                   voffset=10, hoffset=10, css=css)
plugins.connect(fig, tooltip)

# mpld3.show()

import streamlit.components.v1 as components

def mpld3_static(fig: plt.Figure, height=500, width=700, **mpld3_kwargs):
    return components.html(mpld3.fig_to_html(fig, **mpld3_kwargs), height=height, width=width)

mpld3_static(fig)






labels = []
labeldf = gdf[['ggd_regio', 'verschil_M1']].copy()
for i in range(gdf.shape[0]):
  label = labeldf.iloc[[i], :].T
  label.columns = [f'Row {i}']
  # .to_html() is unicode; so make leading 'u' go away with str()
  labels.append(str(label.to_html()))

# # alternatively
# labels = [f'verschil {v}' for v in gdf['verschil_M1']]

tooltip = plugins.PointHTMLTooltip(ax1, labels,
                                   voffset=10, hoffset=10, css=css)
plugins.connect(fig1, tooltip)

mpld3_static(fig1)







import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins
fig, ax = plt.subplots()
points = ax.plot(range(10), 'o')
plugins.connect(fig, plugins.MousePosition())
# fig_to_html(fig)
mpld3_static(fig)