import altair as alt
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
'TotaleZorgkosten': 'totale zorgkosten in de basisverzekering',
'nopzvwkhuisartsconsult': 'Kosten huisarts consult basisverzekering',
'GGZkosten': 'Kosten GGZ basisverzekering',
'zvwkziekenhuis': 'Kosten medisch-specialistische zorg basisverzekering',
'zvwkfarmacie': 'Kosten farmacie basisverzekering'}

uitkomstmaat_map = {'Alg_gez_0goed_1slecht': 'minder goed ervaren gezondheid',
'Chron_ziekte_0_nee': 'één of meer chronische ziekten',
'Hoog_Risico_Depr': 'hoog risico op angststoornis of depressie',
'TotaleZorgkosten': 'totale zorgkosten in de basisverzekering',
'nopzvwkhuisartsconsult': 'huisarts consult kosten',
'GGZkosten': 'geestelijke gezondheidszorg kosten',
'zvwkfarmacie': 'farmacie kosten',
'zvwkziekenhuis': 'medisch specialistische zorg kosten'}

# ggd_topo = alt.topo_feature('ggd_regios.geojson', 'features')


### GEO DATA
gdf_raw = (geopandas.read_file("ggd_regios.shp").rename(columns={'statnaam': 'ggd_regio'}))

# 'GDF raw'
# st.write(gdf_raw)



### ANALYSIS DATA
df = pd.read_csv('final_input_voor_tool.csv')
df['uitkomstmaat'] = df['uitkomstmaat'].replace(uitkomstmaat_map)
# 'DF'
# st.write(df.head())




'# Regionale gezondheidsverschillen'


### USER INPUT
uitkomstmaat = st.sidebar.selectbox('Selecteer de gewenste uitkomstmaat:', df.uitkomstmaat.unique())
ref_regio = st.sidebar.selectbox('Selecteer de referentie regio:', df.ggd_regio.unique())

# save nl gemiddelde voor leeswijzer
nl_df = pd.read_csv('NL_gemiddelden.csv')
nl_df['uitkomstmaat'] = nl_df['uitkomstmaat'].replace(uitkomstmaat_map)
nl_gemiddelde = nl_df.loc[nl_df.uitkomstmaat == uitkomstmaat, 'gemiddelde'].values[0]


if ('kosten' in uitkomstmaat) or ('zvwk' in uitkomstmaat):
    df['verschil'] = df['verschil'].round()
    unit = 'EUR'
else:
    df['verschil'] = (df['verschil'] * 100).round(1)
    unit = 'procentpunt'

### DATA FOR PLOTTING PREPARATION BASED ON INPUTS
verschil_M1 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 1), ['ggd_regio', 'verschil']].copy()
verschil_M1 = verschil_M1.rename(columns={'verschil': 'verschil_M1'})

verschil_M6 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 6), ['ggd_regio', 'verschil']].copy()
verschil_M6 = verschil_M6.rename(columns={'verschil': 'verschil_M6'})

gdf = gdf_raw.merge(verschil_M1, on='ggd_regio', how='left').merge(verschil_M6, on='ggd_regio', how='left')


# st.write([reg for reg in df.ggd_regio if reg not in gdf.ggd_regio])
# 'GDF'
# st.write(gdf)


titeltekst = f"""## {uitkomstmaat.capitalize()} per GGD regio, ten opzichte van {ref_regio}."""

st.write(titeltekst)










# https://github.com/streamlit/streamlit/issues/1002

colorscheme = 'redblue'

legendmax = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].abs().max()
legend_title = f"Verschil met {ref_regio} (in {unit})"
full_domain_reversed = [legendmax, -legendmax]

verschil_M1 = verschil_M1.rename(columns={'ggd_regio': 'statnaam'})
verschil_M6 = verschil_M6.rename(columns={'ggd_regio': 'statnaam'})

ggd_regios = alt.topo_feature(
        "https://raw.githubusercontent.com/NHameleers/regionale_verschillen_st/main/ggd_regios.topojson",
        "ggd_regios",
    )



m1 = (
    alt.Chart(ggd_regios)
    .mark_geoshape(stroke="white", strokeWidth=1)
    .encode(
        color=alt.condition(alt.datum.verschil_M1 != 0,
        alt.Color("verschil_M1:Q", scale=alt.Scale(scheme=colorscheme, domain=full_domain_reversed), legend=alt.Legend(title=legend_title, orient='bottom')),
        alt.value('lightgray'),
        legend=None),
        tooltip=[
            alt.Tooltip("properties.statnaam:O", title="GGD regio"),
            alt.Tooltip("verschil_M1:Q", title=legend_title),
        ],
    )
    .transform_lookup(
        lookup="properties.statnaam",
        from_=alt.LookupData(verschil_M1, "statnaam", ["verschil_M1"]),
    )
    .properties(
        width=400,
        height=440
    )
)
# st.altair_chart(m1)

verschil_M6['ref_regio'] = verschil_M6['statnaam'] == ref_regio
m6 = (
    alt.Chart(ggd_regios)
    .mark_geoshape(stroke="white", strokeWidth=1)
    .encode(
        color=alt.condition(alt.datum.verschil_M6 != 0,
        alt.Color("verschil_M6:Q", scale=alt.Scale(scheme=colorscheme, domain=full_domain_reversed), legend=alt.Legend(title=legend_title, orient='bottom')),
        alt.value('lightgray'),
        legend=None),
        tooltip=[
            alt.Tooltip("properties.statnaam:O", title="GGD regio"),
            alt.Tooltip("verschil_M6:Q", title=legend_title),
        ],
    )
    .transform_lookup(
        lookup="properties.statnaam",
        from_=alt.LookupData(verschil_M6, "statnaam", ["verschil_M6", "ref_regio"]),
    )
    .properties(
        width=400,
        height=440
    )
)
# st.altair_chart(m6)

out2 = (m1 | m6).configure_legend(
    gradientLength=800,
    gradientThickness=30,
    padding=10,
    titleLimit=400,
    titleFontSize=16
) 
# https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html#altair.Chart.configure_legend

st.altair_chart(out2, use_container_width=True)

if 'kosten' in uitkomstmaat.lower():
    f'''De kaarten tonen per GGD regio het verschil met de gekozen referentie regio ({ref_regio}) in gemiddelde {uitkomstmaat} per volwassene (19 jaar en ouder). Wanneer de gemiddelde {uitkomstmaat} per volwassene in een GGD regio hoger zijn dan in de referentie regio ({ref_regio}), dan kleurt de regio rood. Zijn de gemiddelde {uitkomstmaat} lager, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio's verschillen niet met de gekozen referentie regio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld zijn de {uitkomstmaat} in Nederland €{nl_gemiddelde:.00f} per volwassene.'''
else:
    st.write(f'''### Leeswijzer
De kaarten tonen per GGD regio het verschil met de gekozen referentie regio ({ref_regio}) in percentage van de volwassenen (19 jaar en ouder) die {uitkomstmaat} hebben. Wanneer meer volwassenen in een GGD regio {uitkomstmaat} hebben dan in {ref_regio}, dan kleurt de regio rood. Hebben minder volwassenen {uitkomstmaat}, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio’s verschillen niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld heeft {nl_gemiddelde:.1f}% van de Nederlanders {uitkomstmaat}.
''')

# col1, col2 = st.columns((2, 1))
# col1.altair_chart(out2, use_container_width=True)
# col2.write(f'''### Leeswijzer
# De kaarten tonen de percentages (**TODO**: Dynamisch maken voor kosten) van de volwassenen (19 jaar en ouder) die {uitkomstmaat} hebben per regio. Hoe hoger het percentage, hoe meer volwassen {uitkomstmaat} hebben, hoe roder de regio kleurt. Grijze regio’s verschillen niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld heeft **TODO**% van de Nederlanders {uitkomstmaat} voor correctie en **TODO**% na correctie.
# ''')


show_bv = st.sidebar.checkbox('Toon bronverantwoording')
if show_bv:
    st.sidebar.write('(Hier komt dan een stuk met uitleg en categorisering, bron etc per variabele en uitkomstmaat)')














# #########################
# m1 = (
#     alt.Chart(ggd_regios)
#     .mark_geoshape(stroke="white", strokeWidth=1)
#     .encode(
#         color=alt.condition(alt.datum.verschil_M1 != 0,
#         alt.Color("verschil_M1:Q", scale=alt.Scale(scheme=colorscheme, domain=full_domain)),
#         alt.value('lightgray'),
#         legend=None),
#         tooltip=[
#             alt.Tooltip("properties.statnaam:O", title="GGD regio"),
#             alt.Tooltip("verschil_M1:Q", title="Indicator value"),
#         ],
#     )
#     .transform_lookup(
#         lookup="properties.statnaam",
#         from_=alt.LookupData(verschil_M1, "statnaam", ["verschil_M1"]),
#     )
# )
# # st.altair_chart(m1)


# m6 = (
#     alt.Chart(ggd_regios)
#     .mark_geoshape(stroke="white", strokeWidth=1)
#     .encode(
#         color=alt.condition(alt.datum.verschil_M6 != 0,
#         alt.Color("verschil_M6:Q", scale=alt.Scale(scheme=colorscheme, domain=full_domain)),
#         alt.value('lightgray'),
#         legend=None),
#         tooltip=[
#             alt.Tooltip("properties.statnaam:O", title="GGD regio"),
#             alt.Tooltip("verschil_M6:Q", title="Indicator value"),
#         ],
#     )
#     .transform_lookup(
#         lookup="properties.statnaam",
#         from_=alt.LookupData(verschil_M6, "statnaam", ["verschil_M6"]),
#     )
# )
# # st.altair_chart(m6)

# out = m1 | m6
# st.altair_chart(out)
# # bovenstaande is eigenlijk al niet zo slecht, maar de legend heeft slechte grenzen en geen midpoint
