# Changelog

Research discoveries from file analysis. Each entry is keyed to the record that surfaced it.

Entries here represent findings that update the shared reference — newly identified fields, confirmed encodings, corrected hypotheses. The records themselves are the primary data; this log is the research trail.

---

## 2026-05-19

### Source: `garmin-fenix7prosolar-garminconnect-singleexport-running-001`

**New field: `record` def_num 90 — Performance Condition**
- Named `performance_condition` by FitFileViewer
- Garmin real-time metric comparing expected vs actual performance during activity
- Observed value: constant integer (illustrative only); typically ranges ±20 from baseline
- Status: `garmin_proprietary`, confidence: `confirmed`
- Action: add to record message field reference

**Device product codes identified**
- `garmin_product 4375` = Fenix 7 Pro Solar (confirmed by FitFileViewer and device owner)
- `garmin_product 3865` = MediaTek AG3335M GPS chip (internal to Fenix 7 Pro Solar; confirmed by FitFileViewer showing product name `ag3335m`)
- `garmin_product 3299` = HRM-Dual chest strap (confirmed by device owner: https://www.garmin.com/en-GB/p/649059/)

**Garmin Connect single-export filename pattern confirmed**
- ZIP filename: `{activity_id}.zip`
- FIT filename inside ZIP: `{activity_id}_ACTIVITY.fit`

**Internal Fenix 7 Pro Solar device modules identified in `device_info`**
- device_index 1: barometer (product: fenix 7 pro solar)
- device_index 2: GPS chip (product: ag3335m)
- device_index 4: accelerometer (no manufacturer/product)
- device_index 6: wrist HR optical module (no manufacturer/product)
- device_index 7: sensor hub (product: fenix 7 pro solar)
- device_index 5: device_type_raw `8` — **unresolved**. No manufacturer/product populated; not decoded by FitFileViewer or fitparse.

**HR source behaviour confirmed (Fenix 7 Pro Solar + HRM-Dual)**
- `record` def_num 3: active HR source (chest strap value when external HRM paired)
- `record` def_num 136: wrist optical HR (secondary, always present when external HRM paired)
- `record` def_num 144: external HR duplicate (exact copy of def_num 3 when external HRM paired)
