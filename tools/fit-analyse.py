#!/usr/bin/env python3
"""
fit-analyse.py — FIT File Reference analysis tool

Analyses a FIT file and produces a structured JSON record ready for the
fit-file-reference repository.

Usage:
    python tools/fit-analyse.py <path-to-fit-file> [options]

Options:
    --manufacturer     Manufacturer slug (e.g. garmin)
    --product          Product slug (e.g. fenix7prosolar)
    --platform         Source platform slug (e.g. garminconnect)
    --source-type      Source type slug (e.g. singleexport)
    --sport            Sport slug (e.g. running)
    --sequence         Record sequence number (default: 001)
    --out              Output file path (default: stdout)

Example:
    python tools/fit-analyse.py activity.fit \\
        --manufacturer garmin \\
        --product fenix7prosolar \\
        --platform garminconnect \\
        --source-type singleexport \\
        --sport running \\
        --sequence 001 \\
        --out records/garmin/garmin-fenix7prosolar-garminconnect-singleexport-running-001.json

Requirements:
    pip install fitparse

Notes:
    - The tool extracts field presence only. No GPS coordinates, serial numbers,
      timestamps, or other PII are written to the output.
    - Provenance fields (platform, export method, filename pattern) must be
      supplied or edited manually — they cannot be extracted from the file.
    - Review all 'unknown_N' fields against FitFileViewer before submitting.
      Do not guess at field meanings.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from fitparse import FitFile
except ImportError:
    print("Error: fitparse is required. Install with: pip install fitparse", file=sys.stderr)
    sys.exit(1)


# Fields that must never appear in output records.
# def_nums are per-message-type, so we track by (message_type, def_num).
# This list covers known PII-bearing fields; extend as needed.
PII_FIELDS = {
    # GPS coordinates
    ("record",  0),   # position_lat
    ("record",  1),   # position_long
    ("session", 3),   # start_position_lat
    ("session", 4),   # start_position_long
    ("session", 29),  # nec_lat
    ("session", 30),  # nec_long
    ("session", 31),  # swc_lat
    ("session", 32),  # swc_long
    ("session", 38),  # end_position_lat
    ("session", 39),  # end_position_long
    ("lap",     3),   # start_position_lat
    ("lap",     4),   # start_position_long
    ("lap",     5),   # end_position_lat
    ("lap",     6),   # end_position_long
    ("lap",     27),  # nec_lat
    ("lap",     28),  # nec_long
    ("lap",     29),  # swc_lat
    ("lap",     30),  # swc_long
}

# Message types to analyse for field presence.
# Extend this list to cover additional message types as the reference grows.
ANALYSE_MESSAGE_TYPES = {"record", "session", "lap"}


def analyse_fields(fit_path: Path, analyse_types: set) -> dict:
    """Extract field presence from a FIT file. Returns per-message-type field data."""
    fit = FitFile(str(fit_path))
    fields = defaultdict(lambda: defaultdict(lambda: {
        "def_num": None,
        "statuses": set(),
    }))
    message_counts = defaultdict(int)

    for record in fit.get_messages():
        msg = record.name
        message_counts[msg] += 1
        if msg not in analyse_types:
            continue
        for field in record.fields:
            entry = fields[msg][field.name]
            entry["def_num"] = field.def_num
            if field.value is not None:
                entry["statuses"].add("populated")
            else:
                entry["statuses"].add("empty")

    return dict(fields), dict(message_counts)


def build_field_list(msg_type: str, field_data: dict) -> list:
    """Convert raw field data into the record schema field list, stripping PII."""
    result = []
    for name, entry in sorted(field_data.items(), key=lambda x: x[1]["def_num"] or 9999):
        def_num = entry["def_num"]

        # Strip PII fields — record as noted rather than omitting silently
        if (msg_type, def_num) in PII_FIELDS:
            statuses = entry["statuses"]
            status = "mixed" if len(statuses) > 1 else list(statuses)[0]
            result.append({
                "def_num": def_num,
                "name": name,
                "status": status,
                "registry_status": "sdk",
                "notes": "PII — coordinates stripped from record. Field presence confirmed."
            })
            continue

        statuses = entry["statuses"]
        status = "mixed" if len(statuses) > 1 else list(statuses)[0]
        result.append({
            "def_num": def_num,
            "name": name,
            "status": status,
            "registry_status": "new",  # Analyst must classify; 'new' is the safe default
        })
    return result


def build_record(args, fields: dict, message_counts: dict) -> dict:
    """Assemble the full record structure."""
    record_id = f"{args.manufacturer}-{args.product}-{args.platform}-{args.source_type}-{args.sport}-{args.sequence}"

    return {
        "record_id": record_id,
        "schema_version": "0.1.0",

        "provenance": {
            "source_type": args.source_type,
            "platform": args.platform,
            "export_method": "TODO — describe the export path used",
            "filename_pattern": "TODO — document the filename pattern",
            "notes": "TODO — any notable provenance details"
        },

        "devices": {
            "primary": {
                "role": "creator",
                "manufacturer": args.manufacturer,
                "product_name": "TODO — confirm product name",
                "garmin_product_id": None,
                "software_version": "TODO",
                "source_type": "local",
                "device_index": "creator",
                "notes": "TODO — confirm from device_info messages"
            },
            "sensors": [
                {
                    "device_index": "TODO",
                    "device_type": "TODO",
                    "notes": "TODO — enumerate sensors from device_info messages"
                }
            ]
        },

        "activity": {
            "sport": args.sport,
            "sub_sport": "TODO — confirm from session message",
            "display_name": "TODO — value of session def_num 110 if present",
            "num_laps": message_counts.get("lap", 0),
            "num_records": message_counts.get("record", 0),
            "structured_workout": False,
            "notes": "TODO — review and update"
        },

        "message_types": {
            name: {"count": count}
            for name, count in sorted(message_counts.items())
        },

        "fields": {
            msg_type: build_field_list(msg_type, field_data)
            for msg_type, field_data in fields.items()
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Analyse a FIT file for the fit-file-reference repository.")
    parser.add_argument("fit_file", help="Path to the FIT file to analyse")
    parser.add_argument("--manufacturer",  required=True, help="Manufacturer slug (see vocabulary.md)")
    parser.add_argument("--product",       required=True, help="Product slug (see vocabulary.md)")
    parser.add_argument("--platform",      required=True, help="Source platform slug (see vocabulary.md)")
    parser.add_argument("--source-type",   required=True, dest="source_type", help="Source type slug (see vocabulary.md)")
    parser.add_argument("--sport",         required=True, help="Sport slug (see vocabulary.md)")
    parser.add_argument("--sequence",      default="001", help="Record sequence number (default: 001)")
    parser.add_argument("--out",           default=None,  help="Output file path (default: stdout)")
    args = parser.parse_args()

    fit_path = Path(args.fit_file)
    if not fit_path.exists():
        print(f"Error: file not found: {fit_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Analysing {fit_path.name}...", file=sys.stderr)
    fields, message_counts = analyse_fields(fit_path, ANALYSE_MESSAGE_TYPES)
    record = build_record(args, fields, message_counts)

    output = json.dumps(record, indent=2)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output)
        print(f"Written to {out_path}", file=sys.stderr)
        print(f"\nNext steps:", file=sys.stderr)
        print(f"  1. Review all 'registry_status: new' fields against FitFileViewer", file=sys.stderr)
        print(f"  2. Fill in all TODO fields (provenance, devices, activity)", file=sys.stderr)
        print(f"  3. Strip or confirm PII-noted fields", file=sys.stderr)
        print(f"  4. Add a CHANGELOG.md entry for any new findings", file=sys.stderr)
        print(f"  5. Validate against schema/record.schema.json", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
