"""Allow lottery_runner to be executable through `python -m lottery_runner`."""
from lottery_runner.cli import main


if __name__ == "__main__":  # pragma: no cover
    main(prog_name="lottery_runner")