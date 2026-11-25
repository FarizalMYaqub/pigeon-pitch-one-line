"""Pigeon Pitch, One Line.

Writes the pigeon's one-line elevator pitch to /output/entry.txt.
The line must fit the gate: UTF-8 text, 1 to 200 characters, and not
only white space. The pitch is kept as data here, checked once, and
flushed to disk in a way that never leaves a torn file behind.
"""

import os

PITCH = (
    "We're Uber for breadcrumbs: 4,000 daily users, zero churn, and "
    "every park bench in this city is already our distribution network."
)

TARGET = os.path.join("/output", "entry.txt")
LIMIT = 200


class GateError(RuntimeError):
    pass


def check_gate(text):
    if text is None or text.strip() == "":
        raise GateError("blank pitch")
    if not 1 <= len(text) <= LIMIT:
        raise GateError("pitch is %d chars, gate allows 1-%d" % (len(text), LIMIT))
    if "\n" in text or "\r" in text:
        raise GateError("pitch must stay on one line")
    text.encode("utf-8")
    return text


def publish(text, target=TARGET):
    folder = os.path.dirname(target)
    os.makedirs(folder, exist_ok=True)
    scratch = target + ".part"
    with open(scratch, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.rename(scratch, target)
    with open(target, "r", encoding="utf-8") as fh:
        if fh.read() != text:
            raise GateError("published pitch does not match the source line")
    return target


def main():
    line = check_gate(PITCH)
    out = publish(line)
    print("pitch published: %d chars -> %s" % (len(line), out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
