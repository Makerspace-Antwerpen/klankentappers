# Klankentappers hardware

## Lijm de O-ring op het microfoondeksel

We starten met deze stap zodat de lijm kan drogen totdat we het dekseltje nodig hebben

Benodigdheden
* Microfoondeksel
* O-ring
* Secondelijm
* Pincet

1. Leg voorzichtig 2 of 3 druppeltjes secondelijm op de o-ring
2. Gebruik een pincet om de o-ring onderaan het microfoondeksel aan te brengen

⚠️ Opgelet! Secondelijm kleeft onmiddellijk en is niet te herstellen, zorg dat de o-ring daarom direct mooi gecentreerd is.

⚠️ Opgelet! Zorg dat het gaatje in het deksel open blijft en niet dichtgelijmd geraakt. Gebruik eventueel een naald om het gaatje terug te openen.

![Kabeldoos](/documentation/imgs/hardware_oring.png)

## Bereid de kabeldoos voor

Benodigdheden
* Kabeldoos
* Schroevendraaier/hamer

1. Verwijder 2 openingen voor wartels
2. Sluit de gaten in de bodem met de bijgeleverde rubberen stopjes

![Kabeldoos](/documentation/imgs/hardware_kabeldoos.png)

## Bereid het bevestigingsplaatje voor

Benodigdheden
* Bevestigingsplaatje
* 4 M3x8 schroeven
* 4 M2.5 standoffs

1. Bevestig 4 standoffs in het bevestigingsplaatje
2. Bevestig het plaatje in de kabeldoos

![Bevestigingsplaatje](/documentation/imgs/hardware_bevestigingsplaat.png)

## Maak de USB kabel dikker

Omdat de USB kabel te dun is om goed afgesloten te worden met de wartel, maken we hem dikker met isolatietape.

Benodigdheden
* USB-C kabel
* Isolatietape

1. Gebruik isolatietape om de USB kabel dikker te maken, zo'n 2cm van de stekker, tot zo'n 9à10mm dikte.

![USB kabel](/documentation/imgs/hardware_kabel.png)


## Monteer de Raspberry Pi

Benodigdheden
* USB-C kabel
* Wartel
* Raspberry Pi
* SD kaart die voorbereid werd met Balena image
* 4 M2.5x10 schroeven

1. Haal de USB-C kabel door de wartel
2. Breng de SD kaart aan in de Raspberry Pi
3. Verbind de USB-C kabel met de Raspberry Pi
4. Bevestig de Raspberry Pi met 4 schroeven op de bevestigingsplaat
5. Schroef de wartel goed vast, maar let op dat je geen extra torsie op de kabel zet

⚠️ Opgelet! De Raspberry Pi en zijn USB-C kabel passen maar net (of net niet?) in de kabeldoos. De USB-C verbinding zit daardoor een beetje scheef, maar dat is niet erg. Als je de USB-C kabel insteekt en er gaan LEDjes branden op de Raspberry Pi, dan zit je stekker goed.

![Raspi in doos](/documentation/imgs/hardware_raspi_in_doos.png)

## Bekabel de microfoon

Benodigdheden
* Printplaat met microfoon
* 5 F-F jumper kabels in 5 verschillende kleuren
* Pen en papier

1. Bevestig 5 jumperkabels aan de pinnen VDD, GND, SDATA, BCLK en LRCLK op het printplaatje
2. Maak een notitie van welke kleur kabel je aan welke pin hebt verbonden

![Printplaat](/documentation/imgs/hardware_microfoon.png)

## Verbind de microfoon met de Raspberry Pi

Benodigdheden
* 3D printed wartel

1. Bevestig de wartel voor de microfoon in de kabeldoos. Zorg dat de rand binnenin naar buiten steekt
2. Haal de kabels aan de microfoon door de wartel
3. Bevestig de 5 kabels met je notities uit de vorige stap, zoals aangegeven in onderstaande figuur

![GPIO](/documentation/imgs/hardware_gpio.png)

* VDD: Onderste rij, eerste pin van links
* GND: Bovenste rij, derde pin van links
* BCLK: Bovenste rij, zesde pin van links
* SDATA: Bovenste rij, tweede pin van rechts
* LRCLK: Onderste rij, derde pin van rechts

⚠️ Opgelet! De zelfgemaakte wartel is broos. Schroef hem niet te hard vast zodat ie niet breekt.

⚠️ Opgelet! Als de verbindingen niet juist zijn, kan je de printplaat kapot maken! Zorg dat de verbindingen correct zijn aangesloten.

![GPIO](/documentation/imgs/hardware_gpio_connected.png)

## Sluit de microfoon af met het dekseltje

Benodigdheden
* 3D printed deksel met o-ring

1. Gebruik het dekseltje om de printplaat vast te zetten in de wartel.

⚠️ Opgelet! De zelfgemaakte wartel is broos. Schroef het deksel niet te hard vast zodat ie niet breekt.

![deksel](/documentation/imgs/hardware_deksel.png)

## Bevestig de windkap

Benodigdheden
* Windkap
* Cable tie

1. Bevestig de windkap met een cable tie over het deksel

![deksel](/documentation/imgs/hardware_windkap.png)

## Klaar!

Als we het deksel nog sluiten is de hardware klaar!

