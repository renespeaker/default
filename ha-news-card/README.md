# 📰 Morgenbriefing – News-Karte für Home Assistant

Ziel: Jeden Morgen auf dem Dashboard die wichtigsten nationalen News (tagesschau)
und die regionalen Nachrichten für die eigene Region sehen – automatisch
aktualisiert, optional mit Push-Benachrichtigung aufs Handy.

## Architektur

```
RSS-Feeds (tagesschau + Regionalsender)
        │
        ▼
Feedparser-Sensoren (HACS-Integration "feedparser")
        │
        ▼
Markdown-Karte auf dem Dashboard  ◄── Automation: Update um 06:00 + Push
```

## Umsetzung in 5 Schritten

### 1. Feedparser installieren

In HACS nach **feedparser** suchen (Repository: `custom-components/feedparser`)
und installieren, danach Home Assistant neu starten. Die Integration erzeugt
Sensoren, deren `entries`-Attribut die Schlagzeilen mit Titel, Link und
Zeitstempel enthält – ideal für Templates.

### 2. Sensoren anlegen

Inhalt von [`configuration.yaml`](configuration.yaml) in die eigene
`configuration.yaml` übernehmen (oder als Package einbinden). Zwei Sensoren:

- `sensor.tagesschau` – nationale News
- `sensor.news_regional` – Feed des Regionalsenders (URL je nach Bundesland,
  siehe Tabelle unten)

**Wichtig:** Feed-URL vor dem Eintragen einmal im Browser öffnen – es muss
XML/RSS erscheinen. Die Sender ändern ihre URLs gelegentlich.

### 3. Karte aufs Dashboard

Dashboard → Bearbeiten → Karte hinzufügen → **Manuell** → Inhalt von
[`dashboard-card.yaml`](dashboard-card.yaml) einfügen. Die Markdown-Karte
rendert die Top-5-Schlagzeilen beider Feeds mit klickbaren Links.

### 4. Morgen-Automation

[`automation.yaml`](automation.yaml) legt eine Automation an, die um 06:00 Uhr
beide Sensoren aktualisiert und die Top-3-Schlagzeilen als Push-Nachricht aufs
Handy schickt (`notify.mobile_app_…` an das eigene Gerät anpassen).

### 5. Optional: KI-Zusammenfassung

Mit einer KI-Integration (z. B. Anthropic/Claude oder OpenAI in Home Assistant)
kann die Automation die Schlagzeilen zusätzlich per `conversation.process` zu
einem 3-Sätze-Briefing zusammenfassen und in einem `input_text` oder
Template-Sensor ablegen – die Karte zeigt es dann über den Schlagzeilen an.

## Regionale RSS-Feeds (Auswahl)

| Region | Sender | Feed-URL (vor Nutzung prüfen!) |
|---|---|---|
| Deutschland | tagesschau | `https://www.tagesschau.de/index~rss2.xml` |
| NRW | WDR | `https://www1.wdr.de/uebersicht-100.feed` |
| Niedersachsen | NDR | `https://www.ndr.de/nachrichten/niedersachsen/index-rss.xml` |
| Schleswig-Holstein | NDR | `https://www.ndr.de/nachrichten/schleswig-holstein/index-rss.xml` |
| Hamburg | NDR | `https://www.ndr.de/nachrichten/hamburg/index-rss.xml` |
| Mecklenburg-Vorp. | NDR | `https://www.ndr.de/nachrichten/mecklenburg-vorpommern/index-rss.xml` |
| Hessen | hessenschau | `https://www.hessenschau.de/index.rss` |
| Sachsen/Sa.-Anh./Thür. | MDR | `https://www.mdr.de/nachrichten/index-rss.xml` |
| Berlin/Brandenburg | rbb24 | `https://www.rbb24.de/aktuell/index.xml/feed=rss.xml` |
| Bayern | BR24 | RSS-Übersicht auf br.de/nachrichten suchen |
| BW / RLP | SWR | RSS-Übersicht auf swr.de/swraktuell suchen |

Falls eine URL nicht (mehr) funktioniert: Beim jeweiligen Sender nach
„RSS" suchen – alle ARD-Anstalten bieten aktuelle Feed-Übersichten an.

## Hinweise

- `scan_interval: 30 min` reicht völlig und ist fair gegenüber den Sendern.
- Zusätzliche Feeds (Lokalzeitung, Blaulicht, Wetterwarnungen) einfach als
  weitere Feedparser-Sensoren anlegen und in der Karte ergänzen.
- Wer eine aufwendigere Optik möchte: HACS-Karten wie `list-card` oder
  `flex-table-card` können die `entries` ebenfalls rendern.
