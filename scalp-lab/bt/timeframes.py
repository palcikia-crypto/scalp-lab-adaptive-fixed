"""Validated timeframe conversion helpers."""
import re

_UNITS = {"m": 1, "h": 60, "d": 1440}


def tf_to_minutes(tf):
    if not isinstance(tf, str):
        raise ValueError("timeframe must be a string")

    match = re.fullmatch(r"([1-9][0-9]*)([mhd])", tf.strip().lower())
    if not match:
        raise ValueError("unsupported timeframe: %r" % (tf,))

    return int(match.group(1)) * _UNITS[match.group(2)]
