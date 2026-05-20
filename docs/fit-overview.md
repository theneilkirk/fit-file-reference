# FIT File Overview

A primer for developers new to the FIT format.

## What is FIT?

FIT (Flexible and Interoperable Data Transfer) is a binary file format developed by Garmin/ANT+ for storing fitness device data. It is the native format for Garmin devices and is also used by many other manufacturers.

The spec is maintained by ANT+ and documented at https://developer.garmin.com/fit/protocol/.

## Structure

A FIT file is a sequence of **messages**. Each message has a **type** (identified by a `mesg_num`) and contains **fields** (identified by `def_num` within that message type). Fields are defined per-message-type — `def_num 3` in a `record` message is heart rate; `def_num 3` in a `session` message is start latitude. The same number in different message types means different things.

### Key message types for activity files

| Message type | Purpose |
|-------------|---------|
| `file_id` | File metadata — manufacturer, product, creation time |
| `device_info` | Device details — each connected device or sensor gets one or more entries |
| `record` | Per-second time-series data — HR, speed, distance, GPS, cadence, power, etc. |
| `lap` | Aggregate data per lap |
| `session` | Aggregate data for the full activity |
| `event` | Timer start/stop/pause markers |
| `activity` | Top-level wrapper |

### Field presence

Not every field is populated in every file. Presence depends on:

- What sensors are connected (e.g. power only appears if a power meter is paired)
- What the device supports (e.g. barometric altitude requires a barometric sensor)
- Activity type (swimming fields are empty in running files)
- Whether a structured workout was active (workout step fields only appear with a workout loaded)
- Source platform (some platforms strip fields on export)

This reference distinguishes between fields that are `populated`, `empty` (defined but no data), and `mixed` (populated in some messages, empty in others).

## Proprietary extensions

The base FIT spec defines a standard set of fields. Garmin extends this significantly with proprietary fields — many undocumented. These appear in files as unknown field numbers (e.g. `def_num 108` in a `record` message, which Garmin uses for respiration rate).

Third-party tools like [FitFileViewer](https://www.fitfileviewer.com/) have reverse-engineered many of these. This reference tracks the confidence level of each field's identification.

## Parsing

The most widely used Python library is [fitparse](https://github.com/dtcooper/python-fitparse). Its field name dictionary lags behind the Garmin SDK, so newer proprietary fields often appear as `unknown_N`. Where that happens, the field's `def_num` is the stable identifier to use.

## Further reading

- [ANT+ FIT Protocol specification](https://developer.garmin.com/fit/protocol/)
- [Garmin FIT SDK](https://developer.garmin.com/fit/download/)
- [FitFileViewer](https://www.fitfileviewer.com/) — browser-based tool with extensive proprietary field decoding
