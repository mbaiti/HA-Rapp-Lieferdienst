# Home Assistant - Rapp Lieferdienst Integration

[![Marketplace (ehem. HACS)](https://img.shields.io/badge/Marketplace_%28ehem._HACS%29-Custom-orange.svg)](https://github.com/mbaiti/HA-Rapp-Lieferdienst)

Diese benutzerdefinierte Integration für [Home Assistant](https://www.home-assistant.io/) integriert die Liefertermine des Getränkelieferdiensts [Brauerei Rapp](https://brauerei-rapp.de/) in Ihre Smart-Home-Umgebung.

Sie stellt zwei Hauptfunktionen zur Verfügung:
1.  Eine **Kalender-Entität**, die alle zukünftigen Liefertermine anzeigt.
2.  Eine **Sensor-Entität**, die das Datum des nächsten anstehenden Liefertermins darstellt.

## Features

*   **Einfache Einrichtung:** Konfiguration direkt über die Home Assistant Benutzeroberfläche.
*   **Kalender-Integration:** Alle Liefertermine werden in einem eigenen Kalender in Home Assistant angezeigt.
*   **Sensor für den nächsten Termin:** Perfekt für Dashboards und Automatisierungen, um immer den nächsten Liefertermin im Blick zu haben.
*   **Automatische Aktualisierung:** Die Termine werden alle 6 Stunden abgerufen; der Sensor wird zusätzlich jede Nacht um Mitternacht neu berechnet.
*   **Kundennummer ändern:** Über das Zahnrad der Integration oder über **"Neu konfigurieren"** – Entitäten und Verlauf bleiben erhalten.

## Installation

### Voraussetzungen

*   Home Assistant **2025.1** oder neuer.
*   Für die empfohlene Installation: der **Marketplace (ehem. HACS)**, seit Home Assistant 2026.11 fester Bestandteil von Home Assistant.

### Methode 1: Installation über den Marketplace (ehem. HACS) (Empfohlen)

1.  Öffnen Sie **Einstellungen** > **Marketplace** (ehem. HACS).
2.  Suchen Sie nach **"Rapp Lieferdienst"**. Falls die Integration nicht gefunden wird, fügen Sie die URL dieses GitHub-Repositories als benutzerdefiniertes Repository (Kategorie `Integration`) hinzu.
3.  Klicken Sie auf **"Installieren"** und starten Sie Home Assistant anschließend neu.

> Ältere Home-Assistant-Versionen mit separat installiertem HACS funktionieren genauso über die HACS-Oberfläche.

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
            ├── sensor.py
            ├── strings.json
            └── translations/
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

Der Sensor `sensor.nachster_rapp_liefertermin` zeigt den nächsten Liefertermin relativ zum heutigen Tag an: `Heute`, `Morgen`, `in X Tagen` bzw. `Keine Termine`.

Attribute:
*   `date` – Datum des nächsten Liefertermins (ISO-Format, z. B. `2026-11-30`)
*   `days_until` – Anzahl der Tage bis zur Lieferung (0 = heute)

Die Kalender-Entität ist an einem Liefertag `on`, sonst `off`.

**Beispiel für eine Entities-Karte:**
```yaml
type: entities
entities:
  - entity: sensor.nachster_rapp_liefertermin
    name: Nächste Rapp-Lieferung
```

**Beispiel für eine Automation am Vorabend:**
```yaml
triggers:
  - trigger: time
    at: "18:00:00"
conditions:
  - condition: state
    entity_id: sensor.nachster_rapp_liefertermin
    state: Morgen
actions:
  - action: notify.notify
    data:
      message: "Morgen kommt Rapp – Leergut bereitstellen!"
```
## Haftungsausschluss
Dies ist eine inoffizielle Integration und steht in keiner Verbindung mit der Brauerei Rapp GmbH & Co. KG. Sie wird von der Community entwickelt und gewartet.
