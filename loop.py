import argparse
import sys
from pathlib import Path
from autoresearch.loop import AutoresearchLoop
from autoresearch.report import generate_report
from autoresearch.paths import STATE_DIR

def main():
    parser = argparse.ArgumentParser(description="Autoresearch Loop CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Run command
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--max-iters", type=int, default=None)
    run_parser.add_argument("--limit", type=int, default=None)
    run_parser.add_argument("--artifact", type=str, required=True)
    run_parser.add_argument("--dataset", type=str, required=True)
    run_parser.add_argument("--model", type=str, default="gemma-31b")

    # Report command
    subparsers.add_parser("report")

    # Reset command
    subparsers.add_parser("reset")

    args = parser.parse_args()

    if args.command == "run":
        loop = AutoresearchLoop(
            initial_artifact=args.artifact,
            dataset_dir=Path(args.dataset),
            scorer_cli="dredd.py",
            model_name=args.model
        )
        loop.run(max_iters=args.max_iters)
    elif args.command == "report":
        generate_report()
    elif args.command == "reset":
        import shutil
        if STATE_DIR.exists():
            shutil.rmtree(STATE_DIR)
        print("State reset.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
