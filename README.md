# Home Assistant - Rapp Lieferdienst Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

Diese benutzerdefinierte Integration für [Home Assistant](https://www.home-assistant.io/) integriert die Liefertermine des Getränkelieferdiensts [Brauerei Rapp](https://brauerei-rapp.de/) in Ihre Smart-Home-Umgebung.

Sie stellt zwei Hauptfunktionen zur Verfügung:
1.  Eine **Kalender-Entität**, die alle zukünftigen Liefertermine anzeigt.
2.  Eine **Sensor-Entität**, die das Datum des nächsten anstehenden Liefertermins darstellt.

## Features

*   **Einfache Einrichtung:** Konfiguration direkt über die Home Assistant Benutzeroberfläche.
*   **Kalender-Integration:** Alle Liefertermine werden in einem eigenen Kalender in Home Assistant angezeigt.
*   **Sensor für den nächsten Termin:** Perfekt für Dashboards und Automatisierungen, um immer den nächsten Liefertermin im Blick zu haben.
*   **Automatische Aktualisierung:** Die Termine werden alle 24 Stunden automatisch im Hintergrund abgerufen und aktualisiert.
*   **Unterstützt Konfigurations-Änderungen:** Wenn Sie Ihre Kundennummer ändern, werden die Kalenderdaten automatisch neu geladen.

## Installation

### Voraussetzungen

*   Sie benötigen eine funktionierende Home Assistant Instanz (Version 2023.x oder neuer).
*   Der [Home Assistant Community Store (HACS)](https://hacs.xyz/) muss installiert sein.

### Methode 1: Installation über HACS (Empfohlen)

1.  Öffnen Sie Ihre **HACS**-Oberfläche in Home Assistant.
2.  Gehen Sie zu **Integrationen**.
3.  Klicken Sie auf die drei Punkte in der oberen rechten Ecke und wählen Sie **"Benutzerdefinierte Repositories"**.
4.  Fügen Sie die URL dieses GitHub-Repositories in das Feld `Repository` ein und wählen Sie als Kategorie `Integration`.
5.  Klicken Sie auf **"Hinzufügen"**.
6.  Suchen Sie nach der **"Rapp Lieferdienst"** Integration in Ihrer HACS-Liste und klicken Sie auf **"Installieren"**.
7.  Starten Sie Home Assistant neu, wie von HACS empfohlen.

### Methode 2: Manuelle Installation

1.  Laden Sie die neueste Version von diesem Repository herunter.
2.  Kopieren Sie den Ordner `rapp_lieferdienst` (innerhalb von `custom_components`) in den Ordner `custom_components` Ihrer Home Assistant-Installation. Wenn der Ordner `custom_components` nicht existiert, erstellen Sie ihn.
    ```
    <config>/
    └── custom_components/
        └── rapp_lieferdienst/
            ├── __init__.py
            ├── api.py
            ├── calendar.py
            ├── config_flow.py
            ├── const.py
            ├── coordinator.py
            ├── manifest.json
            └── sensor.py
    ```
3.  Starten Sie Home Assistant neu.

## Konfiguration

Nach der Installation kann die Integration einfach über die Benutzeroberfläche eingerichtet werden:

1.  Gehen Sie in Home Assistant zu **Einstellungen** > **Geräte & Dienste**.
2.  Klicken Sie unten rechts auf **"+ Integration hinzufügen"**.
3.  Suchen Sie nach **"Rapp Lieferdienst"** und wählen Sie die Integration aus.
4.  Geben Sie im Konfigurationsdialog Ihre **Rapp-Kundennummer** ein.
5.  Klicken Sie auf **"Absenden"**.

Die Integration wird nun eingerichtet und die beiden Entitäten (`calendar.rapp_lieferkalender` und `sensor.nachster_rapp_liefertermin`) werden erstellt.

## Verwendung

### Kalender

Die Kalender-Entität kann in verschiedenen Kalender-Karten im Dashboard oder in Automatisierungen verwendet werden.

### Sensor

Der Sensor `sensor.nachster_rapp_liefertermin` hat als Zustand einen Zeitstempel des nächsten Lieferdatums. Sie können ihn einfach in einer Entities-Karte oder einer benutzerdefinierten Karte anzeigen.

**Beispiel für eine Entities-Karte:**
```yaml
type: entities
entities:
  - entity: sensor.nachster_rapp_liefertermin
    name: Nächste Rapp-Lieferung
    format: date

Haftungsausschluss: Dies ist eine inoffizielle Integration und steht in keiner Verbindung mit der Brauerei Rapp GmbH & Co. KG. Sie wird von der Community entwickelt und gewartet.

