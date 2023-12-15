---
share: "true"
---


# Kättbo VVO hemsida

## Introduktion
I ett försök att förbättra kommunikationen och underlätta för jaktledarna i deras planeringsarbete så startade jag detta projekt efter första helgjakten efter ordinarie älgjakten jaktåret 2023/2024. Under arbetets gång utvecklades idéerna till att även inkludera andra delar av vilvårdsområdet och jaktlaget

Källkoden finns på [Github](https://www.github.com/eijnar/kattbo-vvo-web)
### Målet med hemsidan

 - Ett ställe att samla all information kring VVO & Kättbo Jaktlag.
	 - Mötesprotokoll
	 - ÄSO information
	 - Pass (karta med möjlighet till exportering till GPX)
	 - Övrig information
 - Förenkla kommunikation med hjälp av automatiska SMS och E-post
	 - Jaktplanering
	 - Mötes planering
	 - Övrig planering som hör till jakt
 - Registrering av fällt vilt för bättre och enklare statistik
 - Kalender med möjlighet till integration med telefon eller annan mjukvara
 - Passuppdateringar

## Teknisk dokumentation

### Övergripande beskrivning

Projektet startade som ett simpelt flask projekt (python). Under tiden migrerade vi till en början från MariaDB till PostgreSQL, då det sistnämnda har bättre stöd för geometrisk data. Senare introducerades Celery för att sköta bakgrunds funktioner för att avlasta front-end såsom utskick av sms och e-post. Framöver så är tanken att vi kommer sära på API delen till ett FastAPI projekt och migrera mer mot microservices
#### Dependencies

- Python 3.9+
- PostgreSQL
- RabbitMQ
## Versioner

För att se närmare teknisk beskrivning av versionerna kolla in [[Changelog|Changelog]]. 
En planering för version 0.2 som kommer vara den första officiella versionen finns. [[Version 0.2|Version 0.2]]

## Installation

För närvarande går detta att köra genom att starta det med python `python run.py` men också via docker-compose lokalt.

### docker-compose.yml

Vill man installera detta och testa lokalt behöver man sätta upp PostgreSQL och RabbitMQ. Detta då dessa inte finns med i `docker-compose.yml`. Det kan vara så att dessa tillkommer senare som alternativ. 

Efter detta måste man också skapa en .env och placera den i root katalogen. Denna skall ha följande inställningar:

``` bash
# General settings
UPLOAD_FOLDER=

# Mail settings
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_PORT=
MAIL_USE_SSL=
MAIL_SERVER=
MAIL_DEFAULT_SENDER_DEV=
MAIL_DEFAULT_SENDER_PROD=

# Flask WTF secret key
SECRET_KEY=

# Flask Security Too settings
SECURITY_PASSWORD_SALT=
SECURITY_PASSWORD_HASH=
SECURITY_REGISTERABLE=
SECURITY_CONFIRMABLE=
SECURITY_TRACKABLE=

# JWT Token settings
JWT_SECRET_KEY=
JWT_ALGORITHM=

# Database settings
SQLALCHEMY_DATABASE_URI_DEV=
SQLALCHEMY_DATABASE_URI_PROD=

# Celery settings
CELERY_BROKER_URL=
CELERY_BACKEND_URL=
```

### CD/CI

För att underlätta deployment av projektet så sköts detta via CD/CI och Github Actions. För att komma igång med denna behöver man sätta ovanstående parametrar i Github. `Settings -> Secrets and Variables -> Actions`

En runner körs lokalt och dokumentation för hur man sätter upp denna finns [[vvo.srv.kaffesump.se|här]]

