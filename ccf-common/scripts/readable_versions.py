"""Human-readable file stamps for optional CCFA state, without content hashing.

A stamp is a visible UTC modification time and byte count. It is a lightweight
single-editor conflict signal, not a cryptographic verification of file content.
"""
from datetime import datetime, timezone
from pathlib import Path


def file_stamp(path):
    info = Path(path).stat()
    timestamp = datetime.fromtimestamp(info.st_mtime, timezone.utc)
    return f"{timestamp.isoformat(timespec='microseconds')} | {info.st_size} bytes"


def describe_size(value):
    return f"{len(value)} bytes"


def is_stamp(value):
    return isinstance(value, str) and " | " in value and value.endswith(" bytes")
