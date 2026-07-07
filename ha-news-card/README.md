# 📰 Morgenbriefing Card – News-Karte für Home Assistant

Jeden Morgen die wichtigsten nationalen und regionalen News auf dem Dashboard –
mit **mitgelieferten Standard-Feeds** (Presets inkl. Google News),
**Google-News-Suchfeeds** für beliebige Orte/Begriffe, **eigenen RSS-Links** und
Unterstützung für **vorhandene Feed-Sensoren**, falls RSS in Home Assistant
schon genutzt wird.

## Dateien

| Datei | Zweck |
|---|---|
| `www/morgenbriefing-card.js` | Die Custom Card (Lovelace-Ressource) |
| `packages/morgenbriefing.yaml` | Standard-Feed-Sensoren als HA-Package (empfohlen) |
| `dashboard-card.yaml` | Beispiel-Konfiguration der Karte |
| `dashboard-card-markdown.yaml` | Fallback ohne Custom Card (reine Markdown-Karte) |
| `automation.yaml` | Morgen-Automation: 06:00 Uhr Update + Push aufs Handy |

## Vier Wege, eine Quelle einzubinden

Jeder Abschnitt (`sections`) der Karte bekommt seine News auf einem von vier Wegen:

```yaml
type: custom:morgenbriefing-card
title: Morgenbriefing
max_items: 5
sections:
  - preset: tagesschau            # 1. Standard-Feed, mitgeliefert
  - preset: wdr                   #    …auch regional
    title: Meine Region
  - title: Lokales                # 2. Google-News-Suche zu Ort/Begriff
    google: "Münster"             #    (ideal für Lokalnachrichten)
  - title: Tech                   # 3. Eigener RSS/Atom-Link
    url: https://www.heise.de/rss/heise-atom.xml
  - title: Wirtschaft             # 4. Vorhandener Sensor (z. B. Feedparser),
    entity: sensor.mein_feed      #    wenn RSS in HA schon läuft
```

**Presets** (Stand siehe `www/morgenbriefing-card.js`):

| Preset | Feed |
|---|---|
| `tagesschau` | tagesschau.de – Topmeldungen |
| `tagesschau_inland` | tagesschau.de – Inland |
| `sportschau` | sportschau.de |
| `heise` | heise online |
| `spiegel` | SPIEGEL Schlagzeilen |
| `ntv` | n-tv |
| `google_news` | Google News – Topmeldungen Deutschland |
| `google_news_welt` | Google News – Welt |
| `google_news_wirtschaft` | Google News – Wirtschaft |
| `google_news_tech` | Google News – Technik |
| `wdr` | NRW (WDR) |
| `ndr_niedersachsen` / `ndr_sh` / `ndr_hamburg` / `ndr_mv` | NDR-Regionalfeeds |
| `hessenschau` | Hessen |
| `mdr` | Sachsen / Sachsen-Anhalt / Thüringen |
| `rbb24` | Berlin / Brandenburg |

**Google News:** Neben den Presets baut `google: "Begriff"` automatisch einen
Google-News-Suchfeed (deutschsprachig, Region DE) – praktisch für
Lokalnachrichten zum eigenen Ort oder Themen wie einen Vereinsnamen. Für den
zuverlässigen serverseitigen Abruf gibt es im Package fertige (auskommentierte)
Google-News-Sensor-Blöcke. Hinweis: Google-News-Links führen über
news.google.com zum Artikel, Titel enthalten den Quellennamen.

**Wie die Karte eine Preset-Quelle auflöst:** Existiert der Sensor
`sensor.mb_<preset>` (aus dem Package), wird er benutzt – zuverlässigster Weg.
Sonst versucht die Karte, den Feed direkt im Browser abzurufen. Blockiert die
News-Seite das per CORS, zeigt die Karte einen Hinweis, für diesen Feed einen
Sensor anzulegen. Gleiches gilt für eigene `url:`-Einträge.

## Installation

### 1. Karte als Ressource einbinden

`www/morgenbriefing-card.js` nach `/config/www/` kopieren, dann:
Einstellungen → Dashboards → ⋮ → **Ressourcen** → Hinzufügen →
URL `/local/morgenbriefing-card.js`, Typ **JavaScript-Modul**. Browser-Cache
leeren (Strg+F5).

### 2. Standard-Sensoren anlegen (empfohlen)

Damit alle Feeds zuverlässig serverseitig geladen werden:

1. HACS-Integration **feedparser** installieren (`custom-components/feedparser`), HA neu starten.
2. `packages/morgenbriefing.yaml` nach `/config/packages/` kopieren und in der
   `configuration.yaml` Packages aktivieren:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
3. Im Package den passenden Regional-Block einkommentieren und bei Bedarf
   eigene Feeds im Abschnitt „Eigene Feeds" ergänzen. HA neu starten.

Wer keine Packages nutzt, kann den `sensor:`-Block auch direkt in die
`configuration.yaml` übernehmen.

**Schon Feedparser/RSS-Sensoren im Einsatz?** Dann entfällt dieser Schritt –
vorhandene Sensoren einfach per `entity:` in der Karte einbinden (die Karte
erwartet ein `entries`-Attribut mit `title`, `link`, `published`).

### 3. Karte aufs Dashboard

Dashboard → Bearbeiten → Karte hinzufügen → **Manuell** → Inhalt von
`dashboard-card.yaml` einfügen und anpassen.

Optionen: `title` (Kartentitel), `max_items` (global oder je Abschnitt),
`show_time: false` (Zeitstempel ausblenden).

### 4. Morgen-Automation (optional)

`automation.yaml` legt eine Automation an, die um 06:00 Uhr die MB-Sensoren
aktualisiert und die Top-3-Schlagzeilen als Push aufs Handy schickt.
`notify.mobile_app_…` und die `entity_id`-Liste anpassen.

## Hinweise

- **Feed-URLs prüfen:** Jede URL einmal im Browser öffnen – es muss XML/RSS
  erscheinen. Sender ändern URLs gelegentlich; im Zweifel beim Sender nach
  „RSS" suchen.
- **Fair bleiben:** `scan_interval` von 30 Minuten reicht – die
  Morgen-Automation lädt um 6 Uhr ohnehin frisch.
- **Fallback ohne Custom Card:** `dashboard-card-markdown.yaml` rendert die
  Sensoren mit einer reinen Markdown-Karte.
- **Optional – KI-Briefing:** Mit einer KI-Integration (z. B. Anthropic oder
  OpenAI) kann die Automation die Schlagzeilen per `conversation.process` zu
  einem 3-Sätze-Briefing zusammenfassen und in einem Template-Sensor ablegen.
