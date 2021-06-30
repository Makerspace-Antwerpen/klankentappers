# Klankentappers omgevingsgeluidsensor

Nauwkeurige dBA metingen met een Raspberry Pi en een I2S MEMS microfoon, voor citizen science projecten.

![klankentapper](/documentation/imgs/hardware_windkap.png)

## Over Klankentappers

De klankentapper is een sensor waarmee je het omgevingsgeluid rond je huis kan meten. Op een online dashboard kan je de hoeveelheid omgevingsgeluid rond je huis bekijken. De sensor bevat een computer (Raspberry Pi) en een op maat gemaakte printplaat met een microfoon. Op de computer berekenen we heel precies de hoeveelheid geluid uit, in dBA, dat is een maat van geluid die is afgestemd op het menselijk oor. 

Een Klankentapper is een open source omgevingsgeluidsensor, ontwikkeld door [Makerspace Antwerpen](https://www.makerspacea.be/) voor het [imec Hackable City of Things](https://www.imeccityofthings.be/en/projecten/hackable-city-of-things_2) initiatief, in samenwerking met [Gents Milieufront](https://www.gentsmilieufront.be/) en [Bewonersgroep Luchtbal Noord](https://www.facebook.com/BewonersgroepLuchtbalNoord/), en wetenschappelijk ondersteund door de [imec Waves onderzoeksgroep](https://www.waves.intec.ugent.be/).

Dit ontwikkelingsproject is momenteel in een Proof-of-Concept fase. Tijdens de zomer van 2021 testen we in Gent en Antwerpen 10 omgevingsgeluidsensoren uit, om te leren hoe precies ze omgevingsgeluid kunnen meten en hoe bestendig ze zijn tegen buiten staan.

## Wat is een klankentapper?

Een [hardware](/hardware/) sensor met [sofware](/src/), [handleiding](/documentation/) en cloud componenten.

### Hardware om een omgevingsgeluidsensor te bouwen

Deze repository bevat het [hardware ontwerp](/hardware/) om een nauwkeurige dBA sensor te maken op basis van een Raspberry Pi 4 en een custom microfoonprintplaat met een [Infineon IM69D120](https://www.infineon.com/cms/en/product/sensor/mems-microphones/mems-microphones-for-consumer/im69d120/) MEMS microfoon. Verder werden zoveel mogelijk off-the-shelf onderdelen, 3D prints en lasercuts gebruikt. 

In onze [handleiding](/documentation/) vind je de bill of materials en een beschrijving om een klankentapper te bouwen.

#### Technologiekeuze

Na een vergelijking van ST MP34DT01-M, Knowles SPH0645LM4H, Vesper VM3000 en Infineon IM69D120 leerden we dat de laatste met goede nauwkeurigheid (<±1.5dBA) kan ingezet worden om op citizen science manier in te zetten om omgevingsgeluid te meten. De nauwkeurigheid van de microfoon en de hardware van de volledige sensor werd uitvoerig getest in de anechoïsche kamer van imec Waves. 

We ontwikkelden voor de Infineon IM69D120 microfoon een kleine printplaat. Ze bevat naast de microfoon ook een [Analog Devices ADAU7002](https://www.analog.com/en/products/adau7002.html#product-overview) PDM-naar-I2S converter chip. Hierdoor kan je de audiodata zowel in I2S als in PDM formaat uitlezen. Dankzij de consistentie van de microfoons onder elkaar kan de microfoon met 1 standaard calibratie (per batch geproduceerde microfoons) gebruikt worden voor citizen science doeleinden.

#### Future work

De omgevingsgeluidsensor is momenteel in een Proof-of-Concept fase. Tijdens de zomer van 2021 leren we hoe goed we omgevingsgeluid kunnen meten en hoe goed de sensor bestand is tegen slecht weer. In de toekomst, na review van de PoC hopen we een betere iteratie te ontwikkelen. Mogelijk ontwikkelen we ook een eenvoudigere versie met een 

### Software om omgevingsgeluiden te analyseren

Deze repository bevat de [software](/src/), in Python, om de data van de microfoon correct in te lezen in de Raspberry Pi, ze te corrigeren voor gekende limitaties van MEMS microfoons met IIR filters, ze te calibreren, er correct dBA uit te berekenen, 1/3 octaafbanden te berekenen en geluidsgebeurtenissen te detecteren.

#### Future work

Tijdens de Proof-of-Concept fase wordt deze software aan een langdurige test onderworpen.

Met AI willen we on-edge omgevingsgeluiden herkennen. Zo willen we bijvoorbeeld automatisch de bron van gebeurtenissen herkennen, zoals een auto, een tram, een gesprek of een werken in de buurt. Door de classificatie van geluiden op de sensor te doen houden we geen privacy-gevoelige context van geluidsopnames bij en onthouden we enkel de anonieme geberutenissen, bvb "een auto, 67.3dBA". Door de Raspberry Pi te gebruiken, kunnen we de herkenning van geluiden mogelijk maken. We bestuderen tijdens de PoC of het mogelijk is geluidsbronnen goed te herkennen met AI.

### Internet of Things stack om de data online te volgen en monitoren

Tijdens de Proof-of-Concept fase pushen we de data (dBA) naar een Thingsboard setup. Per device zijn dashboards beschikbaar. We monitoren de devices en distribueren over-the-air software updates naar de toestellen met Balena.
