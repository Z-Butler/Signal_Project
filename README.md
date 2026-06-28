# SIGINT Signal Collection & Analysis Tool

A CLI tool for filtering and visualizing RF signal collection data. Takes SIGINT data from a CSV, lets you filter it down by various parameters, and outputs an interactive HTML map with collection sites and lines of bearing.

---

## Project Structure

```
sigint_project/
├── collection_sites.py   # signal power calculations, map generation, filter utilities
├── data_filter.py        # entry point, interactive filter loop
└── sigint_sample.csv     # sample dataset
```

---

## Requirements

```bash
pip install numpy pandas folium geopy
```

| Library | Used for |
|---|---|
| `numpy` | free-space path loss calculations |
| `pandas` | data loading and filtering |
| `folium` | HTML map generation |
| `geopy` | bearing and distance calculations |

---

## Usage

```bash
python data_filter.py
```

### Filter Menu

| Option | Description |
|---|---|
| `1` — Date | `YYYY-MM-DD` |
| `2` — Time | `HH:MM` or `HHMM` |
| `3` — Emitter | `EMITTER-001` or just `001` |
| `4` — Frequency | MHz |
| `5` — Bandwidth | KHz |
| `6` — Modulation | `CW`, `AM`, `FM`, `FSK`, `PSK`, `QAM` |
| `7` — Site | exact site name (e.g. `Sigonella, Italy`) |
| `9` — Preview | print filtered results to terminal |
| `10` — Build Map | export to HTML map |
| `11` — Remove Filter | remove one active filter |
| `12` — Clear Filters | reset everything |
| `13` — Quit | exit |

Filters stack — you can apply several at once and remove them individually. If a filter returns zero results it won't be applied.

### Example

```
> 3  →  EMITTER-001
> 6  →  CW
> 9  →  preview results
> 10 →  my_map
```

Opens as `my_map.html` in any browser.

---

## Map Output

Generated maps include collection site markers, lines of bearing from each site, a geocoder search bar, measuring tool, collapsible minimap, and live coordinate readout on mouse position. Bearing lines can be toggled on/off. Tiles from Esri National Geographic.

---

## Sample Data

`sigint_sample.csv` covers 24 hours of collections (~30 min intervals) across 4 sites and 3 emitters.

| Column | Description |
|---|---|
| `timestamp` | date and time of collection |
| `source_id` | emitter ID |
| `frequency_mhz` | frequency in MHz |
| `signal_strength_dbm` | received signal strength |
| `bandwidth_khz` | bandwidth in KHz |
| `modulation` | modulation type |
| `bearing_deg` | direction of arrival |
| `duration_sec` | signal duration |
| `site_name` | collection site |
| `collection_lat` / `collection_lon` | site coordinates |
| `snr_db` | signal-to-noise ratio |
