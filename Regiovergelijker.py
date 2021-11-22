import altair as alt
import geopandas
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
from teksten import teksten
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














################### START FRONT END ######################


################## NAVIGATIE MET RADIO BUTTONS #############

radio_nav = st.sidebar.radio('', ['Home', 'Bronverantwoording'])

if radio_nav == 'Home':
    ################### START HOME PAGE #####################

    '# Regiovergelijker gezondheid en zorgkosten'



    #### INTRODUCTIE TEKST 
    '## Kunnen we regionale gezondheidsverschillen in Nederland verklaren?'
    st.write(teksten.introductie)


    ### USER INPUT
    regiolijst = sorted(df.ggd_regio.unique())
    st.sidebar.markdown('### Uitkomstmaat')
    uitkomstmaat = st.sidebar.selectbox('Selecteer de gewenste uitkomstmaat:', df.uitkomstmaat.unique(), format_func=str.capitalize)
    st.sidebar.markdown('### Referentie Regio')
    ref_regio = st.sidebar.selectbox('Selecteer de referentie regio:', regiolijst, index=23)


    st.sidebar.markdown("***")


    st.sidebar.caption(teksten.dankwoord)

    # TODO: add link to images: https://discuss.streamlit.io/t/how-can-i-add-a-url-link-to-an-image/13997
    c1, c2 = st.sidebar.columns(2)
    c1.image('https://academischewerkplaatslimburg.nl/wp-content/uploads/Logo_AW1.png',
    width=150)
    c2.image('https://www.maastrichtuniversity.nl/sites/default/files/styles/page_photo/public/logo_awdz_vierkant.jpg?itok=iaORmdsD',
    width=75)

    st.sidebar.markdown("***")

    st.sidebar.markdown('We horen graag uw ideeën of feedback over deze applicatie. [Mail ons](mailto:regiovergelijker@maastrichtuniversity.nl)')

    st.sidebar.markdown("***")

    st.sidebar.markdown('''Tenzij anders vermeld is alles in dit werk gelicenceerd onder een [CC-BY 4.0-licentie](https://creativecommons.org/licenses/by/4.0/deed.nl). Wanneer u gebruik wilt maken van dit werk, hanteer dan de volgende methode van naamsvermelding: 
    *"TODO allenamen (2021). Regiovergelijker gezondheid en zorgkosten. https://regiovergelijker.maastrichtuniversity.nl, Maastricht University 1 december 2021."*''')

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
    gezondheid_leeswijzers = {'minder goed ervaren gezondheid': f'''Gemiddeld ervaren {nl_gemiddelde:.1f}% van de Nederlanders een minder goede gezondheid. De kaarten tonen het verschil in het percentage van de volwassenen (19 jaar en ouder) die een minder goede gezondheid ervaren per GGD-regio, met de gekozen referentie regio ({ref_regio}). Wanneer meer volwassenen in een GGD-regio een minder goede gezondheid ervaren dan in {ref_regio} en dit verschil statistisch significant is, dan kleurt de regio rood. Ervaren meer volwassenen een goede gezondheid, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio’s verschillen (statistisch gezien) niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. ''',
    'één of meer chronische ziekten': f'''Gemiddeld heeft {nl_gemiddelde:.1f}% van de Nederlanders minimaal één chronische ziekte. De kaarten tonen het verschil in het percentage van de volwassenen (19 jaar en ouder) die minimaal één chronische ziekte hebben per GGD-regio, met de gekozen referentie regio ({ref_regio}). Wanneer meer volwassenen in een GGD-regio minimaal één chronische ziekte hebben dan in {ref_regio} en dit verschil statistisch significant is, dan kleurt de regio rood. Hebben minder volwassenen minimaal één chronische ziekte, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio’s verschillen (statistisch gezien) niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie.  ''',
    'hoog risico op angststoornis of depressie': f'''Gemiddeld heeft {nl_gemiddelde:.1f}% van de Nederlanders een hoog risico op een angststoornis of depressie. De kaarten tonen het verschil in het percentage van de volwassenen (19 jaar en ouder) die een hoog risico op een angststoornis of depressie hebben per GGD-regio, met de gekozen referentie regio ({ref_regio}). Wanneer meer volwassenen in een GGD-regio een hoog risico hebben op een angststoornis of depressie dan in {ref_regio} en dit verschil statistisch significant is, dan kleurt de regio rood. Hebben minder volwassenen een hoog risico op een angststoornis of depressie, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio’s verschillen (statistisch gezien) niet met de gekozen referentieregio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. '''}

    if 'kosten' in uitkomstmaat.lower():
        leeswijzer_uitkomstmaat = uitkomstmaat.replace(' in de basisverzekering', '')
        leeswijzer = f'''Gemiddeld zijn de {leeswijzer_uitkomstmaat} in de basisverzekering in Nederland €{nl_gemiddelde:.00f} per volwassene. De kaarten tonen het verschil in gemiddelde {leeswijzer_uitkomstmaat} per GGD-regio met de gekozen referentie regio ({ref_regio}) in de basisverzekering per volwassene (19 jaar en ouder). Wanneer de gemiddelde {leeswijzer_uitkomstmaat} in de basisverzekering per volwassene in een GGD-regio hoger zijn dan in de referentie regio ({ref_regio}),  en dit verschil statistisch significant is, dan kleurt de regio rood. Zijn de gemiddelde {leeswijzer_uitkomstmaat} in de basisverzekering lager, dan kleurt de regio blauw. Hoe groter het verschil, hoe dieper de kleur. Grijze regio's verschillen (statistisch gezien) niet met de gekozen referentie regio {ref_regio}. De eerste kaart geeft de cijfers weer zonder enige correctie. De cijfers in het tweede kaartje zijn gecorrigeerd voor leeftijd, geslacht, burgerlijke staat, migratieachtergrond, huishoudinkomen, opleidingsniveau, moeite met rondkomen, zelf-ervaren gezondheid, chronische ziekte, het risico op een angststoornis of depressie, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid en zelfregie. '''
    else:
        leeswijzer = gezondheid_leeswijzers[uitkomstmaat]

    # Hier worden alleen uitkomsten van modellen getoond die voor alle factoren tegelijk corrigeren. Tussenliggende modellen, die voor specifieke combinaties van factoren corrigeren, worden in de twee artikelen besproken.
    
    st.markdown('## Leeswijzer')

    st.markdown(leeswijzer)
    # # in sidebar? maar staat te druk
    # st.sidebar.markdown('### Leeswijzer')
    # st.sidebar.markdown(leeswijzer)

    ###############################################################



    


elif radio_nav == 'Bronverantwoording':
    st.markdown(teksten.bronverantwoording)

#############################################################

