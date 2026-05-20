# Vocabulary

Controlled values used in record IDs and record fields. New values must be added here before use.

## Record ID format

`{manufacturer}-{product_slug}-{source_platform}-{source_type}-{sport}-{NNN}`

Example: `garmin-fenix7prosolar-garminconnect-singleexport-running-001`

All components lowercase, hyphen-separated, no spaces or special characters.

---

## `manufacturer`

| Value | Description |
|-------|-------------|
| `garmin` | Garmin Ltd |
| `coros` | COROS Wearables |
| `polar` | Polar Electro |
| `suunto` | Suunto |
| `wahoo` | Wahoo Fitness |
| `apple` | Apple (Apple Watch) |

---

## `product_slug`

Short, stable identifier for the recording device. Use the manufacturer's product name, lowercased, spaces and punctuation removed.

| Value | Device |
|-------|--------|
| `fenix7prosolar` | Garmin Fenix 7 Pro Solar |
| `forerunner965` | Garmin Forerunner 965 |
| `forerunner255` | Garmin Forerunner 255 |
| `pace3` | COROS Pace 3 |

---

## `source_platform`

The platform the file was exported from.

| Value | Description |
|-------|-------------|
| `garminconnect` | Garmin Connect web/app |
| `strava` | Strava web/app |
| `device` | Directly from the device (USB/MTP) |
| `wahooapp` | Wahoo companion app |

---

## `source_type`

How the file was obtained from that platform.

| Value | Description |
|-------|-------------|
| `singleexport` | Single activity export (e.g. Garmin Connect "Export File" on an activity page) |
| `bulkexport` | Full data export archive (e.g. Garmin data export, Strava bulk export) |
| `directdevice` | Copied directly from device storage |

---

## `sport`

The activity sport type. Derived from the FIT `sport` field.

| Value | FIT sport value |
|-------|----------------|
| `running` | running |
| `cycling` | cycling |
| `swimming` | swimming |
| `walking` | walking |
| `hiking` | hiking |
| `strength` | training / strength_training |
| `indoorcycling` | cycling / indoor_cycling |
| `treadmill` | running / treadmill |
| `generic` | generic or unclassified |

---

## Field status values

Used in `fields[].status`:

| Value | Meaning |
|-------|---------|
| `populated` | Field present and contains data in all observed messages of this type |
| `empty` | Field defined in the message schema but contains no data |
| `mixed` | Field populated in some messages, empty in others |

---

## Registry status values

Used in `fields[].registry_status`:

| Value | Meaning |
|-------|---------|
| `sdk` | Defined in the official ANT+/Garmin FIT SDK specification |
| `garmin_proprietary` | Garmin extension, documented via Garmin developer resources or FitFileViewer with high confidence |
| `ffv_undocumented` | Named by FitFileViewer but marked undocumented by FFV; name is probable, not confirmed |
| `empirical` | Decoded from file analysis; not named by any external tool |
| `undocumented` | Present in files; no name or meaning found anywhere |
| `new` | Observed in this file; not yet classified |
