import altair as alt
import geopandas
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

COLORSCHEME = 'redblue'

UITKOMSTMAAT_MAP = {'Alg_gez_0goed_1slecht': 'minder goed ervaren gezondheid',
'Chron_ziekte_0_nee': 'één of meer chronische ziekten',
'Hoog_Risico_Depr': 'hoog risico op angststoornis of depressie',
'TotaleZorgkosten': 'totale zorgkosten in de basisverzekering',
'nopzvwkhuisartsconsult': 'huisarts consult kosten',
'GGZkosten': 'geestelijke gezondheidszorg kosten',
'zvwkfarmacie': 'farmacie kosten',
'zvwkziekenhuis': 'medisch specialistische zorg kosten'}





################ LOAD MAIN DATASETS #####################

### GEODATA
# why topojson: # https://github.com/streamlit/streamlit/issues/1002
ggd_regios = alt.topo_feature(
    "https://raw.githubusercontent.com/NHameleers/regionale_verschillen_st/main/ggd_regios.topojson",
    "ggd_regios",
)

### ANALYSIS DATA
df = pd.read_csv('final_input_voor_tool.csv')
df['uitkomstmaat'] = df['uitkomstmaat'].replace(UITKOMSTMAAT_MAP)

### NL GEMIDDELDEN VAN UITKOMSTMATEN
nl_df = pd.read_csv('NL_gemiddelden.csv')

#########################################################






################### START FRONT END #####################

'# Regionale gezondheidsverschillen'

### USER INPUT
uitkomstmaat = st.sidebar.selectbox('Selecteer de gewenste uitkomstmaat:', df.uitkomstmaat.unique(), format_func=str.capitalize)
ref_regio = st.sidebar.selectbox('Selecteer de referentie regio:', df.ggd_regio.unique())

f"""## {uitkomstmaat.capitalize()} per GGD regio, ten opzichte van {ref_regio}."""

##########################################################







########################### DATA PREP #####################

# save nl gemiddelde voor leeswijzer
nl_df['uitkomstmaat'] = nl_df['uitkomstmaat'].replace(UITKOMSTMAAT_MAP)
nl_gemiddelde = nl_df.loc[nl_df.uitkomstmaat == uitkomstmaat, 'gemiddelde'].values[0]

# units die bij uitkomstmaat passen
if ('kosten' in uitkomstmaat) or ('zvwk' in uitkomstmaat):
    df['verschil'] = df['verschil'].round()
    unit = '€'
else:
    df['verschil'] = (df['verschil'] * 100).round(1)
    unit = 'procentpunt'

# selectie uit df om te plotten
verschil_M1 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 1), ['ggd_regio', 'verschil']].copy()
verschil_M1 = verschil_M1.rename(columns={'verschil': 'verschil_M1',
'ggd_regio': 'statnaam'})

verschil_M6 = df.loc[(df.uitkomstmaat == uitkomstmaat) & (df.referentie_regio == ref_regio) & (df.model == 6), ['ggd_regio', 'verschil']].copy()
verschil_M6 = verschil_M6.rename(columns={'verschil': 'verschil_M6',
'ggd_regio': 'statnaam'})

##############################################################








##################### PLOTTING ###############################
# de legenda van de plots moet het verste punt van 0 aanhouden per uitkomstmaat, onafhankelijk van ref regio.
legendmax = df.loc[(df.uitkomstmaat == uitkomstmaat), 'verschil'].abs().max()
# domein is reversed om colorscheme goed weer te geven
full_domain_reversed = [legendmax, -legendmax]

tooltip_text = f"Verschil met {ref_regio} (in {unit})"
legend_title = f"Verschil met {ref_regio} (in {unit}), vóór correctie (linkse kaart) en ná correctie (rechtse kaart)."

# model 1 (voor correctie)
m1 = (
    alt.Chart(ggd_regios)
    .mark_geoshape(stroke="white", strokeWidth=1)
    .encode(
        color=alt.condition(alt.datum.verschil_M1 != 0,
        alt.Color("verschil_M1:Q", scale=alt.Scale(scheme=COLORSCHEME, domain=full_domain_reversed), legend=alt.Legend(title=legend_title, orient='bottom')),
        alt.value('lightgray'),
        legend=None),
        tooltip=[
            alt.Tooltip("properties.statnaam:O", title="GGD regio"),
            alt.Tooltip("verschil_M1:Q", title=tooltip_text),
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

# model 6 (na correctie)
verschil_M6['ref_regio'] = verschil_M6['statnaam'] == ref_regio
m6 = (
    alt.Chart(ggd_regios)
    .mark_geoshape(stroke="white", strokeWidth=1)
    .encode(
        color=alt.condition(alt.datum.verschil_M6 != 0,
        alt.Color("verschil_M6:Q", scale=alt.Scale(scheme=COLORSCHEME, domain=full_domain_reversed), legend=alt.Legend(title=legend_title, orient='bottom')),
        alt.value('lightgray'),
        legend=None),
        tooltip=[
            alt.Tooltip("properties.statnaam:O", title="GGD regio"),
            alt.Tooltip("verschil_M6:Q", title=tooltip_text),
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

# kaarten naast elkaar
out2 = (m1 | m6).configure_legend(
    gradientLength=800,
    gradientThickness=30,
    padding=10,
    titleLimit=1100,
    titleFontSize=16
) 
# https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html#altair.Chart.configure_legend

st.altair_chart(out2, use_container_width=True)

##############################################################






######################## LEESWIJZER ##########################
leeswijzer = ''
if 'kosten' in uitkomstmaat.lower():
    leeswijzer = f'''De kaarten tonen per GGD regio het verschil met de gekozen referentie regio ({ref_regio}) in gemiddelde {uitkomstmaat} per volwassene (19 jaar en ouder). Wanneer de gemiddelde {uitkomstmaat} per volwassene in een GGD regio hoger zijn dan in de referentie regio ({ref_regio}), dan kleurt de regio rood. Zijn de gemiddelde {uitkomstmaat} lager, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio's verschillen niet met de gekozen referentie regio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld zijn de {uitkomstmaat} in Nederland €{nl_gemiddelde:.00f} per volwassene.'''
else:
    leeswijzer = f'''### Leeswijzer
De kaarten tonen per GGD regio het verschil met de gekozen referentie regio ({ref_regio}) in percentage van de volwassenen (19 jaar en ouder) die {uitkomstmaat} hebben. Wanneer meer volwassenen in een GGD regio {uitkomstmaat} hebben dan in {ref_regio}, dan kleurt de regio rood. Hebben minder volwassenen {uitkomstmaat}, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio’s verschillen niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. Gemiddeld heeft {nl_gemiddelde:.1f}% van de Nederlanders {uitkomstmaat}.
'''

st.write(leeswijzer)

lw_sidebar = st.sidebar.checkbox('Toon leeswijzer hier')
if lw_sidebar:
    st.sidebar.write(leeswijzer)
###############################################################






################## BRONVERANTWOORDING IN SIDEBAR #############

show_bv = st.sidebar.checkbox('Toon bronverantwoording')
if show_bv:
    st.sidebar.write('(Hier komt dan een stuk met uitleg en categorisering, bron etc per variabele en uitkomstmaat)')

#############################################################

