import numpy as np
from PIL import Image

def alpha_channel_toevoegen(basis_prent):
    """indien axis=2 slechts dimensie van 3 heeft voegen we de alpha layer toe
    mee te geven de afbeelding
    """
    prent_met_alpha = basis_prent.copy()
    if prent_met_alpha.shape[2] !=4:
        prent_met_alpha = np.insert(prent_met_alpha, 3, 255, axis=2)
    return prent_met_alpha

def plaatje_even_maken(te_schalen_prent):
    """
    wanneer er met numpy geschaald wordt kan de afronding problemen veroorzaken.
    om dit in functies die 2 verschillende formaten met elkaar met concat of hstack, vstack
    de numpy array te vergroten dienen de dimensies overeen te komen
    """
    geschaalde_prent = te_schalen_prent
    width, height = geschaalde_prent.shape[:2]
    if height%2 !=0: geschaalde_prent = np.delete(geschaalde_prent,-1,axis=1)
    if width%2 !=0: geschaalde_prent = np.delete(geschaalde_prent,-1,axis=0)
    return geschaalde_prent

def plaatje_knippen(te_knippen_prentje, rijstart,rijeinde,kolomstart,kolomeinde):
    """
    met deze functie kan je een stuk uit de ingeladen afbeelding knippen
    mee te geven parameters:
    - albeelding, als numpy array
    - rijstart, in integer vanaf waar selectie mag beginnen voor de rijen
    - rijeinde, in integer waar de selectie stopt
    - kolomstart, in integer vanaf waar de selectie mag beginnen voor de kolommen
    - kolomeinde, in integer waar de selectie stopt

    de return value is het uitgeknipte stuk als numpy array
    """
    geknipt_prentje = te_knippen_prentje.copy()
    if (rijstart - rijeinde)%2 !=0: rijeinde = rijeinde -1
    if (kolomstart - kolomeinde)%2!=0: kolomeinde = kolomeinde -1
    return geknipt_prentje[
        (None if rijstart == 0 else rijstart):
        (None if rijeinde == 0 else rijeinde),
        (None if kolomstart == 0 else kolomstart):
        (None if kolomeinde == 0 else kolomeinde),:
        ]
def spiegeltje_spiegeltje(te_manipuleren_prentje,actie):
    """
    deze functie kan de afbeelding op een x en y as draaien

    input:
    - de afbeelding als numpy array
    - de actie als string, mogelijke waarden zijn:
        '0' - geen manipulatie
        'S' - spiegelen op de y as
        'V' - spiegelen op de x as
        'SV' - spiegelen op de x en y as

    output: een afbeelding als numpy array

    """
    gemanipuleerd_prentje = te_manipuleren_prentje.copy()
    if actie == '0':
        return gemanipuleerd_prentje
    elif actie == 'S':
        return gemanipuleerd_prentje[:,::-1,:]
    elif actie == 'V':
        return gemanipuleerd_prentje[::-1,:,:]
    elif actie == 'SV':
        return gemanipuleerd_prentje[::-1,::-1,:]

def kleurenpalet(te_kleuren_prentje, kleur):
    """
    deze functie kleurt je afbeelding rood, groen of blauw

    input:
    - afbeelding in numpy array
    - kleur in string met volgende mogelijkheden:
        'R' - rood
        'G' - groen
        'B' - blauw
        alle andere waarden voor kleur houden de afbeelding in originele kleur
    
    output:
    - afbeelding als numpy array
    """
    gekleurd_prentje = te_kleuren_prentje.copy()
    if kleur == 'R':
        gekleurd_prentje[:,:,[1,2]]=0
    elif kleur == 'G':
        gekleurd_prentje[:,:,[0,2]]=0
    elif kleur == 'B':
        gekleurd_prentje[:,:,[0,1]]=0
    else:
        pass
    return gekleurd_prentje

def randje_maken(prentje_zonder_rand,rand):
    """
    deze functie maakt een rand rond een afbeelding

    input:
    - afbeelding als numpy array
    - rand in integer,
        de waarde van deze integer is tevens de omtrek die rond zal voorzien worden

    output:
    - afbeelding als numpy array
    """
    hoogte_rand = rand
    breedte_rand = rand
    prentje_met_rand = prentje_zonder_rand.copy()
    height , width= prentje_met_rand.shape[:2]
    if (height + rand)%2 !=0:
        hoogte_rand = rand -1
    if (width + rand)%2!=0:
        breedte_rand = rand -1
    return np.pad(prentje_met_rand, ((rand, rand), (rand, rand), (0, 0)))

def plaatje_schalen(te_schalen_prent, percent):
    """
    deze functie schaalt de afbeelding met de PIL library volgens het meegegeven percentage
    
    input:
    afbeelding in numpy array
    percent in integer welke het 

    output:
    de geschaalde afbeelding
    """
    geschaalde_prent = te_schalen_prent.copy()
    width, height = geschaalde_prent.shape[:2]
    geschaalde_prent = Image.fromarray(geschaalde_prent)
    return np.array(geschaalde_prent.resize((round((height*percent)/100), round((width*percent)/100))))

def plaatje_schalen_numpy(te_schalen_prent, beweging, aantal=None):
    """
    een afbeelding schalen met numpy.  er wordt gebruik gemaakt van repeat van een pixel
    of delete van pixels, dit steeds volgens een factor 2.  dus iedere pixel wordt 1 maal herhaalt
    voor kolom en 1 maal voor rij.  dit resulteert in een afbeelding die 2 keer groter is in beide dimensies
    voor delete wordt iedere 2e pixel in rijen en kolommen verwijdert
    wat resulteert in een afbeelding die 2 keer kleiner is

    input:
    - afbeelding in numpy array
    - beweging in string, mogelijke waarden:
        'kleiner' - zorgt er voor dat de afbeelding een stap kleiner wordt
        'groter' - zorgt er voor dat de afbeelding een stap groter wordt
    - aantal in integer, default value none.  wanneer een waarde meegegeven wordt
    zal de beweging groter of kleiner x keer uitgevoerd worden.

    output:
    - afbeelding in numpy array
    """
    if aantal == None: aantal = 1
    geschaalde_prent = te_schalen_prent.copy()
    if beweging == 'groter':
        for _ in range(aantal):
            geschaalde_prent = geschaalde_prent.repeat(2,axis=0)
            geschaalde_prent = geschaalde_prent.repeat(2,axis=1)
    else:
        for _ in range(aantal):
            geschaalde_prent = geschaalde_prent[::2,::2,:]
    return geschaalde_prent

def breien(patroon,aantal_steken,horizontaal,spiegel, verticaal, spiegel_verticaal):
    """voorloper van de nieuwere flexibel_met_kleuren_en_richtingen_breien functie,
    gelieve die te gebruiken"""
    
    numpy_arrays_list = list()
    te_breien_prentje = patroon.copy()
    horizontaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje,'0')
    spiegel_breiwerk = spiegeltje_spiegeltje(te_breien_prentje,'H')
    verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje,'V')
    spiegel_verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje,'SV')
    if aantal_steken == 1:
        pass
    else:
        for _ in range(aantal_steken-1):
            horizontaal_breiwerk = np.concatenate((horizontaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje,'0')), axis = 1)
            spiegel_breiwerk = np.concatenate((spiegel_breiwerk,spiegeltje_spiegeltje(te_breien_prentje,'H')), axis =1)
            verticaal_breiwerk = np.concatenate((verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje,'V')), axis = 1)
            spiegel_verticaal_breiwerk = np.concatenate((spiegel_verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje,'SV')),axis=1)
    if horizontaal !=0:
        numpy_arrays_list.append(horizontaal_breiwerk)
    if spiegel !=0:
        numpy_arrays_list.append(spiegel_breiwerk)
    if verticaal !=0:
        numpy_arrays_list.append(verticaal_breiwerk)
    if spiegel_verticaal !=0:
        numpy_arrays_list.append(spiegel_verticaal_breiwerk)
    return np.concatenate((numpy_arrays_list),
                           axis = 0)

def andere_manier_breien(aantal_steken,horizontaal_prentje,spiegel_prentje, verticaal_prentje, spiegel_verticaal_prentje):
    """voorloper van de nieuwere flexibel_met_kleuren_en_richtingen_breien functie,
    gelieve die te gebruiken"""
    
    numpy_arrays_list = list()
    te_breien_horizontaal_prentje = horizontaal_prentje.copy()
    te_breien_spiegel_prentje = spiegel_prentje.copy()
    te_breien_verticaal_prentje = verticaal_prentje.copy()
    te_breien_spiegel_verticaal_prentje = spiegel_verticaal_prentje.copy()
    
    horizontaal_breiwerk = spiegeltje_spiegeltje(te_breien_horizontaal_prentje,'0')
    spiegel_breiwerk = spiegeltje_spiegeltje(te_breien_spiegel_prentje,'H')
    verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_verticaal_prentje,'V')
    spiegel_verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_spiegel_verticaal_prentje,'SV')
    
    if aantal_steken == 1:
        pass
    else:
        for _ in range(aantal_steken-1):
            horizontaal_breiwerk = np.concatenate((
                horizontaal_breiwerk,spiegeltje_spiegeltje(te_breien_horizontaal_prentje,'0')),
                                                  axis = 1)
            spiegel_breiwerk = np.concatenate((
                spiegel_breiwerk,spiegeltje_spiegeltje(te_breien_spiegel_prentje,'H')),
                                              axis =1)
            verticaal_breiwerk = np.concatenate((
                verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_verticaal_prentje,'V')),
                                                axis = 1)
            spiegel_verticaal_breiwerk = np.concatenate((
                spiegel_verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_spiegel_verticaal_prentje,'SV')),
                                                        axis=1)
    
    numpy_arrays_list.append(horizontaal_breiwerk)
    numpy_arrays_list.append(spiegel_breiwerk)
    numpy_arrays_list.append(verticaal_breiwerk)
    numpy_arrays_list.append(spiegel_verticaal_breiwerk)
    return np.concatenate((numpy_arrays_list),
                           axis = 0)

def flexibel_met_kleuren_breien(patroon, aantal_steken,horizontaal_kleur,spiegel_kleur, verticaal_kleur, spiegel_verticaal_kleur):
    """voorlopig niet meer in gebruik, functie werkt, maar is niet actief onderhouden.
    is een voorloper van de nieuwere functie flexibel_met_kleuren_en_richtingen_breien
    zie maw die functie"""
    numpy_arrays_list = list()
    te_breien_prentje_horizontaal = kleurenpalet(patroon.copy(),horizontaal_kleur)
    te_breien_prentje_spiegel = kleurenpalet(patroon.copy(),spiegel_kleur)
    te_breien_prentje_verticaal = kleurenpalet(patroon.copy(),verticaal_kleur)
    te_breien_prentje_spiegel_verticaal = kleurenpalet(patroon.copy(),spiegel_verticaal_kleur)
    
    horizontaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje_horizontaal,'0')
    spiegel_breiwerk = spiegeltje_spiegeltje(te_breien_prentje_spiegel,'H')
    verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje_verticaal,'V')
    spiegel_verticaal_breiwerk = spiegeltje_spiegeltje(te_breien_prentje_spiegel_verticaal,'SV')

    if aantal_steken == 1:
        pass
    else:
        for _ in range(aantal_steken-1):
            horizontaal_breiwerk = np.concatenate((
                horizontaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje_horizontaal,'0')),
                                                  axis = 1)
            spiegel_breiwerk = np.concatenate((
                spiegel_breiwerk,spiegeltje_spiegeltje(te_breien_prentje_spiegel,'H')),
                                              axis =1)
            verticaal_breiwerk = np.concatenate((
                verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje_verticaal,'V')),
                                                axis = 1)
            spiegel_verticaal_breiwerk = np.concatenate((
                spiegel_verticaal_breiwerk,spiegeltje_spiegeltje(te_breien_prentje_spiegel_verticaal,'SV')),
                                                        axis=1)
    if horizontaal_kleur !=0: numpy_arrays_list.append(horizontaal_breiwerk)
    if spiegel_kleur !=0: numpy_arrays_list.append(spiegel_breiwerk)
    if verticaal_kleur !=0: numpy_arrays_list.append(verticaal_breiwerk)
    if spiegel_verticaal_kleur !=0: numpy_arrays_list.append(spiegel_verticaal_breiwerk)
    return np.concatenate((numpy_arrays_list),
                           axis = 0)

def flexibel_met_kleuren_en_richtingen_breien(patroon, aantal_steken,
                                              horizontaal_kleur, horizontaal_richting,
                                              spiegel_kleur, spiegel_richting,
                                              verticaal_kleur, verticaal_richting,
                                              spiegel_verticaal_kleur, spiegel_verticaal_richting):
    """
    deze functie stelt de gebruiker in staat om een eigen gekozen patroon samen te stellen
    momenteel is de functie beperkt tot 4 rijen dit omdat er vertrokken werd vanuit de opdracht
    in deze 4 rijen is alles mogelijk, je kan per rij meegeven welke richting en welke kleur deze heeft
    het resultaat is hoe je het zelf graag wil
    
    input:
    - patroon, een afbeelding als numpy array
    - aantal steken, in integer, bepaalt hoeveel keer het patroon zich herhaalt 
    - horizontale_kleur, volgens het 'R', 'G', 'B' of 0 (zie functie kleurenpalet)
    - horizontale_richting, bepaal de richting op x en/of y as hoe de afbeelding moet gedraaid worden
        '0', 'S', 'V', 'SV' (zie functie spiegeltje_spiegeltje voor verdere uitleg en details)
    - verticale_kleur (zelfde als horizontale_kleur)
    - verticale_richting (zelfde als horizontale_richting)
    - spiegel_verticale_kleur (zelfde als horizontale_kleur)
    - spiegel_verticale_richting (zelfde als horizontale_richting)

    output:
    - afbeelding als numpy array
        '"""
    numpy_arrays_list = list()
    te_breien_prentje_horizontaal = kleurenpalet(patroon.copy(),horizontaal_kleur)
    te_breien_prentje_spiegel = kleurenpalet(patroon.copy(),spiegel_kleur)
    te_breien_prentje_verticaal = kleurenpalet(patroon.copy(),verticaal_kleur)
    te_breien_prentje_spiegel_verticaal = kleurenpalet(patroon.copy(),spiegel_verticaal_kleur)
    
    horizontaal_breiwerk = np.tile(spiegeltje_spiegeltje(te_breien_prentje_horizontaal,horizontaal_richting),(1,aantal_steken,1))
    spiegel_breiwerk = np.tile(spiegeltje_spiegeltje(te_breien_prentje_spiegel,spiegel_richting),(1,aantal_steken,1))
    verticaal_breiwerk = np.tile(spiegeltje_spiegeltje(te_breien_prentje_verticaal,verticaal_richting),(1,aantal_steken,1))
    spiegel_verticaal_breiwerk = np.tile(spiegeltje_spiegeltje(te_breien_prentje_spiegel_verticaal,spiegel_verticaal_richting),(1,aantal_steken,1))

    if horizontaal_kleur !=0: numpy_arrays_list.append(horizontaal_breiwerk)
    if spiegel_kleur !=0: numpy_arrays_list.append(spiegel_breiwerk)
    if verticaal_kleur !=0: numpy_arrays_list.append(verticaal_breiwerk)
    if spiegel_verticaal_kleur !=0: numpy_arrays_list.append(spiegel_verticaal_breiwerk)
    return np.concatenate((numpy_arrays_list),
                           axis = 0)

def flexibel_breien(patroon, positie= None):
    """
    deze functie maakt deel uit van de verplichte oefening waarbij een grote afbeelding omringt is 
    door allemaal gekleurde, verkleinde afbeeldingen van de grote afbeelding.
    er werd wel een extraatje voorzien zodat niet alleen de standaard afbeelding gegenereerd wordt
    
    input:
    - patroon, als afbeelding in numpy array
    - positie; extra optie die het mogelijk maakt om de positie te kiezen waar de 
    grote afbeelding staat op het kleine patroon, mogelijke waarden:
        'BR' - boven rechts
        'BL' - boven links
        'MR' - midden rechts
        'ML' - midden links
        'OR' - onder rechts
        'OL' - onder links
        alle andere ingaves plaatsen de grote afbeelding gecentreerd in het midden
         
    - output:
     een samengestelde afbeelding van verkleinde afbeeldingen in blauw, rood, groen
      waarbij de grote afbeelding werd geplaatst volgens de positie """
    nieuw_patroon = patroon.copy()
    kleiner_patroon = plaatje_schalen_numpy(nieuw_patroon,'kleiner')
    blauwe_tile = kleurenpalet(kleiner_patroon,'B')
    rode_tile = kleurenpalet(kleiner_patroon,'R')
    groene_tile = kleurenpalet(kleiner_patroon,'G')

    nieuw_patroon = match_afmetingen(nieuw_patroon,kleiner_patroon)

    if positie == 'BL':
        eerste_band = np.hstack((nieuw_patroon,np.vstack((np.hstack((blauwe_tile,blauwe_tile)), np.hstack((rode_tile,rode_tile))))))
        tweede_band = np.tile(rode_tile,(1,4,1))
        derde_band = np.tile(groene_tile, (1,4,1))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    elif positie == 'BR':
        eerste_band = np.hstack((np.vstack((np.hstack((blauwe_tile,blauwe_tile)), np.hstack((rode_tile,rode_tile)))),nieuw_patroon))
        tweede_band = np.tile(rode_tile,(1,4,1))
        derde_band = np.tile(groene_tile, (1,4,1))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    elif positie == 'ML':
        eerste_band = np.tile(blauwe_tile,(1,4,1))
        tweede_band = np.hstack((nieuw_patroon,np.vstack((np.hstack((rode_tile,rode_tile)), np.hstack((rode_tile,rode_tile))))))
        derde_band = np.tile(groene_tile, (1,4,1))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    elif positie == 'MR':
        eerste_band = np.tile(blauwe_tile,(1,4,1))
        tweede_band = np.hstack((np.vstack((np.hstack((rode_tile,rode_tile)), np.hstack((rode_tile,rode_tile)))),nieuw_patroon))
        derde_band = np.tile(groene_tile, (1,4,1))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    elif positie == 'OL':
        eerste_band = np.tile(blauwe_tile,(1,4,1))
        tweede_band = np.tile(rode_tile, (1,4,1))
        derde_band = np.hstack((nieuw_patroon, np.vstack((np.hstack((rode_tile,rode_tile)), np.hstack((groene_tile,groene_tile))))))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    elif positie == 'OR':
        eerste_band = np.tile(blauwe_tile,(1,4,1))
        tweede_band = np.tile(rode_tile, (1,4,1))
        derde_band = np.hstack((np.vstack((np.hstack((rode_tile,rode_tile)), np.hstack((groene_tile,groene_tile)))),nieuw_patroon))
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))
    else:
        eerste_band = np.tile(blauwe_tile,(1,4,1))
        tweede_band = np.hstack((np.vstack((rode_tile,rode_tile)), nieuw_patroon,np.vstack((rode_tile,rode_tile))))
        derde_band = np.tile(groene_tile, (1,4,1)) 
        resultaat = np.vstack((eerste_band, tweede_band, derde_band))

    return resultaat

def match_afmetingen(grote_plaat, kleine_plaat):
    """
    deze functie is speciaal voorzien om de functie flexibel breien te ondersteunen
    omdat er in flexibel breien met 2 verschillende groottes van numpy arrays wordt gewerkt
    kan een mismatch in dimensies ontstaan.  vooral bij verkleinen wordt een afronding naar boven
    gedaan wanneer np.delete wordt gebruikt, wat resulteert in een verkleinde dimensie die, eens je
    ze weer vermenigvuldigt 1 rij en/of 1 kolom groter is dan de afbeelding waarvan vertrokken werd
    om dit te compenseren, controleren we de breedte en hoogte van de kleine afbeelding
    en zorgen de grote afbeelding matcht, dit door np.delete of np.pad te gebruiken
    
    input: de grote afbeelding en de kleine afbeelding
    output: de grote afbeelding
    """
    grote_plaat = grote_plaat
    grote_width, grote_height= grote_plaat.shape[:2]
    kleine_width,kleine_height= kleine_plaat.shape[:2]
    if kleine_width < int(grote_width/2):
        grote_plaat = np.delete(grote_plaat,-1,axis=0)
    else:
        grote_plaat = np.pad(grote_plaat,((0,0),(0,1),(0,0)), constant_values=0)
    if kleine_height < int(grote_height/2):
        grote_plaat = np.delete(grote_plaat,-1,axis=1)
    else:
        grote_plaat = np.pad(grote_plaat,((0,1),(0,0),(0,0)), constant_values=0)
    return grote_plaat

