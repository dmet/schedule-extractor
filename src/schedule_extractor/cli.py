from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="schedule-extract")
    parser.add_argument("pdf", help="Path to a construction-schedule PDF")
    parser.add_argument("--out", default="-", help="Output path (CSV) or '-' for stdout")
    args = parser.parse_args(argv)

    del args  # pipeline not implemented yet
    print("schedule-extract: pipeline not implemented yet", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
