her er hele word filen med notater og planlegging

Ideer for pygame  spill

Kortspill
Notater fra spilling:
Spilte balatro siden det er et kortspill
Jeg må finne på noe interessant mechanic for kortspillet mitt.

Ide:
Du spiller som en konspirasjonsteoretiker og cryptozoolog. Du har vært heldig og får betaling fra staten for et spesielt program for folk som deg.
Du har kort for forskjellige «cryptids» so du bruker for å slåss mot andre cryptids, jaktere og ville dyr fra skogen. Det er fem plasser du kan legge ned kortene og skapninger kommer sakte ut av skogen over tid. Alle kort har liv og skade, og kamp fungerer mye som i inscryption
Du har et «troverdighets-meter» som du må passe på å holde over et spesifikt eller flere spesifikke punkt. Å bruke kort koster troverdighet. Sterkere kort koster mer troverdighet og kort av skapninger som viste seg å være ekte gir deg mer troverdighet. Hvis du mister all troverdighet, får du ikke lenger penger fra staten og blir hjemløs (du taper). Du har i totalt 10 troverdighet. 
Du kan bruke forskjellige greier for å få tilbake troverdighet. Ting som dårlige kameraer og avis-nyheter.
Mulig mechanics senere: 
Mani: Jo lengre du kommer inn i spillet desto mer mani får du. Dette kommer til å gjøre spillet farligere, legge til ekstra mechanics og mer forvirrende kort. Kan også ha ekstra kraftige kort som også koster Mani å bruke.
Hver gang du slåss mot en skapning får du bevis av deres eksistens og hvis du får nok bevis kan du kjøpe den hos dyreselgeren.
Hav eller vann tiles, der du kan plassere havdyr.
Notater fra pre-beta-testing (på ark):
Louis: Likte ikke hoop snake. Ble sur på jegeren sin RNG (skill issue). Flere ting med fire hp for å overleve hp eller senke damage til jegeren
Konrad: Likte veldig godt loveland frog.




Kort:
Enkle Kort:
Jackalope:
https://en.wikipedia.org/wiki/Jackalope
Standard billig kort, kan muligens bli oppgradert senere med whiskey
Liv: 2
Skade: 1
Koster: 1 Troverdighet

Hoop Snake:
https://en.wikipedia.org/wiki/Hoop_snake
Liv: 1
Skade: 1
Kostnad: 2 troverdighet
Ruller: Skade øker med 1 for hver runde den er på banen

Hugag:
https://en.wikipedia.org/wiki/Hugag
Liv: 3
Skade: 2
Kostnad: 3 Troverdighet
Ball-Tailed cat:
https://en.wikipedia.org/wiki/Ball-tailed_cat
Liv: 2
Skade: 1
Kostnad: 2 Troverdighet
Haleslag: Dytter det den slår til venstre hvis det er plass der.
Thylacine:
https://en.wikipedia.org/wiki/Thylacine#Searches_and_unconfirmed_sightings
Liv: 1
Skade: 1
Kostnad: 1
Utryddet: Når spilt tjener du tilbake 2 troverdighet

Middels Kort:
Jersey Devil:

Fouke Monster:
https://en.wikipedia.org/wiki/Fouke_Monster#
Liv: 2
Skade: 4
Kostnad: 3

Cactus Cat:
https://en.wikipedia.org/wiki/Cactus_cat
Liv: 4
Skade: 1
Kostnad: 4
Forfriskende: Gir skapningen til venstre +2 liv hver runde
Hidebehind:
Liv: 5
Skade: 2
Kostnad: 2
Gjemsel: Når denne skapningen er skadet går den tilbake til hånden, den får ikke tilbake noe liv.
Loveland Frog:
https://en.wikipedia.org/wiki/Loveland_frog
Skunk Ape:
https://en.wikipedia.org/wiki/Skunk_ape

Vanskelige Kort:
Fiendtlige Kort:
Ulv:
Liv: 2
Skade: 2
Kanin:
Liv: 2
Skade: 1
Bjørn:
Liv: 4
Skade: 3
Hidebehind:
Liv: 5
Skade: 2
Gjemsel: Når denne skapningen blir angrepet gjemmer den seg i skogen igjen.
Jeger:
Liv: 6
Skade: 3 for nå, men kan senkes til 2
Gevær: Hver gang den angriper får den 



Sluttlogg:
Jeg logget ikke så mye gjennom prosjektet så jeg skriver dette her på slutten for å forklare hvordan alt fungerer

Den generelle ideen til spillet er et Inscryption (https://store.steampowered.com/app/1092790/Inscryption/) inspirert kortspill basert
på amerikansk folketro og kryptozoologi. Ideen er at spillet er satt på 70-80 tallet i amerika og du er en kryptozoolog som har fått betaling
fra staten for å bevise at skapningene eksisterer. For å spille kort koster det troverdighet, du tjener tilbake 2 troverdighet hver runde.

Gjennom spillet samler du flere kort og kan forandre på dine tidligere kort.
Det finnes fortsatt 2 debug keybinds i spillet som jeg brukte for å teste spillet.
hvis du trykker 1 trekker du et kort
hvis du trykker 2 gjør den at alle fiender gjør 0 skade og har 0 liv.
Trykk på space for å starte at kortene slåss.
Etter du har drept alle wavesene med fiender kommer et kart ned der du kan trykke på neste og bruke mushjulet for å bevege kartet opp og ned

Den grafiske stilen er basert på found-footage som ofte er tilknyttet til cryptozoologi. Kortet er polaroider fordi de skal liksom være bevis på at skapningene eksisterer. Tidligere var det pixel art, men jeg byttet til photoshopet bilder som jeg tenkte passet bedre.

Forklaring av koden:
Mesteparten av koden består av classes. Den viktigste er classen er kortene som inneholder all informasjon kortene trenger, som posisjon, stats og alt annet.
Det er en class for lanesene der man kan klare å plassere alle kortene.
Jeg lagde en timer class som kan kjøre funksjoner etter de er ferdig, som hovedsaklig er brukt for å animere kortene via et keyframes-aktig system.
Spillet er også delt opp i "Phases" som deler opp i input og rendering i slåss delen, kartet og butikkene. Selv om funksjonen for angrep heter "Attack Phase" er den ikke en phase i koden. 
En av de tingene jeg er mest stolt av at jeg gjorde var at jeg ville at tingene fra butikkfasen og slåssfasen skulle bli igjen på bakgrunnen når kartet er der, så istedenfor å måtte rendere alt og lage massevis av problemer tar spillet et screenshot og putter det som bakgrunnen. Dette leder til at spillet kræsjer noen sjeldne ganger fordi den ikke finner filen, selv når den sjekker at filen er der før den legger til bakgrunnen.

Fiender blir spawnet via pools og tokens. Dette var inspirert av systemet til Risk of Rain 2, der vi har en liste med fiender som kan spawnes og hvor mange tokens vi kan bruke for å spawne de. Dette har på spesifikt "Fourth Level" kræsjet noen sjeldne ganger, men fungerer ellers. Disse poolsene er tilkoblet til stagesene og inkluderer muligheten til å ha tvunget fiender. Jeg rakk ikke å ordentlig fikse et problem med tvungede fiender som er at når de spawner på nytt resettes ikke hp-en deres.
Ellers håper jeg at de 1100 linjene med koden kan forklare seg selv ihvertfall litt siden jeg er for lat for å skrive så mye mer.


Hvis jeg skulle jobbet lengre med prosjektet hadde jeg gjort dette:
1. Løse resten av bugsene i spillet
2. Flere vanskelighetsgrader, kort, fiender og generelt content.
3. Hvis jeg hadde spesielt god tid, vurdert å kode spillet igjen helt fra bunnen av (og hvis mulig kanskje i en ordentlig engine)



også feedback jeg fikk fra playtesting var bare løs bugs og spillet er gøy. ingenting mer å skrive om