# Changelog

Research discoveries from file analysis. Each entry is keyed to the record that surfaced it.

Entries here represent findings that update the shared reference — newly identified fields, confirmed encodings, corrected hypotheses. The records themselves are the primary data; this log is the research trail.

---

## 2026-07-12

### Source: `garmin-fenix7prosolar-strava-singleexport-running-001`

**First strava-sourced record — Strava's manual export is a stripped re-encode, not a passthrough**
- Same physical device (Fenix 7 Pro Solar, product 4375) as `garmin-fenix7prosolar-garminconnect-singleexport-running-001`, but exported via strava.com instead of Garmin Connect
- Of the ~20 Garmin proprietary/undocumented message types seen in the garminconnect export, only `unknown_312` (split) survives; every other one is absent
- Every observed field in record/session/lap messages is a plain SDK field — zero `garmin_proprietary` or `ffv_undocumented` fields anywhere in this file
- `heart_rate` (record def_num 3) is entirely absent, despite an HRM-Dual chest strap (garmin_product 3299) still appearing in `device_info` as a paired sensor
- `device_info` itself is thinner: no `software_version`, `hardware_version`, or `device_type` populated for any entry
- `strava` added as a confirmed source_platform in practice (already present in vocabulary.md, previously unused)
- Root cause unconfirmed — could be Strava re-encoding on export, or the original upload to Strava already lacking these fields. Flagged as `probable` confidence pending a same-activity garminconnect comparison

---

## 2026-05-21

### Source: `garmin-forerunner35-garminconnect-singleexport-running-001`

**First FR35 record — new device, significantly reduced field set vs Fenix 7**
- `forerunner35` added to vocabulary.md (garmin_product_id 2503 confirmed)
- FR35 record messages contain only SDK fields plus one unknown (def_num 88, constant 300)
- No running dynamics, respiration, body battery, stamina, grade-adjusted speed, wrist HR, or performance condition — all absent on FR35
- Confirms many proprietary extensions in record-001 (Fenix 7 Pro Solar) are device-class-specific, not universal Garmin

**unknown_104 (device_status) hypothesis revised**
- Count of 7 in FR35 file does not match lap count (4); previously assumed per-lap in record-001 where count matched
- Per-lap interpretation is incorrect or incomplete; true trigger unknown

**unknown_140 (activity_metrics) confirmed as non-high-end feature**
- Present in both Fenix 7 Pro Solar and FR35 (entry-level device), confirming this is a general Garmin Connect export feature

**New field: record def_num 88**
- Constant value 300 in all record messages; added to field-registry as speculative
- Needs FitFileViewer lookup on FR35 file

---

## 2026-05-20

### Source: `garmin-fenix7prosolar-garminconnect-singleexport-running-001`

**13 unknown message types confirmed via FitFileViewer**

All identities supplied by eyeballing in FitFileViewer. Types marked * in FFV are undocumented (ffv_undocumented); unknown_13 is documented (garmin_proprietary).

| Message type | FFV name | Registry status | Notes |
|---|---|---|---|
| unknown_13 | training_settings | garmin_proprietary | Documented by FFV. Session-level training config. |
| unknown_22 | device_used | ffv_undocumented | Count of 6 may reflect paired sensors. |
| unknown_79 | user_metrics | ffv_undocumented | Single occurrence; session-level physio snapshot. |
| unknown_104 | device_status | ffv_undocumented | Count 9 = one per lap; prior per-lap hypothesis directionally correct. |
| unknown_113 | best_effort | ffv_undocumented | 3 occurrences; personal best tracking segments. |
| unknown_140 | activity_metrics | ffv_undocumented | Single occurrence; session-level metrics summary. |
| unknown_141 | epo_status | ffv_undocumented | EPO = Extended Prediction Orbit (GPS satellite data). |
| unknown_147 | sensor_settings | ffv_undocumented | Single occurrence; sensor config block. |
| unknown_216 | time_in_zone | ffv_undocumented | 20 occurrences; likely one per HR zone or zone x metric. Distinct from session field def_num 216 (ending_body_battery). |
| unknown_312 | split | ffv_undocumented | 10 occurrences; km/mile auto-splits plus partial final. |
| unknown_313 | split_summary | ffv_undocumented | Aggregated summary across split types; paired with unknown_312. |
| unknown_326 | gps_event | ffv_undocumented | 49 occurrences in ~49 min run; once-per-minute count was correct, identity was not. |
| unknown_394 | cpe_status | ffv_undocumented | CPE likely = Course Point or Computed Position Error. |

**Corrected hypotheses**
- unknown_104: prior hypothesis was per-lap analytics; confirmed as device_status with per-lap cadence intact
- unknown_113: prior hypothesis was HRM connection events; confirmed as best_effort
- unknown_312: prior confidence was `unknown`; confirmed as split
- unknown_326: prior hypothesis was minute-level summary; count was right, identity wrong; confirmed as gps_event

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
