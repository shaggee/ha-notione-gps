# Changelog

All notable changes to this project. 🇵🇱 Polska wersja pod każdą wersją angielską.

## [0.1.6] – 2026-10-13

**EN**

### Added
- **Theft alarm trigger** option *Device changes location* (`POSITION`) – now always available in the list
- README rewritten in English and Polish with all features, device settings and automation examples

**PL**

### Dodano
- Opcja **Powiadomienie alarmu, gdy**: *Urządzenie zmieni lokalizację* (`POSITION`) – teraz zawsze dostępna na liście
- README przepisane po angielsku i po polsku – wszystkie funkcje, ustawienia lokalizatora i przykłady automatyzacji

## [0.1.5] – 2026-10-13

**EN**

### Added
- **Theft alarm all day** switch
- **Theft alarm start / end** time entities (used when "all day" is off)
- **Theft alarm trigger** select. Known value: *Device detects movement* (`MOVEMENT`). Any other value set in the app (e.g. *Device changes location*) is shown as-is so it can be mapped in a later release.

### Changed
- Speed alarm threshold limited to the values offered by the app: 40–140 km/h in steps of 10
- "Theft alarm sound" renamed to **Alarm sound on phone** (it plays on the phone, not on the tracker)

**PL**

### Dodano
- Przełącznik **Alarm całą dobę**
- Godziny **Początek alarmu / Koniec alarmu** (działają, gdy „całą dobę” jest wyłączone)
- Lista **Powiadomienie alarmu, gdy**. Znana wartość: *Urządzenie wykryje ruch* (`MOVEMENT`). Inna wartość ustawiona w aplikacji (np. *Urządzenie zmieni lokalizację*) jest pokazywana tak, jak zwraca ją serwer, i zostanie opisana w kolejnej wersji.

### Zmieniono
- Próg alarmu prędkości ograniczony do wartości z aplikacji: 40–140 km/h co 10
- „Dźwięk alarmu” przemianowany na **Alarm dźwiękowy na telefonie** (dźwięk gra telefon, nie lokalizator)

## [0.1.4] – 2026-10-13

**EN**

### Added – device settings (same as in the notiOne app)
- **Select:** report interval when moving (10 s … 1 d), report interval when stationary (1 h / 6 h / 1 d)
- **Switch:** theft alarm, theft alarm sound, speed alarm, battery saving, allow turning off with button
- **Number:** speed alarm threshold (km/h), battery saving threshold (%)

Settings are read every 5 minutes. A change reads the current config, changes one field and writes the whole object back, exactly like the app does.

### Fixed
- Subscription, e-TOLL and refresh interval entities from 0.1.3 showed *unknown* (the fields live in `gpsDetails`)
- A long "moving" interval (e.g. 1 day) no longer slows polling down to that interval – the server-derived floor is capped at 60 s

**PL**

### Dodano – ustawienia lokalizatora (te same co w aplikacji notiOne)
- **Listy wyboru:** interwał raportowania w ruchu (10 s … 1 d), interwał raportowania w bezruchu (1 h / 6 h / 1 d)
- **Przełączniki:** alarm antykradzieżowy, dźwięk alarmu, alarm prędkości, oszczędzanie baterii, wyłączanie przyciskiem
- **Liczby:** próg alarmu prędkości (km/h), próg oszczędzania baterii (%)

Ustawienia są odczytywane co 5 minut. Zmiana odczytuje aktualną konfigurację, zmienia jedno pole i odsyła całość, tak samo jak aplikacja.

### Naprawiono
- Encje abonamentu, e-TOLL i interwału odświeżania z 0.1.3 pokazywały *nieznany* (te pola są w `gpsDetails`)
- Długi interwał w ruchu (np. 1 dzień) nie spowalnia już odpytywania do tej wartości – dolna granica wynikająca z serwera wynosi maksymalnie 60 s

## [0.1.3] – 2026-10-13

**EN**

### Added
- **Lost mode** binary sensor (`wanted` flag from the notiOne app), with the found message as an attribute
- **Last connection** timestamp sensor (`lastPairedTime`) – when the tracker last talked to the server, independent of the GPS fix
- Diagnostic sensors: **IMEI**, **Subscription** type, **Subscription end**, **Server refresh interval**
- Diagnostic binary sensors: **Subscription active**, **e-TOLL** (with service status attribute)
- EN/PL translations for all new entities

### Changed
- Polling never runs more often than the server's own `refreshIntervalSeconds`

**PL**

### Dodano
- Sensor binarny **Tryb zgubiony** (flaga `wanted` z aplikacji notiOne), z komunikatem dla znalazcy jako atrybutem
- Sensor czasu **Ostatnie połączenie** (`lastPairedTime`) – kiedy lokalizator ostatnio połączył się z serwerem, niezależnie od pozycji GPS
- Sensory diagnostyczne: **IMEI**, typ **Abonamentu**, **Koniec abonamentu**, **Interwał odświeżania serwera**
- Diagnostyczne sensory binarne: **Abonament aktywny**, **e-TOLL** (ze statusem usługi jako atrybutem)
- Tłumaczenia EN/PL dla wszystkich nowych encji

### Zmieniono
- Integracja nigdy nie odpytuje częściej niż `refreshIntervalSeconds` podany przez serwer

## [0.1.2] – 2026-10-13

**EN**

### Changed
- Phones registered in the notiOne app as beacons (`PHONE` / `BEACON_PHONE`) are no longer added as devices. The API returns no position or samples for them, so all their entities were empty.
- Devices that are no longer exposed are removed automatically (together with their entities) after updating and restarting Home Assistant.

**PL**

### Zmieniono
- Telefony zarejestrowane w aplikacji notiOne jako beacony (`PHONE` / `BEACON_PHONE`) nie są już dodawane jako urządzenia. API nie zwraca dla nich pozycji ani próbek, więc wszystkie ich encje były puste.
- Urządzenia, których integracja już nie obsługuje, są usuwane automatycznie (razem z encjami) po aktualizacji i restarcie Home Assistanta.

## [0.1.1] – 2026-10-13

**EN**

### Added
- Integration icon (`brand/icon.png`), shown in Home Assistant 2026.3 or newer.

**PL**

### Dodano
- Ikona integracji (`brand/icon.png`), widoczna w Home Assistant 2026.3 lub nowszym.

## [0.1.0] – 2026-10-13

**EN**

First public release of the unofficial notiOne GPS integration for Home Assistant.

- UI configuration (e-mail + password), re-authentication, configurable polling interval (default 20 s)
- One HA device per tracker on the account
- `device_tracker` with GPS position, accuracy, battery, speed and reverse-geocoded place
- Sensors: battery, temperature, humidity, speed, accelerometer state, place, last report, orientation, GPS SNR (disabled by default), last button press
- Binary sensors: motion, online, charging
- `notione_accelerometer_changed` event on every accelerometer state change
- English and Polish translations

**PL**

Pierwsze publiczne wydanie nieoficjalnej integracji notiOne GPS dla Home Assistanta.

- Konfiguracja z UI (e-mail + hasło), ponowne logowanie, ustawiany interwał odpytywania (domyślnie 20 s)
- Jedno urządzenie w HA na każdy lokalizator z konta
- `device_tracker` z pozycją GPS, dokładnością, baterią, prędkością i nazwą miejsca
- Sensory: bateria, temperatura, wilgotność, prędkość, stan akcelerometru, miejsce, ostatni raport, orientacja, GPS SNR (domyślnie wyłączony), ostatnie wciśnięcie przycisku
- Sensory binarne: ruch, online, ładowanie
- Zdarzenie `notione_accelerometer_changed` przy każdej zmianie stanu akcelerometru
- Tłumaczenia angielskie i polskie

[0.1.6]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.6
[0.1.5]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.5
[0.1.4]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.4
[0.1.3]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.3
[0.1.2]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.2
[0.1.1]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.1
[0.1.0]: https://github.com/shaggee/ha-notione-gps/releases/tag/v0.1.0
