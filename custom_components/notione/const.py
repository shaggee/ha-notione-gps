"""Constants for notiOne GPS."""

DOMAIN = "notione"

AUTH_URL = "https://auth.notinote.me/public/user/authorize/login"
API_URL = "https://api.notinote.me/secured/internal"
# Static client credential of the panel.notione.com web app (same for every user)
CLIENT_BASIC = (
    "dGVzdC1vYXV0aC1jbGllbnQtaWQ6JDJ5JDEyJHZYT1V0RWVuVkZDTzFaZ3kyWWllUHVG"
    "M1dGL3NEZ05PM1luaFJqbDQ5TklEbEViR2VTZU91"
)

CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 20  # seconds
MIN_SCAN_INTERVAL = 10

EVENT_ACCELEROMETER = "notione_accelerometer_changed"
STATIONARY = "STATIONARY"
