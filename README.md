# Fahrschul-Webseite

Dieses Projekt ist ein einfaches Beispiel für eine Webseite einer Fahrschule.
Fahrschüler können sich nur mit einem Registrierungscode anmelden, Bilder von
bestandenen Prüfungen hochladen und Bewertungen abgeben. Der Fahrlehrer kann
Bilder freischalten und die Bewertungen einsehen.

## Funktionen

* Registrierung nur mit Code
* Zwei Rollen: Fahrschüler und Fahrlehrer
* Bild-Upload der Schüler mit Freischaltung durch den Lehrer
* Bewertungssystem (1–10) für Theorie und Fahrstunden
* Kontolöschung erfolgt 24 Stunden nach Anforderung

## Installation

1. Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

2. Anwendung starten:

```bash
python app.py
```

Die Webseite läuft anschließend unter `http://localhost:5000`.

Der Registrierungscode ist in `app.py` in der Konstante `REGISTRATION_CODE`
definiert und kann dort angepasst werden.
