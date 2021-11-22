class teksten:


    introductie = '''Deze Regiovergelijker laat zien hoe regio’s van elkaar verschillen als het gaat om gezondheid en zorgkosten. We laten daarnaast zien in hoeverre deze verschillen zijn toe te schrijven aan persoonlijke kenmerken van inwoners per GGD-regio. Met deze kenmerken kijken we zowel naar demografie (leeftijd, geslacht, burgerlijke staat, migratieachtergrond), als sociaaleconomische status (opleidingsniveau, inkomen, moeite met rondkomen), leefstijl (body mass index (BMI), roken, alcoholconsumptie, bewegen) eenzaamheid en zelfregie. Van al deze kenmerken is bekend dat zij gezondheid kunnen beïnvloeden. Wat dragen zij **samen** dan bij aan het verklaren van regionale verschillen in gezondheid? 

Om deze vraag te kunnen beantwoorden is gebruik gemaakt van gecombineerde, geanonimiseerde gegevens van meer dan 300,000 Nederlanders van 19 jaar en ouder die representatief zijn voor de Nederlandse bevolking. 

In het Tijdschrift voor Gezondheidswetenschappen (TSG) themanummer Sociaaleconomische Gezondheidsverschillen wordt in twee onderzoeken gekeken naar de verklaring van regionale verschillen in gezondheid en zorgkosten ten opzichte van de regio Zuid-Limburg zonder en met correctie voor bovengenoemde persoonlijke kernmerken. In deze Regiovergelijker kun je zelf kiezen welke regio je als referentie wilt gebruiken.

Voor een korte uitleg van ons onderzoek en het gebruik van de Regiovergelijker klik HIER [link filmpje]. De wetenschappelijke artikelen kun je hier downloaden over gezondheid[link artikel] en zorgkosten[link artikel].

'''

    leeswijzers = {'Minder goed ervaren gezondheid': '''
    '''}

    def prep_leeswijzer(uitkomstmaat, gemiddelde):
        pass

    dankwoord = '''Deze Regiovergelijker is mogelijk gemaakt door de [Academische Werkplaats Publieke Gezondheid](https://www.academischewerkplaatslimburg.nl/) en de [Academische Werkplaats Duurzame Zorg](https://www.maastrichtuniversity.nl/nl/onderzoek/academische-werkplaats-duurzame-zorg-limburg).
Met dank aan de GGD-en, CBS en Vektis voor het beschikbaar stellen van de geanonimiseerde Microdatabestanden in de CBS Remote Access omgeving.'''


    bronverantwoording = '''
    # Bronverantwoording
De data voor dit onderzoek is volledig geanonimiseerd geanalyseerd binnen de beveiligde omgeving van het CBS (Remote Access). Hieronder worden alle gebruikte uitkomstmaten en correctie variabelen opgesomd. Voor de uitgebreide methodologische overwegingen en limitaties verwijzen we naar de wetenschappelijk artikelen [link1] en [link2].

## Uitkomsten
De uitkomstmaten voor dit onderzoek zijn zelf-ervaren gezondheid, het hebben van minimaal één chronische ziekte, het risico op een angststoornis of depressie en zorgkosten zoals vergoed onder de basisverzekering (totaal, huisartsconsult, farmacie en medisch specialistische zorg). De drie gezondheidsuitkomsten zijn afgeleid van de Gezondheidsmonitor Volwassenen en Ouderen 2016 van de GGD en CBS. De gegevens over de vergoede zorgkosten zijn afkomstig van Vektis over het jaar 2017.

### Zelf-ervaren gezondheid
De variabele ‘zelf-ervaren gezondheid’ is gebaseerd op de vraag ‘Hoe is over het algemeen uw gezondheid’ en werd beantwoord op een 5-punt schaal. De antwoorden worden als volgt gecategoriseerd:
* Goede ervaren gezondheid (‘goed’ of ‘zeer goed’)
* Minder goede ervaren gezondheid (‘gaat wel’, ‘slecht’ of ‘zeer slecht’)
### Het hebben van minimaal één chronische ziekte
De variabele ‘chronische ziekte’ is afgeleid van de vraag ‘Heeft u één of meer langdurige ziekten of aandoeningen?’ Hier wordt bij toegelicht dat ‘langdurig’ (naar verwachting) 6 maanden of langer is. Deze vraag werd beantwoord met ‘ja’ of ‘nee’.
### Het risico op een angststoornis of depressie
Het risico op een angststoornis of een depressie is afgeleid van de [Kessler-10 vragenlijst](https://doi.org/10.1017/s0033291702006074). De 10 vragen worden beantwoord middels de antwoordcategorieën op een 5-punts schaal (altijd, meestal, soms, af en toe, en nooit). Deze antwoorden leiden tot een score tussen de 10 (geen risico) en 50 (hoog risico). De Kessler-10 vragenlijst is opgesteld uit deze vragen:

In de afgelopen 4 weken…

1. Hoe vaak voelde u zich erg vermoeid zonder duidelijke reden?
2. Hoe vaak voelde u zich zenuwachtig?
3. Hoe vaak was u zo zenuwachtig dat u niet tot rust kon komen?
4. Hoe vaak voelde u zich hopeloos?
5. Hoe vaak voelde u zich rusteloos of ongedurig?
6. Hoe vaak voelde u zich zo rusteloos dat u niet meer stil kon zitten?
7. Hoe vaak voelde u zich somber of depressief?
8. Hoe vaak had u het gevoel dat alles veel moeite kostte?
9. Hoe vaak voelde u zich zo somber dat niets hielp om u op te vrolijken?
10. Hoe vaak vond u zichzelf afkeurenswaardig, minderwaardig of waardeloos?

### Totale zorgkosten
Dit zijn alle kosten die worden vergoed onder basisverzekering van de Zorgverzekeringswet. Naast huisarts, farmacie, medisch specialistische en GGZ kosten vallen hier ook kleinere kostenposten onder zoals hulpmiddelen, mondzorg, paramedische zorg, ziekenvervoer, geboortezorg, grensoverschrijdende zorg, geriatrische revalidatie zorg en verpleging en verzorging.

### Huisartsconsultkosten 
Dit bevat alle kosten voor huisartsconsulten, dit is exclusief het inschrijftarief en overige huisartsenzorgkosten.

### Farmaciekosten
Dit bevat de kosten voor farmaceutische hulp en praktijkkosten voor apothekers. Dit is exclusief de kosten voor geneesmiddelen verstrekt door ziekenhuizen.

### Medisch specialistische kosten
Onder medisch specialistische kosten vallen alle Diagnose Behandel Combinatie (DBC) zorgproducten, geneesmiddelen verstrekt in ziekenhuizen, kaakchirurgie, en overige ziekenhuis- en curatieve zorg.

### GGZ kosten
Onder GGZ kosten vallen Diagnose Behandel Combinatie (DBC) met en zonder verblijf, generalistisch basis en langdurige GGZ. Bij opname in een GGZ-instelling worden de kosten tot 3 jaar gefinancierd uit de Zorgverzekeringswet en daarna vanuit de Wet Langdurige Zorg (Wlz). De kosten die worden gefinancierd door de Wlz worden niet meegenomen in de Vektis data.

## Correctie
In de totale correctie worden variabelen meegenomen uit de Gezondheidsmonitor (leeftijd, geslacht, burgerlijke staat, opleidingsniveau, moeite met rondkomen, BMI, roken, alcoholconsumptie, voldoende beweging, eenzaamheid, zelfregie) en aanvullende gegevens uit de registers van het CBS op basis van de Basisregistratie Personen (migratieachtergrond) en de Belastingdienst (huishoudinkomen).

### Burgerlijke staat
Burgerlijke staat is opgedeeld in de categorieën:

* Gehuwd, geregistreerd partnerschap, samenwonend 
* Ongehuwd, nooit gehuwd geweest
* Gescheiden
* weduwe, weduwnaar

### Migratieachtergrond
De migratieachtergrond is gebaseerd op de gegevens uit de Basisregistratie Personen met als categorieën een Nederlandse achtergrond, westerse migratie achtergrond, of niet-westerse migratie achtergrond.

### Huishoudinkomen 
Het inkomen is per huishouden opgeteld en gecorrigeerd voor het aantal personen en de samenstelling van het huishouden (ofwel gestandaardiseerd met behulp van equivalentiefactoren). Vervolgens zijn de gestandiseerde huishoudinkomens vergeleken met alle huishoudinkomens in Nederland en op basis hiervan in 4 groepen verdeeld:
* 0-25% laagste huishoudinkomens (ofwel 1e kwartiel)
* 26-50% (2e kwartiel)
* 51-75% (3e kwartiel)
* 76-100% hoogste huishoudinkomens (4e kwartiel)

### Opleidingsniveau 
Op basis van de vraag ‘Wat is uw hoogst voltooide opleiding? (Een opleiding afgerond met diploma of voldoende getuigschrift)’ zijn de volgende vier categorieën gedefinieerd:
* (Speciaal) Basisonderwijs of geen onderwijs
* Lager voorbereidend beroepsonderwijs (lbo) of middelbaar algemeen voortgezet onderwijs (mavo)
* Middelbaar beroepsonderwijs (mbo), hoger algemeen en voorbereiden wetenschappelijk onderwijs (havo en vwo)
* Hoger beroepsonderwijs (hbo) of wetenschappelijk onderwijs (wo)

### Moeite met rondkomen
De variabele moeite met rondkomen is gebaseerd op de vraag ‘Hebt u de afgelopen 12 maanden moeite gehad om van het inkomen van uw huishouden rond te komen’. De antwoordmogelijkheden zijn:
* Nee, geen enkele moeite
* Nee, geen moeite, maar ik moet wel letten op mijn uitgaven
* Ja, enige moeite
* Ja, grote moeite

### Body Mass Index (BMI)
Het [BMI](https://www.euro.who.int/en/health-topics/disease-prevention/nutrition/a-healthy-lifestyle/body-mass-index-bmi) is berekend aan de hand van de gevraagde lengte (in centimeter) en gewicht (in kilogram). Vervolgens zijn deze BMI-groepen gevormd:
* Ondergewicht (een BMI van 18,5 of lager)
* Normaal (een BMI tussen de 18,5 en 25)
* Overgewicht (een BMI tussen 25 en 30)
* Obesitas (een BMI van 30 of hoger)

### Roken
Op basis van de vragen ‘Rookt u weleens’ en ‘Heeft u vroeger wel gerookt’ zijn de volgende categorieën gevormd:
* Nooit gerookt
* Ex-roker
* Roker

### Alcoholconsumptie
De Gezondheidsmonitor 2016 stelt een 7-tal vragen over alchol consumptie. Op basis hiervan zijn de volgende categorieën gedefinieerd:
* Nooit 
* Matig 
* Overmatig
Er is sprake van overmatige alcoholconsumptie bij meer dan 14 glazen per week voor vrouwen, en meer dan 21 glazen voor mannen [zoals gedefinieerd door de Gezondheidsraad](https://www.gezondheidsraad.nl/documenten/adviezen/2015/11/04/alcohol-achtergronddocument-bij-richtlijnen-goede-voeding-2015).

### Voldoende beweging 
De Gezondheidsmonitor stelt meerdere vragen over het beweeggedrag van respondenten, zoals woon-werkverkeer, lichamelijke activiteit op werk of school, huishoudelijke activiteiten, vrije tijd en sport. Op basis van deze antwoorden is berekend of een persoon minimaal 2,5 uur matig intensief beweegt per week of 2 keer per week intensief traint. Als aan één van deze voorwaarden is voldaan, is er sprake van voldoende beweging, [zoals gedefinieerd door de Gezondheidsraad](https://www.gezondheidsraad.nl/documenten/adviezen/2017/08/22/beweegrichtlijnen-2017).

### Eenzaamheid 
Voor eenzaamheid is gebruik gemaakt van de [Jong-Gierveld schaal](https://doi.org/10.1177/014662168500900307). Deze schaal bestaat uit 11 stellingen die worden beantwoord met “ja”, “min of meer” of “nee”. Deze antwoorden resulteren in een score tussen de 0 en 11. Een persoon met een score van 0,1 of 2 wordt beschouwd als niet eenzaam. Iemand is matig eenzaam bij een score van 3 tot en met 8, ernstig eenzaam bij een score van 9 of 10 en zeer ernstig eenzaam bij een score van 11. De 11 stellingen zijn:

1.	Er is altijd wel iemand in mijn omgeving bij wie ik met mijn dagelijkse probleempjes terecht kan.
2.	Ik mis een echt goede vriend of vriendin.
3.	Ik ervaar een leegte om mij heen.
4.	Er zijn genoeg mensen op wie ik in geval van narigheid kan terugvallen.
5.	Ik mis gezelligheid om mij heen.
6.	Ik vind mijn kring van kennissen te beperkt.
7.	Ik heb veel mensen op wie ik volledig kan vertrouwen.
8.	Er zijn voldoende mensen met wie ik me nauw verbonden voel.
9.	Ik mis mensen om mij heen.
10.	Vaak voel ik me in de steek gelaten.
11.	Wanneer ik daar behoefte aan heb, kan ik altijd bij mijn vrienden terecht.
### Zelfregie
De variabele zelfregie is gebaseerd op de 7 stellingen van de [Pearlin & Schooler Mastery Scale](https://doi.org/10.2307/2136319). De 7 stellingen worden beantwoord op een 5-punt schaal van “helemaal eens” tot “helemaal oneens”, met een uiteindelijke score van 7-35. Hoe hoger de uiteindelijke score, hoe meer regie men over het eigen leven ervaart. De stellingen zijn:

1. Ik heb weinig controle over de dingen die me overkomen.
2. Sommige van mijn problemen kan ik met geen mogelijkheid oplossen.
3. Er is weinig dat ik kan doen om belangrijke dingen in mijn leven te veranderen.
4. Ik voel me vaak hulpeloos bij het omgaan met de problemen van het leven.
5. Soms voel ik dat ik een speelbal van het leven ben.
6. Wat er in de toekomst met me gebeurt, hangt voor het grootste deel van mezelf af.
7. Ik kan ongeveer alles als ik m’n zinnen erop gezet heb.
'''