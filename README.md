# notiOne GPS for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)
[![Validate](https://github.com/shaggee/ha-notione-gps/actions/workflows/validate.yml/badge.svg)](https://github.com/shaggee/ha-notione-gps/actions/workflows/validate.yml)

Unofficial Home Assistant integration for **notiOne GPS / GPS Plus** trackers.
It logs in to the same cloud API used by [panel.notione.com](https://panel.notione.com)
and exposes every tracker on the account as a device with a location tracker and sensors.

🇵🇱 [Polska wersja niżej](#polski)

> ⚠️ This project is not affiliated with or endorsed by notiOne / Notinote.
> It uses an undocumented API that may change without notice.

## Features

- UI configuration (e-mail + password), re-authentication, configurable polling interval
- One HA device per tracker on the account
- `device_tracker` with GPS position, accuracy, battery, speed and reverse-geocoded place
- Sensors: battery, temperature, humidity, speed, accelerometer state, place, last report,
  orientation, GPS SNR (disabled by default), last button press
- Binary sensors: motion, online, charging
- Event `notione_accelerometer_changed` fired whenever the accelerometer state changes
  (useful for "motorcycle is being moved" automations)

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
The tracker itself reports on its own schedule, so polling faster than it reports
only adds requests.

## Automation example

```yaml
alias: Motorcycle moved
triggers:
  - trigger: event
    event_type: notione_accelerometer_changed
    event_data:
      to: MOVING   # check the actual values in Developer tools → Events
actions:
  - action: notify.mobile_app_phone
    data:
      message: "{{ trigger.event.data.name }} is moving!"
```

Event data: `device_id`, `name`, `from`, `to`.

## Requirements

Home Assistant 2025.2 or newer.

## Troubleshooting

```yaml
logger:
  logs:
    custom_components.notione: debug
```

---

## Polski

Nieoficjalna integracja Home Assistant dla lokalizatorów **notiOne GPS / GPS Plus**.
Loguje się do tego samego API, z którego korzysta [panel.notione.com](https://panel.notione.com),
i dodaje każdy lokalizator z konta jako urządzenie z trackerem i sensorami.

> ⚠️ Projekt nie jest powiązany z notiOne / Notinote. Korzysta z nieudokumentowanego API,
> które może się zmienić bez uprzedzenia.

### Co daje

- Konfiguracja z UI (e-mail + hasło), ponowne logowanie, ustawiany interwał odpytywania
- `device_tracker` z pozycją GPS, dokładnością, baterią, prędkością i nazwą miejsca
- Sensory: bateria, temperatura, wilgotność, prędkość, akcelerometr, miejsce, ostatni raport,
  orientacja, GPS SNR (domyślnie wyłączony), ostatnie wciśnięcie przycisku
- Sensory binarne: ruch, online, ładowanie
- Zdarzenie `notione_accelerometer_changed` przy każdej zmianie stanu akcelerometru

### Instalacja przez HACS

1. HACS → ⋮ → **Custom repositories**
2. Adres: `https://github.com/shaggee/ha-notione-gps`, typ: **Integration**
3. Wyszukaj **notiOne GPS**, zainstaluj i zrestartuj Home Assistanta
4. Ustawienia → Urządzenia i usługi → **Dodaj integrację** → *notiOne GPS*

### Instalacja ręczna

Skopiuj `custom_components/notione` do `<config>/custom_components/` i zrestartuj HA.

## License

MIT
