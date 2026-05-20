# FIT File Reference

A community-maintained reference for the data found in `.fit` activity files, documenting how field content varies by manufacturer, device, source platform, and activity type.

## The problem

The FIT protocol defines a base set of message types and fields, but manufacturers extend it heavily with proprietary fields — many undocumented. The same field number means different things in different message types. Files from the same device vary depending on how they were exported. There is no single reference that captures all of this.

This project builds that reference, one analysed file at a time.

## What's here

- **`records/`** — structured JSON records, one per analysed file, organised by manufacturer. Each record documents provenance (where the file came from, what recorded it) and schema (which message types and fields are present, populated, or empty).
- **`schema/`** — the JSON Schema specification for a valid record, plus vocabulary definitions for the controlled values used in record IDs and fields.
- **`docs/`** — a FIT file primer for newcomers, and a contributing guide.
- **`CHANGELOG.md`** — a log of research discoveries (newly identified fields, confirmed encodings, corrected hypotheses), each keyed to the record that surfaced it.

## Scope

Activity FIT files only. Wellness, sleep, and HRV files have different message structures and are out of scope for now.

## Privacy

Records contain no personally identifiable information. GPS coordinates, serial numbers, timestamps, and platform activity IDs are stripped before publication. Field *presence* and *encoding* are documented; actual values are included only where necessary to illustrate encoding, and are anonymised or synthetic where used.

## Contributing

See [docs/contributing.md](docs/contributing.md).

## License

MIT. See [LICENSE](LICENSE).
