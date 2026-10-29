"""Command line entry point.

    python -m erp                    progress board of every module
    python -m erp inventory          progress board of one module
    python -m erp demo               run the finished tasks on the real data
    python -m erp demo crm           same, for one module
"""

import sys

from erp.common import board, demo


def main(argv: list[str]) -> None:
    if sys.version_info < (3, 11):
        sys.exit(f"Python 3.11 or newer is required (you have {sys.version.split()[0]}). "
                 "Check that your virtual environment is activated.")
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # emojis on Windows consoles
    except (AttributeError, ValueError):
        pass
    if argv and argv[0] == "demo":
        demo.run(argv[1:])
    else:
        board.run(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
