 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 86cf909251f6403c81e1298e6a952b0a8d5c6317..09fd43f394edb38d1743abb33a57d2f9bde15a9d 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,33 @@
-# ginoco
+# Fahrschul-Webseite
+
+Dieses Projekt ist ein einfaches Beispiel für eine Webseite einer Fahrschule.
+Fahrschüler können sich nur mit einem Registrierungscode anmelden, Bilder von
+bestandenen Prüfungen hochladen und Bewertungen abgeben. Der Fahrlehrer kann
+Bilder freischalten und die Bewertungen einsehen.
+
+## Funktionen
+
+* Registrierung nur mit Code
+* Zwei Rollen: Fahrschüler und Fahrlehrer
+* Bild-Upload der Schüler mit Freischaltung durch den Lehrer
+* Bewertungssystem (1–10) für Theorie und Fahrstunden
+* Kontolöschung erfolgt 24 Stunden nach Anforderung
+
+## Installation
+
+1. Abhängigkeiten installieren:
+
+```bash
+pip install -r requirements.txt
+```
+
+2. Anwendung starten:
+
+```bash
+python app.py
+```
+
+Die Webseite läuft anschließend unter `http://localhost:5000`.
+
+Der Registrierungscode ist in `app.py` in der Konstante `REGISTRATION_CODE`
+definiert und kann dort angepasst werden.
 
EOF
)
