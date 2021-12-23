#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

data = {
'aisles_msg_1': "Dal fondo del corrido io arriva una luce fioca, forse troverai altre stanze?",
'aisles_msg_2' : "Il soffitto è crollato e il corridoio è bloccato (blocca la strada con uno o più segnalini crollo accanto all'ultima porta). O tornare indietro o entrare. Che cosa ti dice di fare l\'istinto?",
'aisles_msg_3' : "Il soffitto è crollato e il corridoio è bloccato dopo la porta (blocca la strada con uno o più segnalini crollo accanto all'ultima porta). Dal buio del corridoio arriva un rumore sinistro: sulla tua strada trovi {}",
'aisles_msg_4' : "Hai trovato una porta {}. Colloca una porta per entrare nella prima stanza inesplorata o ancora senza accessi. {}",
'aisles_msg_5' : "Hai trovato due porte. Una prima porta {} e una seconda porta {}. Ognuna ti conduce ad una stanza inesplorata o ancora senza accessi. {}",
'aisles_msg_6' : "Hai trovato tre porte. Colloca una prima porta {}, una seconda porta {} e una terza porta a {}. Ognuna ti conduce ad una stanza inesplorata o ancora senza accessi.{}",
'aisles_msg_7' : "Non hai trovato nessuna porta.",
'aisles_msg_8' : "\nATTENZIONE: Se le porte indicate conducono fuori dal tabellone, mettile frontalmente sulla prima stanza utile. Se invece ti conducono su stanze già esplorate ignora il comando.",
'dungeon_msg_00': "(Esplorazione del turno {}) \nScrutate con attenzione tra le tenebre davanti a voi. Ecco cosa vedete... \n",
'dungeon_msg_01': "Una porta chiusa ti sbarra la strada (Metti una porta chiusa nella stanza {}). \n",
'dungeon_msg_02': "Da una porta aperta arriva della luce (Metti una porta aperta nella stanza {}). \n",
'dungeon_msg_03': "Il sotterraneo continua attraverso le tenebre. (Puoi continuare vero il POV {}). \n",
'dungeon_msg_04': "Puoi continuare o tornare sui tuoi passi. La via del ritorno resta libera ma strani scricchiolii provengono dal soffitto. Meglio affrettarsi. (La via verso il POV {} resta libera, ). \n",
'dungeon_msg_05': "Non c'è modo di andare avanti. Sembra proprio un vicolo cieco e il passaggio è bloccato da un crollo (Metti un segnalino crollo adiacente all'eroe verso il POV {}. \n",
'dungeon_msg_06': "Un crollo blocca l'accesso a questa parte del sotterraneo. (Metti un segnalino crollo adiacente all'eroe verso il POV {}. \n",
'dungeon_msg_07': "Un muro fatto di rozze pietre vi sbarra la strada. (Metti un segnalino crollo adiacente all'eroe verso il POV {}. \n",
'dungeon_msg_08': "Una luce innaturale illumina il passaggio. Per ora è possibile proseguire. (Il corridoio verso il POV {} è libero...per ora). \n",
'dungeon_msg_09': "Un vicolo cieco che sa di trappola. (Metti un segnalino verso ogni altro POV non esplorato distante almeno 1 casella dall'eroe). \n",
'dungeon_msg_10': "Questo luogo vi disorienta e una strana aura aleggia nell'aria e vedete della mani trasparenti che vi trattengono. (La via verso ogni altro POV è bloccata (Mettete un segnalino crollo verso altre direzioni; il vostro turno finisce qui. Per potervi muovere ottenete uno scudo lanciando i dadi da combattimento in base ai vostri Punti Mente. Attaccate e difendete con un dado in meno.) \n",
'dungeon_msg_11': "La strada è sbarrata...(Metti un segnalino verso ogni altro POV non esplorato distante almeno 1 casella dall'eroe). \n",
'dungeon_msg_12': "In questo punto il sotterraneo prende due strade. Puoi proseguire verso il POV {} oppure il POV {} \n",
'dungeon_msg_13': "Per ora la strada sembra libera.\n {}",
'dungeon_msg_14': "Sembrava un vicolo cieco, ma sembra esserci un altro cunicolo.\n {}",
'dungeon_msg_15': "Il percorso si biforca.\n{}",
'dungeon_msg_16': "Il cunicolo sembra proseguire nel buio.\n {}",
'dungeon_msg_17': "Sei arrivato in fondo a questo cunicolo.\n {}",
'dungeon_msg_18': "Questa strada sembra non portare da nessuna parte.\n{}",
'dungeon_msg_19': "Fetore e un senso di malessere aleggiano per il corridoio. A stento prosegui.\n PIPPO {}",
'dungeon_msg_20': "Sembra un vicolo cieco, solo pietre crollate e brandelli di muri si parano davanti a voi. Metti un segnalino crollo verso ogni altro POV non esplorato distante almeno 2 caselle dall\'eroe o dopo una porta.",
'dungeon_msg_21': "La via prosegue verso il POV {}.",
'treasures_msg_1' : "Pesca una carta dal mazzo dei Tesori.",
'treasures_msg_2' : "Dopo una attenta ricerca forse hai trovato qualcosa. Scopri cosa contiere il tesoro.",
'treasures_msg_3' : "Mentre cerchi tra vecchi stracci e ossa di sorcio, senti uno scatto: un dardo ti colpisce e perdi 1 punto corpo (Ignora questa istruzione se hai cercato trabocchetti in questa stanza.",
'treasures_msg_4' : "Pesca una carta dal mazzo dei Tesori.",
'secret_doors_msg_1': "Non hai trovato nessuna porta segreta.",
'secret_doors_msg_2' : "Hai trovato una porta segreta a metà del muro {}. (Se ti porta ad una stanza o corridio già esplorati o con già una porta, mettila verso una stanza o un corridoio adiacente; se non sono possibili le prime due opzioni allora mettine una nella stanza in cui sei e un'altra in una stanza inesplorata o ancora senza accessi.",
'secret_doors_msg_3' : "Hai trovato una botola. Metti una botola davanti a te e un'altra in una stanza non esplorata",
'secret_doors_msg_4' : "Facendo pressione su un blocco di pietra si rivela davanti a te un tunnel che ti conduce nelle viscere della terra. Quando risali ed entri nella stanza non puoi credere ai tuoi occhi...(metti la porta segreta verso una stanza adiacente se non esplorata, oppure in una qualsiasi stanza non esplorata)...",
'chest_msg_1' : "Hai trovato un tesoro con dentro: {}",
'chest_msg_2' : "Hai trovato {} monete d'oro",
'chest_msg_3' : "Putroppo hai fatto scattare un trabocchetto. Se provare a disinnescarlo tirando un dado da combattimento: \nCon 1 scudo bianco non ti succede nulla e puoi ritentare la sorte; \nCon 1 scudo nero non ti succede nulla; \nCon 1 teschio perdi 1 punto corpo.",
'chest_msg_4' : "Non puoi credere ai tuoi occhi. Hai trovato un'arma:\n{}",
'traps_msg_1' : "Per fortuna non ci sono trabocchetti.",
'traps_msg_2' : "Mentre cerchi una porta segreta, senti il rumore di un meccanisco e un trabocchetto scatta proprio sotto ai tuoi piedi (trappola con lancia). Scopri se riesci ad evitarlo tirando un dado da combattimento:\n Con 1 scudo bianco passi indenne. \n Con uno scudo nero o un teschio cadi e perdi 1 punto corpo. Se sei caduto difendi con un dado in meno e uscirai solo facendo un valore superiore a 2 lanciando un D6",
'traps_msg_3' : "Un trabocchetto scatta, ma riesci a schivarlo. Spostati di una casella e metti una tessera crollo al posto tuo",
'traps_and_secret_doors_msg_1' : "Trabocchetti: \n{} \n\n Porte segrete: \n{} \n{}",
'fornitures_msg_1' : "Nella stanza trovi{}",
'fornitures_msg_2' : "Non c'è mobilio ma attento agli incantesimi!!!",
'monsters_msg_1' : "Preparati alla battaglia. Nella stanza trovi {}.",
'monsters_msg_2' : "Meno male. Nessun Mostro in vista!!!",
'monsters_msg_3' : "Il mostro errante in questa avventura è ",
'monsters_msg_4' : "Un mostro errante richiamato dai rumori appare alle tue spalle e ti attacca subito.",
'monsters_msg_5' : "La felicità per aver trovato il tuo obbiettivo dura poco...Senti un fetore e un gorgoglio strano provenire dalle tue spalle. Un mostro errante ti coglie di sorpresa e ti attacca subito; pensi: Anche oggi tocca fare gli straordinari!",
'monsters_msg_close' : " prepararsi alla battaglia! Imbracciate le armi. Combattete! Cooombatteeette!",
'monsters_msg_first_room' : "Tutto sembra tranquillo, ma il fetore del passaggio di qualche immonda creatura sembra molto chiaro. Meglio stare in allerta.",

'position_dict': {1: 'a sinistra',
                  2: 'a destra',
                  3: 'sul fondo',
                  4: 'al centro della stanza',
                  5: 'davanti a te'},


'treasures_card_dict' :  {1: "La pietra che avete sotto i piedi comincia a spostarsi e vi accorgete, troppo tardi, che si tratta di un trabocchetto. Cascate in uns buca piena di spuntoni e perdete 1 punto-corpo, ma al vostro prossimo turno potrete venire fuori e ricominciare a giocare normalmente.",
                     2: "La leggera pressione di un filo contro le gambe vi fa prima vacillare, poi girare...ma troppo tardi! Perdete 1 punto-corpo a causa di una freccia lanciata da una balestra nascosta dentro un muro",
                     3: "State cercando qualcosa e fate scattare inavvertitamente una trappola che vi scaglia addosso un dardo da dentro un muro. Perdete 1 punto-corpo.",
                     4: "Da uno scaffale polveroso tirate giù uno strano flacone. Ripulendolo vi accorgete che si tratta di una pozione magica. Potrete berla in qualsiasi momento ed essa vi permetterà, al vostro prossimo movimento, di tirare un numero di dadi doppio rispetto al normale. La carta va scartata dopo l'uso.",
                     5: "Avvolta in un mucchio di stracci trovate una bottiglietta colma di un liquido che si rivela essere una pozione risanante. Potrete berla in qualsiasi momento ed essa vi farà riguardagnare fino a 4 punti-corpo perduti. La carta va scartata dopo l'uso.",
                     6: "Scoprite una bottiglietta di color porpora. Contiene  una pozione rinforzante, che potrete bere in qualsiasi momento. Essa vi permetterà di tirare 2 dadi di combattimento in più durante la vostra prossima azione di attacco. La carta va scartata dopo l'uso.",
                     7: "In mezzo a un gruppo di vecchie bottiglie e di bricchi in terracotta, scoprite un flaconcino trasparente con dentro una pozione del recupero. Potrete berla in qualsiasi momento, dopo di che potrete lanciare per difendervi 2 dadi da combattimento in più la prossima volta che se ne presenterà l'occasione. La carta va scartata dopo l'uso.",
                     8: "Una sacca di pelle che pende da un muro contiene una pozione magica: l\'infuso Eroico, da bere prima dell\'attacco. Ogni Personaggio che beve la posizione sarà in grado per un turno solo, di condurre 2 attacchi invece di uno. La carta va scartata dopo l'uso.",
                     9: "Abbandonata e dimenticata in un angolo della stanza, trovate un'ampollina d'acqua benedetta. Potrete usarla al posto di un attacco dato che eliminerà qualsiasi nonmorto, sia esso Scheletro, Zombie o Mummia. Scartare la carta dopo l'uso.",
                     10 : "Dopo una assidua ricerca scoprite tanti piccoli mucchi d'oro sparsi in vari nascondigli. Perdete però la cognizione del tempo. Tirate allora un dado e moltiplicate il valore per 10 onde scoprire quante monete avete trovato. Saltate un turno. Riportate il totale sul retro del vostro foglio segna-punti e rimettete questa carta nel mazzo.",
                     11: "Dietro una pietra traballante trovate un borsellino di cuoio avvolto in un vecchio straccio. Lo aprite e e vi trovate 50 monete d'oro! Riportate la cifra sul retro del vostro foglio segna-punti e rimettete questa carta nel mazzo del tesoro.",
                     12: "Dopo aver frugato in vari cassetti trovate 20 monete d'oro. Riportate la cifra sul retro del vostro foglio segna punti e rimettete questa carta nel mazzo del tesoro.",
                     13: "Qualcuno ha stupidamente lasciato in vista una scatoletta contenente 25 onete d'oro. Segnate il valore sul retro del foglio segna punti e riponete la carta nel mazzo del tesoro.",
                     14: "Tra un mucchio di cianfrusaglie, vecchi cenci sporchi e bisunte coperte trovate 25 monete d'oro. Registrate il valore sul retro del foglio segna punti e riponete questa carta nel mazzo del tesoro.",
                     15: "Un magro bottino di sole 10 monete d'oro è stato trovato nel taschino di un logoro puzzolente gilet. Registrate il valore sul retro del foglio segna punti e riponete la carta nel mazzo del tesoro.",
                     16: "La fortuna è dalla vostra! In un piccolo scrigno, nascostro sotto ad una vecchia pelliccia, scoprite 100 monete d'oro. Dopo averle registrate sul retro del vostro foglio segna-punti rimettete la carta nel mazzo del tesoro.",
                     17: "Avete trovato una vecchia cassettina di legno tarlato che, all\'interno, è foderata di raso rosso e contiene gioielli del valore di 50 monete d'oro. Riportate la cifra sul retro del vostro foglio segna-punti e rimettete questa carta nel mazzo del tesoro.",
                     18: "Nascosta dentro la punta di un vecchio stivale trovate una pietra preziosa del valore di 50 monete d'oro. Segnate il valore sul retro del foglio segna-punti e riponete la carta nel mazzo del tesoro.",
                     19: "Mentre siete occupati nella ricerca un mostro vi soprende furtivamente alle spalle e vi attacca. Lo Stregone dovrà mettere il mostro errante, menzionato per questa avventura nel libro delle imprese, in una casella qualsiasi a te adiacente. Il mostro vi attaccherà subito.",
                     20: "Nonostante abbiate cercato ovunque non trovate ... niente!"},

'fornitures_dict': {1: "uno scrigno",
                    2: "un trono",
                    3: "un armadio",
                    4: "una libreria",
                    5: "un caminetto",
                    6: "un tavolo di tortura",
                    7: "un tavolo dell\'alchimista",
                    8: "un bancone del mago",
                    9: "una tomba",
                    10: "una rastrelliera",
                    11: "lungo il muro una porta aperta verso una zona inesplorata",
                    12: "lungo il muro una porta chiusa verso una zona inesplorata",
                    13: "tavolo"
                    },

'monsters_dict' : {1 : "un Goblin",
                   2 : "un Orco",
                   3 : "un Fimir",
                   4 : "uno Scheletro",
                   5 : "uno Zombie",
                   6 : "una Mummia",
                   7 : "un Guerriero del Caos",
                   8 : "un Gargoyle",
                   9 : "lo Stregone del Chaos"},

'weapons_dict' : {1: "Balestra",
                  2: "Spadino",
                  3: "Bastone",
                  4: "Ascia da battaglia",
                  5: "Armatura Corazzata",
                  6: "Ascia",
                  7: "Lancia",
                  8: "Borsa degli attrezzi",
                  9: "Elmo",
                  10: "Scudo",
                  11: "Spadone",
                  12: "Maglia di ferro"},

  'btn_1':"Come è fatto il corridoio",
  'FIELD_BOX_1': "Esplora un nuovo corridoio",
  'btn_2':"Scopri come è fatta la stanza",
  'TXT_1': "Nr. caselle della stanza (min. 6)",
  'TXT_2': "Esplora una nuova Stanza",
  'btn_3':"Ci sono tesori?",
  'TXT_3':'Esplora la stanza e i suoi mobili',
  'TXT_4': "Turno",
  'TXT_5': "1",
  'btn_4':"Cosa contiene?",
  'btn_5':"Ci sono mostri nella stanza?",
  'btn_6':"Ci sono trabocchetti o porte segrete?",
  'btn_7':"Nuovo turno",
  'aux_msg_1': 'Una porta ti conduce verso una zona inesplorata o ancora senza accessi. {}',
  'aux_msg_2': 'Nella penombra vedi',
  'aux_msg_3': 'La luce di alcune fiaccole accese illumina a mala pena i muri e vedete',
  'aux_msg_4': 'Da una finestra entra della luce che illumina',
  'aux_msg_5': 'Attendi che la vista si adatti al buio e vedi',
  'aux_msg_6': 'La stanza è spoglia e solo muffa e sangue arredano le sue pareti.',
  'aux_msg_7': 'Siete tornati sui vostri passi e un rumore sinistro vi accoglie...cosa può essere?',
  'aux_msg_8': 'Un ticchettio sordo e una freccia parte dal muro verso di te! Per evitare la freccia difenditi lanciando un dado da combattimento per ogni punto mente che hai. (ATTENZIONE: se hai già cercato trabocchetti qui ignora il messaggio).',
  'aux_msg_9': 'Attirato dai rumori ti ritrovi davanti {} (Metti la miniatura fino a 4 caselle dall\'eroe)',
  'aux_msg_10': 'Fino a qui tutto tranquillo...',
  'aux_msg_11': 'Per ora nessun problema... ma attento ai trabocchetti!!!',
  'aux_msg_12': 'I mostri si preparano alla battaglia',
  'end_msg_1' : 'La via d\'uscita! Noti una pietra spostata nel muro e toccandola, un rumore di ingranaggi apre una voragine nel pavimento. Hai trovato le scale per uscire!',
  'monsters_msg_intro': 'Prendi tutto il tuo coraggio e guardi dentro. Ecco cosa vedi:\n',


  'combat_value_dict'  : {
            'goblin'        : 15,
            'orc'           : 16,
            'fimir'         : 17,
            'zombie'        : 10,
            'skeleton'      : 11,
            'mummy'         : 12,
            'chaos_warrior' : 17,
            'gargoyle'      : 19,
            'chaos_wizard'  : 15
                            },


  'monster_name_conversion_dict'  : {
                                    'goblin'        : 'Goblin',
                                    'orc'           : 'Orco',
                                    'fimir'         : 'Fimir',
                                    'skeleton'      : 'Scheletro',
                                    'zombie'        : 'Zombie',
                                    'mummy'         : 'Mummia',
                                    'chaos_warrior' : 'Guerriero del Chaos',
                                    'gargoyle'      : 'Gargoyle',
                                    'chaos_wizard'  : 'Stregone del Chaos'
                                    },


  'monster_name_reconversion_dict'  : {
                                    'Goblin'        : 'goblin',
                                    'Orco'          : 'orc',
                                    'Fimir'         : 'fimir',
                                    'Scheletro'     : 'skeleton',
                                    'Zombie'        : 'zombie',
                                    'Mummia'        : 'mummy',
                                    'Guerriero del Chaos' : 'chaos_warrior',
                                    'Gargoyle'      : 'gargoyle',
                                    'Stregone del Chaos' : 'chaos_wizard'
                                    },

 'forniture_name_conversion_dict'  : {
                                    'chest'          : 'Scrigno',
                                    'throne'         : 'Trono',
                                    'wardrobe'       : 'Armadio',
                                    'bookcase'       : 'Libreria',
                                    'chimney'        : 'Caminetto',
                                    'torture_table'  : 'Tavolo di tortura',
                                    'alchemist_desk' : 'Scrivania dell\'Alchimista',
                                    'wizard_counter' : 'Bancone del mago',
                                    'tomb'           : 'Tomba',
                                    'weapon_rack'    : 'Rastrelliera',
                                    'open_doors'     : 'Porta aperta',
                                    'closed_doors'   : 'Porta chiusa',
                                    'table'          : 'Tavolo'
                                    },


  'forniture_name_reconversion_dict'  : {
                                     'Scrigno'                  : 'chest' ,
                                     'Trono'                    : 'throne',
                                     'Armadio'                  : 'wardrobe' ,
                                     'Libreria'                 : 'bookcase',
                                     'Caminetto'                : 'chimney',
                                     'Tavolo di tortura'        : 'torture_table',
                                     'Scrivania dell\'Alchimista': 'alchemist_desk',
                                     'Bancone del mago'         : 'wizard_counter',
                                     'Tomba'                    : 'tomb',
                                     'Rastrelliera'             : 'weapon_rack',
                                     'Porta aperta'             : 'open_doors',
                                     'Porta chiusa'             : 'closed_doors',
                                     'Tavolo'                   : 'table'                                     },

  'id_fornitures_convertion_dict' : {
                                    'chest'          : 1,
                                    'throne'         : 2,
                                    'wardrobe'       : 3,
                                    'bookcase'       : 4,
                                    'chimney'        : 5,
                                    'torture_table'  : 6,
                                    'alchemist_desk' : 7,
                                    'wizard_counter' : 8,
                                    'tomb'           : 9,
                                    'weapon_rack'    : 10,
                                    'open_doors'     : 11,
                                    'closed_doors'   : 12,
                                    'table'          : 13
                                   },

  'treasures_random_type' : { 'chest'          : ["Uno scrigno pieno di gioielli del valore di 200 monete d'oro.",
                                                  "Tra varie cianfrusaglie notate un luccichio sul fondo. Avete trovato uno Spadino. Prendete la relativa carta e annotatevi il valore di attacco.",
                                                  "Aprite lo scrigno e scoprire sfortunatamente che qualcuno è passato prima di voi, a parte un straccio che protegge una fiala (Si tratta di una pozione curativa per 2 punti corpo).",
                                                  "Un forziere ricolmo d'oro! Sono 500 monete d\'oro ma se deciderete di trasportarle dovrete muovermi con un dado in meno. A te la scelta!"],
                              'throne'         : ["Frugate nelle imbottiture e scovate 25 monete d'oro. Un magro bottino ma meglio di niente...",
                                                  "Il trono sembra mal ridotto e il legno infradiciato, ma vi accorgete che sopra allo schienale è incastonata una gemma del valore di 150 monete d'oro",
                                                  "Frugate ovunque e alla fine vi accorgete di uno scomparto segreto nel poggiolo. Trovate un pugnale da lancio con +1 punto di attacco da vicino e +2 se lo lanciate.",
                                                  "Dopo un\'estenuante ricerca decidete di sedervi e ... avvertite un click dietro allo schienale: avete trovato uno scomparto segreto con una pozione di coraggio da +2 dadi in attacco."],
                              'wardrobe'       : ["Tra gli scaffali dell\'armadio trovate una pozione di cura che vi permette di recuperare 2 punti corpo",
                                                  "Trovate uno scomparto segreto nell\'armadio che continee una fiala: si tratta di acqua benedetta in grado di uccidere un non-morto.",
                                                  "Una custodia voluminosa attira la vostra attenzione: la aprite con cautela e...meraviglia! Avete trovato una sborsa degli attrezzi che vi farà ritirare un dado da combattimento a scelta nel caso cadiate in una trappola.",
                                                  "Mentre cercate dentro all\'armadio fate scattare un meccanismo. L\'armadio si sposta e vi rivela una porta segreta"],
                              'bookcase'       : ["Un voluminoso tomo contiene tantissime formule utili. Purtroppo non c\'è tempo per studiarle tutte: vi appuntate una formula per guarire un vostro compagno di avventura con +1 punto corpo.",
                                                  "Non c'è tempo per indugiare tra questi polverosi libri. Ne prendete un po' sperando che valgano qualcosa. Alla fine dell\'avventura tirate due D6 e moltiplicate il valore per 10: sarà il vostro guadagno per rivendere i libri al vecchio mercato di Aman Sur.",
                                                  "Cercando tra i libri un grosso tomo rosso scuro attira la vostra attenzione: tirandolo a voi fa scattare un meccanismo che rivela una porta (mettetela preferibilmente verso una stanza inesplorata o ancora senza accessi"],
                              'chimney'        : ["Un meccanismo nastosco nel camino fa aprire un porta segreta che vi conduce in una stanza inesplorata o ancora senza accessi",
                                                  "Appoggiata sul caminetto trovate una fiala con all\'interno dell\'elisir del coraggio che vi danno +2 dadi da combattimento al prossimo scronto.",
                                                  "Tra i tizzoni ardenti notate una pergamena sbruciacchiata: è una mappa che vi conduce ad un tesoro. La mappa recità così: trova la libreria dell\'alchimista, lì vi è una gemma di inestimabile valore. Il primo che trova e arriva ad una casella adiacente ad una libreria o fa ritorno ad una libreria già trovata, conquista la gemma da 500 monete d'oro"],
                              'torture_table'  : ["Hai trovato una spada arrugginita (+ 1 dado da combattimento in attacco)",
                                                  "Tra le ossa del povero sventurato, hai trovato un antico scudo nanico molto pesante ammaccato (+2 dadi in difesa e 1 dado di movimento in meno se non sei un nano)."],
                              'alchemist_desk' : ["Una pozione di guarigione (+ 4 punti corpo)",
                                                  "Una pozione di guarigione (+ 1 punto corpo)",
                                                  "Una pozione di difesa (+ 3 dadi in difesa)"],
                              'wizard_counter' : ["Un antico pugnale sacrificale giace sul tomo appoggiato sul bancone. (+1 dado da combattimento in attacco)"],
                              'tomb'           : ["Sposti con forza il coperchio della tomba e al suo interno trovi uno spadone un po\' arrugginito. (se vorrai tenerlo otterrai +2 dadi da comabttimento, ma sottrai -2 dai prossimi movimenti",
                                                  "Non c\'è tempo per cercare altro: stacchi una gemma dalla tomba (+30 monete d'oro)"],
                              'weapon_rack'    : ["Le armi nella rastrelliera sono quasi tutte arrugginite a parte una balestra (+1 dado in attacco da lontano)",
                                                  "Scegli tra uno scudo (+ 1 dado da combattimento in difesa) e una piccola daga affilata (+2 dadi da combattimento in attacco)"],
                              'table'          : ["Un pugno di monete giace sul tavolo dall\'ultima partita a dadi di qualche orco (+5 monete d\'oro)",
                                                  "Sotto al tavolo trovi uno scudo (+1 dado da combattimento in difesa)"],
                              'open_doors'     : ["La porta è aperta solo in parte e ti accorgi che è incastrata in qualcosa che giace sul pavimento: si tratta di un vecchio coltello da lancio. Da vicino non vale nulla, ma lo potrai usare per lanciarlo contro un mostro, infliggendogli un danno di 1 punto corpo.",
                                                    "Osservi da vicino la porta già spalancata: qualcuno ha lasciato appoggiato alla maniglia un sacchetto di cuoio: contiene una pozione di difesa: +2 dadi da combattimento in difesa al prossimo combattimento."],
                              'closed_doors'   : ["La porta si rivela essere chiusa grazie ad un incantesimo: lancia un D6 per ogni punto mente che hai: se fai un numero superiore o uguale a 9 la porta si aprirà rivelandovi una nicchia che contiene una pozione curativa da +4 punti, ma se fallirai perderai un punto corpo (Dietro a questa porta non generare una stanza)",
                                                  "Ti attardi ad osservare la porta chiusa davanti a te: le borchie brillano e sembrano essere fatte di metalli preziosi: ma sai che non è tutto oro quel che luccica. Per verificare se c'è dell'oro e dell'argento da sgraffignare perdi tempo e ricavi un bottino da 25 monete d'oro. Il tuo turno finisce qui e salterai il turno successivo."]
                            },


  'attack_messages' : {1: ['Il mostro attacca l\'eroe {} oppure si muove verso l\'eroe più vicino e se può lo attacca.',
                           'Se ci sono nemici nel raggio di movimento, il mostro muove va verso l\'eroe {}. Se lo raggiunge lo attacca; altrimenti si muove verso l\'eroe più vicino e se può lo attacca.',
                           'Se il mostro è vicino ad un eroe lo attacca e poi si muove il più lontano possibile. Altrimenti non si muove.',
                           'Se il mostro non è solo, chiama a sè tutti i mostri (in base al contatto visivo) che attaccano contemporaneamente l\'eroe più vicino, altrimenti cerca di fuggire lontano.'],

                       2: ['il mostro non accenna a muoversi: potrebbe essere la vostra occasione',
                          'Il mostro cerca di fuggire lontano.', 'Il mostro cerca di bloccare la via di fuga agli eroi. Se finisce vicino ad un eroe non lo attacca, blocca solo la fuga.',
                          'Il resta a sorvegliare il suo antro e non si sposta.'],

                       3: ['Il mostro con un rapido movimento raccoglie dei sassi da terra e te li scaglia in faccia infliggendoti 1 punto ferita (Ti difendi con un dado da combattimento)',
                           'Il mostro scarta di lato e ti coglie di sorpresa attancandoti (Lancia un dado da combattimento in attacco per il mostro. L\'eroe si difende normalmente.)']
                           },

  'choice_dict' : {1:'più vicino {}',
                   2:'più lontano {}',
                   3: 'con meno punti corpo {}',
                   4: 'con più punti corpo {}',
                   5: 'con meno dadi da difesa {}'
                   },

  'monster_direction_dict' : {1:'alla sua sinistra',
                              2:'alla sua destra',
                              3: 'dietro di lui',
                              4: 'davanti a lui'},

  'missions_dict' : { 1: ["Il maniero di Hogarth", "Nelle terre di Hogarth, in un maniero abbandonato, si trova nascosto in un sotterraneo un antico laboratorio. Dovrai recuperare un talismano che il potente necromante tiene nascosto da qualche parte. Trova il laboratorio e cerca di sopravvivere tornando alle scale!!! (Metti le scale, una porta chiusa verso il corridoio e gli eroi nell\'angolo del tabellone in alto a destra."],
                      2: ["Il gioiello di Eriamar", "Il re Volgarth (discendente di Eriamar) per recuperare il gioiello del suo antenato, donerà la spada -Morte degli Orchi- a colui che gli riporterà l\'antico manufatto del suo antenato, sottrandolo dalla tomba del leggendario Eriamar, re barbaro dei tempi antichi; il gioiello si dice che giaccia sulla sua tomba, in fondo ad un profondo intrico di cunicoli. Vai nella fortezza di Gurmardath, cerca la tomba dell\'antico re e recupera il gioiello. Metti le scale al centro del tabellone con gli eroi e 4 porte chiuse al centro di ogni muro; per vincere dovrai trovare la tomba e ... ."],
                      3: ["Il Bastione di Oropher", "Un grande pericolo si annida nel Bastione di Oropher. Un Mago del Chaos ha evocato un Gargoyle per riprendere il controllo sulle terre circoscanti. Recati al bastione, trova e uccidi il Gargoyle e il suo evocatore, ma attento: si dice che se il padrone e la sua nefasta creatura sono insieme, la loro furia raddoppia. Se la speranza ti sta abbandonando sappi che in una segreta, lo Stregone del Chaos ha nascosto la Lama degli spiriti, la sua nemesi. Trovala prima che lo stregone del Chaos trovi te!!!\n##################\nObbiettivo: Recupera la Lama degli Spiriti, uccidi lo Stregone del Chaos e il Gargoyle e torna alle scale. Metti le scale e gli eroi in una stanza da 6 caselle con una porta chiusa su un corridoio. \nRegole: Il Mago del Chaos si muove di 5 caselle, ha 2 dadi di attacco e uno di difesa. Possiede i tre incantesimi di fuoco che userà nei suoi primi 3 attacchi: lancia un D6: 1-4 Palla di Fuoco, 2-5 Coraggio; 3-6 Fiamma d\'ira. Se lo stregone del Chaos e il Gargoyle sono in contatto visivo attaccano 2 volte per turno."],
                      4: ["Caccia alla Corazza di Borin", "Il re Asaroth ha ordinato di recuperare la corazza di Borin. I suoi maghi hanno scoperto che si trova all\'interno della Rocca di Balagar e hanno individuato un\'antica porta segreta per intruforlarsi nel maniero. Cerca la Corazza, recuperala ed esci vivo dalla Rocca. Collaca una porta segreta sul bordo esterno del pannello, al centro del lato con la scritta HEROQUEST con gli eroi pronti ad entrare; per vincere dovrai uscire da questa porta con la corazza."]
                     },

  'specials_rooms' : {1: [[1,1,3,7], "Hai trovato la stanza di Hogarth, necromante della dinastia di Hamasul che qui ha il suo laboratorio. Metti sul fondo due scrigni, a sinistra il tavolo dell\'alchimista e un armadio a destra. Metti due Guerrieri del Chaos a difesa della stanza. Sconfiggendo i due mostri riuscirai ad aprire l\'armadio e far apparire il Talismano di Lore. (Se i mostri sono già impiegati sul tabellone spostali qui)"],
                      2: [[9], "Hai trovato la catacomba in cui riposa Eriamar della dinastia di Hamasul. Senti arrivare un tonfo sordo, come di un crollo e l\'angoscia ti attanaglia: ora hai la certezza che la via è chiusa (Rimuovi il tassello delle scale da dove sei partito). Improvvisamente ricordi cosa ti ha detto Mentor: \'Giovane eroe, ricordati che appena prenderai il gioiello, la tomba ti rivelerà delle scale per uscire, ma attento agli spettri che difendono la tomba\'. Finalmente le sue parole diventano chiare: Metti la tomba in fondo alla stanza difesa da 3 scheletri, poi colloca nel corridoio 2 mummie e 2  zombie (se i mostri sono già impiegati sul tabellone spostali qui). Per fuggire recupera il gioiello arrivando ad una casella adiacente la tomaba che si sposterà rivelandoti le scale. Il primo eroe che riesce nell\'impresa avrà in premio la Morte degli Orchi."],
                      3: [[8], "Hai finalmente trovato l\'altare sacro dello Stregone del Chaos, ma ... Una misteriosa forza ti risucchia nella stanza (metti tutti gli eroie i mostri  che si trovano nel raggio di 4 caselle dalla porta dentro alla stanza e togli la porta). Sulle pagine del libro aperto un potente incantesimo tiene la Lama degli Spiriti celata agli occhi degli umani. Prova a spezzare l\'incantesimo che ti intrappola nella stanza e ti tiene celata la Lama degli Spiriti: in ogni turno lancia 2D6 e somma il risultato ai tuoi punti mente: con un valore superiore a 10 libererai la Lama degli Spiriti e farai riapparire la porta. \n###########\nATTENZIONE:se dopo 4 tentativi non sarai riuscito nell\'impresa l\'incantesimo della stanza evocherà lo spirito dello Stregone del Chaos che si materializzerà nella stanza (anche se lo avevi già ucciso) con ma con solo 4."],
                      4: [[10, 13],"Finalmente hai trovato l\'armeria della Rocca di Balagar. La Corazza di Borin è alla tua portata ma, nonappena cerchi di entrare 2 Guerrieri del Chaos appaiono nella stanza per impedirti di prenderla (Metti la rastrelliera con accanto un tavolo sul fondo della stanza e 2 Guerrieri del Chaos tra te e l\'armeria (Se i mostri sono impegnati altrove, spostali qui). Per conquistare la corazza arriva con un eroe vicino alla rastrelliera. Una volta presa la Corazza scappa dalla porta segreta da cui sei entrato."]},

  'monster_class'  : {1 : ['orc'],
                      2 : ['not_dead', 'magical'],
                      3 : ['not_dead', 'magical'],
                      4 : ['orc']},

  'monster_types'  : ['orc','not_dead','magical']

}


# Serializing json
json_object = json.dumps(data, indent = 4)
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)



