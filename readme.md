# Docker Compose ja PostgreSQL

Tämän tehtävän tavoitteena on perehtyä Dockerin ja Docker Compose:n keskeisiin käsitteisiin ja ominaisuuksiin, kuten volyymit, ympäristömuuttujat ja palveluriippuvuudet. Samalla pääsemme työskentelemään PostgreSQL:n ja pgAdminin kaltaisten oikeiden työkalujen kanssa.

Käsittelemme tässä tehtävässä [**PostgreSQL**-tietokantaa](https://hub.docker.com/_/postgres) ja [**pgAdmin**-hallintatyökalua](https://www.pgadmin.org/), mutta samoja periaatteita voidaan soveltaa myös muiden tietokantojen yhteydessä.

**Suositeltua taustamateriaalia:**

* [How to Use the Postgres Docker Official Image (docker.com)](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/)
* [`docker compose` CLI reference (docker.com)](https://docs.docker.com/reference/cli/docker/compose/)
* [Compose file reference (docker.com)](https://docs.docker.com/reference/compose-file/)
* [DevOps with Docker, part 2 (devopswithdocker.com)](https://devopswithdocker.com/category/part-2)
* [Docker Compose will BLOW your MIND!! (YouTube, NetworkChuck)](https://youtu.be/DM65_JyGxCo)

## Miksi Docker compose?

Docker Compose on usein parempi vaihtoehto kuin erillisten `docker run` -komentojen kirjoittaminen, erityisesti silloin, kun käynnistettäviä palveluita on useita. Docker compose yksinkertaistaa monimutkaisten ympäristöjen hallintaa yksittäisen YAML-tiedoston avulla. Tämä tekee ympäristön pystyttämisestä helpompaa ja vähemmän virhealttiista, kun kaikki konfiguraatiot ja riippuvuudet ovat yhdessä paikassa.

Docker Compose hallitsee volyymit ja verkot automaattisesti ja mm. liittää kaikki samaan tiedostoon määritellyt palvelut osaksi samaa verkkoa, jolloin ne voivat olla vuorovaikutuksessa keskenään. Saman YAML-tiedoston jakaminen esimerkiksi versionhallinnan kautta muiden kanssa on myös sujuvaa, ja se vähentää eroavaisuuksia eri kehittäjien kehitysympäristöissä sekä muissa ympäristöissä.


## PostgreSQL

PostgreSQL on suosittu avoimen lähdekoodin relaatiotietokanta, jota voidaan käyttää hyvin monenlaisissa eri käyttötarkoituksissa.

> *PostgreSQL, often simply "Postgres", is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards-compliance. As a database server, its primary function is to store data, securely and supporting best practices, and retrieve it later, as requested by other software applications, be it those on the same computer or those running on another computer across a network (including the Internet). It can handle workloads ranging from small single-machine applications to large Internet-facing applications with many concurrent users.*
>
> What is PostgreSQL? https://hub.docker.com/_/postgres

PostgreSQL löytyy valmiina Docker-imagena Docker Hub -konttirekisteristä: https://hub.docker.com/_/postgres. Tässä tehtävässä sinun tarvitsee vain hyödyntää valmista imagea ja tutustua sen dokumentaatioon.


## pgAdmin 4

**pgAdmin 4** on web-pohjainen graafinen hallintatyökalu PostgreSQL-tietokannan hallintaan. Sen avulla kehittäjät voivat suorittaa SQL-kyselyitä, tarkastella tietokantatauluja, sekä hallita käyttäjiä ja tietokannan asetuksia ilman tarvetta käyttää esimerkiksi komentorivityökaluja.

> *pgAdmin is a management tool for [PostgreSQL](https://www.postgresql.org/) and derivative relational databases such as [EnterpriseDB's](https://www.enterprisedb.com/) EDB Advanced Server. It may be run either as a web or desktop application. For more information on the features offered, please see the [Features](https://www.pgadmin.org/features/) and [Screenshots](https://www.pgadmin.org/screenshots/) pages.*
>
> What is pgAdmin 4? https://www.pgadmin.org/faq/

pgAdmin-työkalun kotisivulla löytyy tarkemmat ohjeet sen käyttämiseksi kontitettuna: https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html. Ohjesivu sisältää mm. eri ympäristömuuttujat, joiden avulla työkalu saadaan ottamaan yhteyttä juuri haluamaasi tietokantapalvelimeen. Docker Hub -konttirekisteristä osoitteesta https://hub.docker.com/dpage/pgadmin4 löytyy puolestaan virallinen pgAdmin-image.


# Tehtävä: tietokantapalvelimen sekä hallintakäyttöliittymän asennus

Kehittäessäsi sovellusta tarvitset usein tietokannan, jonka tiedot säilyvät pysyvästi ja johon voit helposti yhdistää. Tässä tehtävässä luot Docker Compose -tiedoston avulla ympäristön, jossa PostgreSQL toimii kontissa, tietokanta alustetaan haluttuun alkutilaan, data pysyy säilytettynä kontin elinkaaresta riippumatta ja pääset hallitsemaan tietokantaa pgAdminin avulla.

> [!NOTE]
> Tämän tehtävän Docker Compose -asetelma soveltuu hyvin **kehitysympäristöihin**, joissa tarvitset nopeasti käyttöön otettavan tietokannan. Tietokantojen kontittamisesta tuotantoympäristöissä on olemassa eriäviä näkemyksiä. Jotkut kannattavat konttien käyttöä tietokannoille tuotannossa, koska kontit ovat helposti siirrettäviä ja skaalautuvia. Toiset taas vastustavat ajatusta, sillä tietokannat saattavat vaatia monimutkaisempaa hallintaa ja suorituskykyä, mikä voi olla haaste konttipohjaisessa ympäristössä.
>
> Toisaalta pgAdmin on työkalu, jota käytetään tyypillisesti vain kehitysympäristöissä tai paikallisessa käytössä. Tuotannossa tietokantojen hallinta tehdään yleensä muilla tavoilla, kuten komentorivityökaluilla tai automatisoiduilla prosesseilla, eikä graafista käyttöliittymää välttämättä käytetä. Mikäli tuotantopalvelussa olisi käytössä pgAdmin tai vastaava hallintatyökalu, pääsyä siihen kannattaisi rajoittaa erityisen huolellisesti.

## docker-compose.yml

Tästä repositoriosta löytyy valmiiksi [docker-compose.yml](./docker-compose.yml)-tiedosto, johon kaikkien tehtävän osien ratkaisut kirjoitetaan. Kokeile ratkaisujesi toimivuutta aina ensin `docker compose up` -komennolla ja sulje palvelut `docker compose down`-komennolla ennen seuraavaa kokeilua. Löydät muut mahdolliset komennot [`docker compose`-komennon dokumentaatiosta](https://docs.docker.com/reference/cli/docker/compose/).

[docker-compose.yml](./docker-compose.yml)-tiedostosta löytyy valmiiksi kaksi palvelua: `postgres` ja `pgadmin`:

```yaml
services:
  postgres:
    image: postgres:latest
    container_name: database

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: database-admin
```

Molemmat palvelut perustuvat valmiiseen Docker-imageen. Palveluiden nimet (`postgres` ja `pgadmin`) ovat vapaasti valittavissa, ja palvelut voivat ottaa yhteyksiä toisiinsa näiden nimien avulla:

> *"By default, any service can reach any other service at that service's name."*
>
> https://docs.docker.com/compose/networking/#link-containers

`container_name` puolestaan määrittelee nimen, jolla voit itse suorittaa esimerkiksi Docker-komentoja käynnissä oleville konteille.


## Osa 1: porttien avaaminen (20 %)

PostgreSQL-kontti kuuntelee oletuksena porttia **5432** ja pgadmin4-kontti porttia **80**. Julkaise nämä portit konteista host-koneelle asettamalla [docker-compose.yml](./docker-compose.yml)-tiedostoon `ports`-määritykset molemmille palveluille.

> [!TIP]
> Voit käyttää host-koneella mitä vain portteja, niiden ei tarvitse olla samat kuin konttien sisäiset portit. Voit myös määritellä portit kuuntelemaan vain `127.0.0.1`-verkkoa, jolloin näiden konttien ei pitäisi näkyä koneesi ulkopuolelle.

Voit nyt kokeilla käynnistää palvelut `docker compose up`-komennolla, törmäät ainakin seuraavaan virheeseen:

> *You need to define the PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD or PGADMIN_DEFAULT_PASSWORD_FILE environment variables.*

Ennen palveluiden käyttämistä niille tuleekin määritellä ympäristömuuttujat, joita käsitellään seuraavaksi.


## Osa 2: ympäristömuuttujien asettaminen (20 %)

Toimiakseen oikein, sekä PostgreSQL että pgAdmin 4 tarvitsevat ympäristömuuttujia, kuten käyttäjätunnukset ja salasanat. Tutustu PostgreSQL:n Docker-imagen dokumentaatioon osoitteessa https://hub.docker.com/_/postgres sekä pgAdmin 4:n dokumentaatioon osoitteessa https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html ja määrittele [docker-compose.yml](./docker-compose.yml)-tiedostoon [`environment`-lohkot](https://docs.docker.com/reference/compose-file/services/), joista löytyy dokumentaatiossa mainitut vaaditut ympäristömuuttujat.

Voit nyt kokeilla käynnistää palvelut `docker compose up`-komennolla. Nyt sinulla pitäisi olla pääsy pgAdmin-kontin web-käyttöliittymään verkkoselaimesi avulla käyttämällä host-koneen porttia, jonka määrittelit aiemmin. Huomaa kuitenkin, että pgadmin-palvelun ensimmäinen käynnistys kestää melko kauan, joten odota vähintään kunnes terminaalissa kerrotaan, että se kuuntelee sisäisesti porttia 80.

Kokeile kirjautua sisään pgAdmin-työkaluun sähköpostiosoitteella ja salasanalla, jotka määrittelit ympäristömuuttujiin. Löydät ohjeita pgAdmin-työkalun käyttämiseksi hakukoneilla ja työkalun omasta dokumentaatiosta. Voit aloittaa esimerkiksi videosta [ pgAdmin Tutorial - How to Use pgAdmin (YouTube, Database Star)](https://youtu.be/WFT5MaZN6g4?feature=shared&t=160).

Kun otat pgAdmin-työkalulla yhteyden omaan PostgreSQL-palvelimeesi, muista käyttää yhteyttä muodostettaessa "host name"-kentässä palvelun nimeä, eli *postgres*.


## Osa 3: salaisuuksien hallinta .env-tiedoston avulla (20 %)

Salaisuuksien, kuten käyttäjätunnusten ja salasanojen, säilyttäminen suoraan Docker Compose -tiedostossa ei ole turvallista, sillä tiedosto on tarkoitus tallentaa versionhallintaan ja sitä on tarkoitus jakaa. Eri ympäristöissä tarvitaan usein myös eri muuttujia, joten myös toiminnallisesti on hyvä, jos muuttuvaa tietoa ei kovakoodata. Näiden ongelmien välttämiseksi ympäristömuuttujat tulee seuraavaksi siirtää `.env`-tiedostoon, jota ei lisätä versionhallintaan. `.env` onkin jo valmiiksi mainittuna tämän tehtävän [.gitignore](./.gitignore)-tiedostossa.

**Luo uusi .env-niminen tiedosto** tähän hakemistoon ja lisää sinne PostgreSQL-palvelun tarvitsemat salaisuudet:

```plaintext
POSTGRES_USER=myusername
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
```

**Päivitä docker-compose.yml-tiedosto** käyttämään ympäristömuuttujia `.env`-tiedostosta. Lisää `env_file`-lohko PostgreSQL-palvelulle ja korvaa kovakoodatut arvot ympäristömuuttujaviittauksilla:

```yaml
services:
  postgres:
    image: postgres:latest
    container_name: database

  environment:
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    POSTGRES_DB: ${POSTGRES_DB}

  env_file:
    - .env
```

Tee sama myös pgAdmin-palvelun salaisuuksille. Voit hyvin käyttää molemmissa palveluissa samaa .env-tiedostoa, tai halutessasi luoda erillisen tiedoston.


## Osa 4: volumet (2 kpl) (20 %)

PostgreSQL-tietokannan data täytyy säilyttää pysyvästi myös konttien uudelleenkäynnistyksen jälkeen. Tämä onnistuu käyttämällä Dockerin volumea, joka säilyttää tiedot host-järjestelmässä. Liitä siis kontin sisään polkuun `/var/lib/postgresql/data` volume, jossa tietokannan tiedot säilyvät myös mahdollisen kontin poistamisen jälkeen. Lue lisää esim. artikkelista [How to Use the Postgres Docker Official Image](https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/).

PostgreSQL mahdollistaa tietokannan alustamisen automaattisesti, kun kontti käynnistetään ensimmäistä kertaa. Tätä varten voidaan käyttää **initialization script** -ominaisuutta, jossa tietokantapalvelimen käynnistyksen yhteydessä ajetaan tietty SQL-skripti, joka lisää tietokantaan halutun datan:

> *"If you would like to do additional initialization in an image derived from this one, add one or more \*.sql, \*.sql.gz, or \*.sh scripts under /docker-entrypoint-initdb.d (creating the directory if necessary). After the entrypoint calls initdb to create the default postgres user and database, it will run any \*.sql files, run any executable \*.sh scripts, and source any non-executable \*.sh scripts found in that directory to do further initialization before starting the service."*
>
> Initialization scripts, https://hub.docker.com/_/postgres

Tässä tehtävässä haluamme lisätä tietokantapalvelimelle automaattisesti **Chinook-esimerkkitietokannan**, jonka luontiskripti löytyy valmiiksi tämän repositorion `sql`-hakemistosta. Liitä siis host-koneen `./sql`-hakemisto tietokantapalvelun sisään hakemistoksi `/docker-entrypoint-initdb.d/`. Tämän jälkeen sulje palvelut (`docker compose down`) ja käynnistä ne uudelleen (`docker compose up`). Tällä kertaa terminaaliin pitäisi ilmestyä lukuisia lokirivejä `postgres`-palvelusta, jossa kerrotaan, että tietokantaan luodaan tauluja ja rivejä.


### Chinook-esimerkkitietokanta

**Chinook** on esimerkkitietokanta, joka sisältää musiikkikaupan tietoja, kuten artisteja, albumeita, kappaleita ja asiakkaita. Se on suunniteltu tarjoamaan realistinen mutta yksinkertainen tietokantarakenne, joka on hyödyllinen SQL-kyselyiden ja tietokannan hallinnan harjoitteluun. Tässä tehtävässä Chinook-tietokantaa käytetään, koska sen sisältö on monipuolinen ja helposti ymmärrettävä, ja se mahdollistaa opiskelijoiden harjoitella tietokannan perustaitoja, kuten tietojen hakuamista ja analysointia, ilman tarvetta käsitellä liian monimutkaisia tai suuria tietomääriä.

Sinun ei tarvitse osata erityisiä SQL-komentoja tämän tehtävän suorittamiseksi, sillä tietokannan luontikäskyt ja tarvittavat komennot on annettu valmiina.


## Osa 5: toimiva lopputulos (20 %)

Lopuksi varmistamme, että kaikki vaiheet toimivat onnistuneesti, suorittamalla pgAdmin-työkalulla SQL-kyselyn, jossa etsitään kaikki sellaiset artistit, joiden minkä tahansa kappaleen nimessä esiintyy sana "hello" tai sana "world". Nämä voivat sijaita missä vain kohtaa kappaleen nimeä, jopa osana toista sanaa. Suorita seuraava kysely Chinook-tietokannassa, ja tallenna sen tuottamasta vastauksesta artistien nimet [tiedostoon hello_world.txt](./hello_world.txt).

```sql
select distinct artist.name
from artist
join album on artist.artist_id = album.artist_id
join track on album.album_id = track.album_id
where track.name like '%hello%' or track.name like '%world%';
```


# Lisenssit


## Docker

> "The Docker Engine is licensed under the Apache License, Version 2.0. See LICENSE for the full license text."
>
> "However, for commercial use of Docker Engine obtained via Docker Desktop within larger enterprises (exceeding 250 employees OR with annual revenue surpassing $10 million USD), a paid subscription
is required."
>
> https://docs.docker.com/engine/

## PostgreSQL

> "PostgreSQL is released under the PostgreSQL License, a liberal Open Source license, similar to the BSD or MIT licenses."
>
> https://www.postgresql.org/about/licence/


## pgAdmin

> "pgAdmin 4 is released under the PostgreSQL licence."
>
> https://www.pgadmin.org/licence/


## Chinook-tietokanta

Chinook-tietokannan on luonut [Luis Rocha](https://github.com/lerocha) ja se on lisensoitu [MIT-lisenssillä](https://github.com/lerocha/chinook-database/blob/master/LICENSE.md).


## Tämä oppimateriaali

Tämän tehtävän on kehittänyt Teemu Havulinna ja se on lisensoitu [Creative Commons BY-NC-SA -lisenssillä](https://creativecommons.org/licenses/by-nc-sa/4.0/).

Tehtävänannon, lähdekoodien ja testien toteutuksessa on hyödynnetty ChatGPT-kielimallia sekä GitHub copilot -tekoälyavustinta.