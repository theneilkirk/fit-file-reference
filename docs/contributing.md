# Contributing

## What we're building

A reference documenting which FIT file fields exist, what they contain, and how that varies by manufacturer, device, source platform, and activity type. The goal is to make FIT file parsing less of a guessing game for developers.

## Adding a record

A record documents one analysed FIT file (or one representative file from a bulk export). The process:

1. **Obtain a FIT file** — single export, bulk export, or direct from device.
2. **Record provenance** — source platform, export method, device make and model, activity type. You'll need to supply this; it cannot be extracted from the file alone.
3. **Analyse the file** — extract all message types and fields, noting which are populated, empty, or mixed. The analysis script in `tools/` (coming soon) automates this.
4. **Research unknowns** — for fields fitparse cannot name, check [FitFileViewer](https://www.fitfileviewer.com/) and the [Garmin FIT SDK](https://developer.garmin.com/fit/protocol/). Do not guess. Record what you find and what you don't.
5. **Scrub PII** — before writing the record, remove: GPS coordinates, serial numbers, ANT IDs, platform activity IDs, and precise timestamps. Field presence is what matters; actual values are only included to illustrate encoding.
6. **Write the record** — follow the JSON schema in `schema/record.schema.json`. Name it `{record_id}.json` and place it in `records/{manufacturer}/`.
7. **Update CHANGELOG.md** — if your file surfaced new findings (new fields, confirmed encodings, corrected hypotheses), add a dated entry referencing your record ID.
8. **Submit a PR** — include a brief description of what device/source this covers and what, if anything, is new.

## Record ID convention

Format: `{manufacturer}-{product_slug}-{source_platform}-{source_type}-{sport}-{NNN}`

All values from `schema/vocabulary.md`. The sequence suffix (`001`, `002`, ...) is per combination — so the second running file from a Fenix 7 Pro Solar via Garmin Connect single export would be `garmin-fenix7prosolar-garminconnect-singleexport-running-002`.

## Privacy rules

These are non-negotiable:

- No GPS coordinates (lat, long, bounding boxes)
- No device serial numbers
- No ANT IDs
- No platform activity IDs or URLs linking to specific accounts
- No precise timestamps (date alone is acceptable where it contextualises firmware/software versions)
- Sample values are only included to illustrate field encoding, and must be anonymised or synthetic

## What makes a good contribution

- A device or source platform not yet represented in `records/`
- A different activity type for an existing device (e.g. cycling or strength from a Garmin watch already documented for running)
- A field confirmed or corrected via the Garmin SDK or FitFileViewer that updates a prior `undocumented` or `ffv_undocumented` entry
- A bulk export that reveals different field presence compared to a single export from the same platform

## Questions

Open an issue. If you're unsure whether a field is PII, err on the side of removing it.
