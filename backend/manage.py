import os
import sys


def main():

    # AutoInsight project root
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    sys.path.insert(
        0,
        project_root
    )

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "backend.settings"
    )

    try:
        from django.core.management import (
            execute_from_command_line
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()