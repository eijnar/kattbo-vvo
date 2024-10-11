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

Osmakliga omstruktureringar, en helt ny värld. Jag gjorde om allt från början helt enkelt.

### filebeat.yml

```
filebeat.inputs:
- type: filestream
  enabled: true
  paths:
    - /home/eijnar/projects/kattbo-vvo-web/api/logs/*.log*
  fields:
    log_type: api_log
  json.keys_under_root: true
  json.add_error_key: true
  json.overwrite_keys: true

processors:
  - decode_json_fields:
      fields: ["message"]
      target: ""
      overwrite_keys: true
  - timestamp:
      field: "timestamp"
      layouts:
        - '2006-01-02T15:04:05.000000Z'
        - '2006-01-02T15:04:05.000Z'
        - '2006-01-02T15:04:05Z'
        - '2006-01-02T15:04:05.000+0200'
        - '2006-01-02T15:04:05+0200'
        - '2006-01-02T15:04:05.000000-07:00'

filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false

output.elasticsearch:
  hosts: [""]
  protocol: "https"
  ssl.certificate_authorities: [""]
  #api_key: "sample_api_key"
  username: ""
  password: ""

logging.level: debug
logging.selectors: ["*"]

# Optionally, specify output for logs if you want to save them to a file
logging.to_files: true
logging.files:
  path: /home/eijnar/projects/kattbo-vvo-web/filebeat/log/
  name: filebeat
  keepfiles: 7
  permissions: 0644

```
