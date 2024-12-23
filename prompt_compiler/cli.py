import argparse
import sys
from pathlib import Path
from typing import Optional, List
import yaml

from .compiler import Compiler
from .ai_adapters import GptAdapter, ClaudeAdapter
from .exceptions import PromptCompilerError


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-compiler",
        description="Compile prompt files into code using AI models",
    )

    # Input/Output options
    parser.add_argument(
        "input",
        type=Path,
        help="Input prompt file(s)",
        nargs="+",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output directory (default: current directory)",
        default=Path.cwd(),
    )

    # Compiler options
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        help="Config file path",
        default=Path("prompt-compiler.yaml"),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild, ignore cache",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Cache directory (default: .cache)",
        default=Path(".cache"),
    )

    # AI model options
    model_group = parser.add_argument_group("AI Model Options")
    model_group.add_argument(
        "--model",
        choices=["gpt", "claude"],
        default="gpt",
        help="AI model type to use (default: gpt)",
    )
    model_group.add_argument(
        "--model-name",
        help=(
            "Specific model name (e.g., gpt-4, gpt-3.5-turbo, "
            "claude-3-opus-20240229, claude-3-sonnet-20240229)"
        ),
    )
    model_group.add_argument(
        "--api-key",
        help="API key for the AI model (can also be set in config file)",
    )

    # Output format options
    parser.add_argument(
        "--format",
        choices=["single", "split"],
        default="split",
        help="Output format: single file or split into multiple files (default: split)",
    )

    return parser


def load_config(config_path: Path) -> dict:
    """Load configuration from file."""
    if not config_path.exists():
        return {}

    with open(config_path, "r") as f:
        return yaml.safe_load(f) or {}


def setup_compiler(args: argparse.Namespace, config: dict) -> Compiler:
    """Setup compiler with given arguments and config."""
    # Get API key from args or config
    api_key = args.api_key or config.get("api_key")
    if not api_key:
        raise PromptCompilerError(
            "API key is required. Provide it via --api-key or config file."
        )

    # Get model name from args or config
    model_name = args.model_name or config.get("model_name")

    # Initialize AI adapter
    if args.model == "gpt":
        default_model = "gpt-4"
        adapter = GptAdapter(api_key=api_key, model=model_name or default_model)
    else:  # claude
        default_model = "claude-3-opus-20240229"
        adapter = ClaudeAdapter(api_key=api_key, model=model_name or default_model)

    # Initialize compiler
    return Compiler(
        ai_adapter=adapter,
        cache_dir=args.cache_dir,
    )


def process_output(
    result: dict, output_dir: Path, format: str, prompt_file: Path
) -> None:
    """Process and write compilation results."""
    output_dir.mkdir(parents=True, exist_ok=True)

    if format == "single":
        # Write everything to a single file
        output_file = output_dir / f"{prompt_file.stem}.py"
        content = f"{result['code']}\n\n# Tests\n{result['tests']}"
        output_file.write_text(content)
    else:
        # Split into separate files
        src_dir = output_dir / "src"
        test_dir = output_dir / "tests"

        src_dir.mkdir(exist_ok=True)
        test_dir.mkdir(exist_ok=True)

        (src_dir / f"{prompt_file.stem}.py").write_text(result["code"])
        (test_dir / f"test_{prompt_file.stem}.py").write_text(result["tests"])


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for the compiler CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    try:
        # Load config
        config = load_config(args.config)

        # Setup compiler
        compiler = setup_compiler(args, config)

        # Process each input file
        for prompt_file in args.input:
            if not prompt_file.exists():
                print(f"Error: Input file not found: {prompt_file}", file=sys.stderr)
                continue

            try:
                # Compile prompt
                result = compiler.compile(prompt_file, force_rebuild=args.force)

                # Write output
                process_output(result, args.output_dir, args.format, prompt_file)

                print(f"Successfully compiled {prompt_file}")

            except Exception as e:
                print(f"Error compiling {prompt_file}: {e}", file=sys.stderr)

        return 0

    except PromptCompilerError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
