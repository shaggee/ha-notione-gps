# notiOne GPS for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Validate](https://github.com/shaggee/ha-notione-gps/actions/workflows/validate.yml/badge.svg)](https://github.com/shaggee/ha-notione-gps/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/shaggee/ha-notione-gps)](https://github.com/shaggee/ha-notione-gps/releases)

Unofficial Home Assistant integration for **notiOne GPS / GPS Plus** trackers.
It logs in to the same cloud API used by the notiOne app and [panel.notione.com](https://panel.notione.com),
exposes every GPS tracker on the account as a device, and lets you change the tracker settings
(report intervals, theft alarm, speed alarm) straight from Home Assistant.

🇵🇱 [Polska wersja niżej](#polski)

> ⚠️ This project is not affiliated with or endorsed by notiOne / Notinote.
> It uses an undocumented API that may change without notice.

## Features

### Location and status

| Entity | Description |
|---|---|
| Device tracker | GPS position, accuracy, battery, speed, place |
| Battery, Temperature, Humidity, Speed | Tracker measurements |
| Accelerometer | `MOVE` / `STATIONARY` |
| Place | Reverse-geocoded street and city |
| Last report | Time of the last GPS fix |
| Last connection | When the tracker last talked to the server (also without a GPS fix) |
| Motion | On when moving (accelerometer or speed > 0) |
| Charging | Battery charging |
| Lost mode | Tracker reported as lost/stolen in the notiOne app |

### Diagnostics

Online, orientation, GPS SNR (disabled by default), last button press, IMEI,
subscription type, subscription end, subscription active, e-TOLL, refresh interval.

### Device settings (Configuration section of the device page)

Same options as **Configuration → Alerts** in the notiOne app. Changes are sent to the tracker
through the notiOne cloud; settings are read back every 5 minutes.

| Entity | Type | Values |
|---|---|---|
| Report interval when moving | select | 10 s, 1 min, 5 min, 10 min, 30 min, 1 h, 3 h, 6 h, 12 h, 1 d |
| Report interval when stationary | select | 1 h, 6 h, 1 d |
| Allow turning off with button | switch | |
| Theft alarm | switch | notify when the tracker moves |
| Alarm sound on phone | switch | |
| Theft alarm all day | switch | |
| Theft alarm start / end | time | used when "all day" is off |
| Theft alarm trigger | select | device detects movement / device changes location |
| Speed alarm | switch | |
| Speed alarm threshold | number | 40–140 km/h, step 10 |
| Battery saving, Battery saving threshold | switch, number | experimental – not shown in the app for every model |

### Other

- Phones registered in the notiOne app as beacons are skipped (the API returns no data for them)
- Event `notione_accelerometer_changed` fired whenever the accelerometer state changes
- Integration icon (Home Assistant 2026.3 or newer)
- English and Polish translations

## Installation

### HACS (recommended)

1. HACS → ⋮ → **Custom repositories**
2. Repository: `https://github.com/shaggee/ha-notione-gps`, type: **Integration**
3. Search for **notiOne GPS**, install it and restart Home Assistant

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=shaggee&repository=ha-notione-gps&category=integration)

### Manual

Copy `custom_components/notione` into `<config>/custom_components/` and restart Home Assistant.

## Configuration

Settings → Devices & services → **Add integration** → *notiOne GPS*, then log in with
your notiOne account.

[![Add integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=notione)

**Options:** polling interval in seconds (default 20, min 10, max 3600).
Polling is never faster than the tracker's own report interval (capped at 60 s),
because there would be no new data.

## Automation examples

Notify when the motorcycle starts moving:

```yaml
alias: Motorcycle moved
triggers:
  - trigger: event
    event_type: notione_accelerometer_changed
    event_data:
      to: MOVE
actions:
  - action: notify.mobile_app_phone
    data:
      message: "{{ trigger.event.data.name }} is moving!"
```

Event data: `device_id`, `name`, `from`, `to`.

Entity IDs depend on the HA language – check yours on the entity page.

Report every 10 s while away, every 5 min at home (saves battery):

```yaml
alias: notiOne report interval
triggers:
  - trigger: state
    entity_id: person.me
actions:
  - action: select.select_option
    target:
      entity_id: select.notione_gps_5913_report_interval_when_moving
    data:
      option: "{{ '5 min' if trigger.to_state.state == 'home' else '10 s' }}"
```

## Requirements

- Home Assistant 2025.2 or newer
- Integration icon: Home Assistant 2026.3 or newer (HACS itself does not show local icons yet)

## Troubleshooting

```yaml
logger:
  logs:
    custom_components.notione: debug
```

Changelog: [CHANGELOG.md](CHANGELOG.md)

---

## Polski

Nieoficjalna integracja Home Assistant dla lokalizatorów **notiOne GPS / GPS Plus**.
Loguje się do tego samego API, z którego korzysta aplikacja notiOne i [panel.notione.com](https://panel.notione.com),
dodaje każdy lokalizator GPS z konta jako urządzenie i pozwala zmieniać jego ustawienia
(interwały raportowania, alarm antykradzieżowy, alarm prędkości) bezpośrednio z Home Assistanta.

> ⚠️ Projekt nie jest powiązany z notiOne / Notinote. Korzysta z nieudokumentowanego API,
> które może się zmienić bez uprzedzenia.

### Funkcje

#### Lokalizacja i stan

| Encja | Opis |
|---|---|
| Tracker urządzenia | Pozycja GPS, dokładność, bateria, prędkość, miejsce |
| Bateria, Temperatura, Wilgotność, Prędkość | Pomiary lokalizatora |
| Akcelerometr | `MOVE` / `STATIONARY` |
| Miejsce | Ulica i miasto |
| Ostatni raport | Czas ostatniej pozycji GPS |
| Ostatnie połączenie | Kiedy lokalizator ostatnio połączył się z serwerem (także bez pozycji GPS) |
| Ruch | Włączony, gdy lokalizator jest w ruchu (akcelerometr lub prędkość > 0) |
| Ładowanie | Ładowanie baterii |
| Tryb zgubiony | Lokalizator zgłoszony w aplikacji jako zgubiony/skradziony |

#### Diagnostyka

Online, orientacja, GPS SNR (domyślnie wyłączony), ostatnie wciśnięcie przycisku, IMEI,
typ abonamentu, koniec abonamentu, abonament aktywny, e-TOLL, interwał odświeżania.

#### Ustawienia lokalizatora (sekcja Konfiguracja na stronie urządzenia)

Te same opcje co w aplikacji notiOne w **Konfiguracja → Alerty**. Zmiany trafiają do lokalizatora
przez chmurę notiOne; ustawienia są odczytywane co 5 minut.

| Encja | Typ | Wartości |
|---|---|---|
| Interwał raportowania w ruchu | lista | 10 s, 1 min, 5 min, 10 min, 30 min, 1 h, 3 h, 6 h, 12 h, 1 d |
| Interwał raportowania w bezruchu | lista | 1 h, 6 h, 1 d |
| Wyłączanie przyciskiem | przełącznik | |
| Alarm antykradzieżowy | przełącznik | powiadomienie, gdy lokalizator jest w ruchu |
| Alarm dźwiękowy na telefonie | przełącznik | |
| Alarm całą dobę | przełącznik | |
| Początek / Koniec alarmu | godzina | gdy „całą dobę” jest wyłączone |
| Powiadomienie alarmu, gdy | lista | urządzenie wykryje ruch / urządzenie zmieni lokalizację |
| Alarm prędkości | przełącznik | |
| Próg alarmu prędkości | liczba | 40–140 km/h co 10 |
| Oszczędzanie baterii, Próg oszczędzania baterii | przełącznik, liczba | eksperymentalne – nie każdy model pokazuje je w aplikacji |

#### Pozostałe

- Telefony zarejestrowane w aplikacji jako beacony są pomijane (API nie zwraca dla nich danych)
- Zdarzenie `notione_accelerometer_changed` przy każdej zmianie stanu akcelerometru
- Ikona integracji (Home Assistant 2026.3 lub nowszy)
- Tłumaczenia angielskie i polskie

### Instalacja przez HACS

1. HACS → ⋮ → **Custom repositories**
2. Adres: `https://github.com/shaggee/ha-notione-gps`, typ: **Integration**
3. Wyszukaj **notiOne GPS**, zainstaluj i zrestartuj Home Assistanta
4. Ustawienia → Urządzenia i usługi → **Dodaj integrację** → *notiOne GPS*

### Instalacja ręczna

Skopiuj `custom_components/notione` do `<config>/custom_components/` i zrestartuj HA.

### Opcje

Interwał odpytywania w sekundach (domyślnie 20, min. 10, maks. 3600).
Integracja nie odpytuje częściej niż lokalizator raportuje (maks. 60 s), bo nie byłoby nowych danych.

### Przykłady automatyzacji

Powiadomienie, gdy motocykl ruszy:

```yaml
alias: Motocykl w ruchu
triggers:
  - trigger: event
    event_type: notione_accelerometer_changed
    event_data:
      to: MOVE
actions:
  - action: notify.mobile_app_telefon
    data:
      message: "{{ trigger.event.data.name }} jest w ruchu!"
```

Identyfikator encji zależy od języka HA – sprawdź go na stronie encji.

Raportowanie co 10 s poza domem, co 5 min w domu (oszczędza baterię):

```yaml
alias: notiOne interwał raportowania
triggers:
  - trigger: state
    entity_id: person.ja
actions:
  - action: select.select_option
    target:
      entity_id: select.notione_gps_5913_interwal_raportowania_w_ruchu
    data:
      option: "{{ '5 min' if trigger.to_state.state == 'home' else '10 s' }}"
```

### Wymagania

- Home Assistant 2025.2 lub nowszy
- Ikona integracji: Home Assistant 2026.3 lub nowszy (sam HACS nie pokazuje jeszcze lokalnych ikon)

### Rozwiązywanie problemów

```yaml
logger:
  logs:
    custom_components.notione: debug
```

Lista zmian: [CHANGELOG.md](CHANGELOG.md)

## License

MIT
