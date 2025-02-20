import datetime
import json
import shlex
import shutil
import statistics
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple

from rich.console import Console
from rich.panel import Panel

console = Console()


def clean_old_runs(base_dir: Path) -> None:
    """Clean up old benchmark runs.

    Args:
        base_dir: Base directory containing benchmark outputs
    """
    output_dir = base_dir / "outputs"
    if output_dir.exists():
        shutil.rmtree(output_dir)


def create_run_directory(base_dir: Path) -> Tuple[Path, str]:
    """Create a new test run directory with timestamp.

    Args:
        base_dir: Base directory for outputs

    Returns:
        Tuple of run directory path and run ID
    """
    # Create timestamp and run ID
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"run_{timestamp}"

    # Create run directory
    run_dir = base_dir / "outputs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir, run_id


def create_category_directories(run_dir: Path, category: str) -> Path:
    """Create category-specific directories within a run.

    Args:
        run_dir: Test run directory
        category: Category name (e.g., 'performance', 'tokenization')

    Returns:
        Path to category directory
    """
    # Create directory structure:
    # run_dir/
    # └── category/
    #     ├── raw/         (raw command outputs)
    #     ├── analysis/    (analysis files)
    #     └── timings/     (timing data)
    category_dir = run_dir / category

    # Create category subdirectories
    (category_dir / "raw").mkdir(parents=True, exist_ok=True)
    (category_dir / "analysis").mkdir(exist_ok=True)
    (category_dir / "timings").mkdir(exist_ok=True)

    return category_dir


def format_command(cmd: List[str]) -> str:
    """Format command list into a shell-compatible string.

    Args:
        cmd: List of command arguments

    Returns:
        Formatted command string
    """
    return " ".join(shlex.quote(str(arg)) for arg in cmd)


def run_tokenizer(
    directory: str, category_dir: Path, run_id: str, iteration: int, model: str = "gpt-4o"
) -> Tuple[float, Dict, Dict[str, float]]:
    """Run code tokenizer and measure execution time.

    Args:
        directory: Directory to analyze
        category_dir: Category directory
        run_id: Run ID
        iteration: Current iteration
        model: Model to use for tokenization

    Returns:
        Tuple of execution time, statistics, and detailed timings
    """
    # Get category subdirectories
    raw_dir = category_dir / "raw"
    analysis_dir = category_dir / "analysis"
    timings_dir = category_dir / "timings"

    # Define output files
    cli_output_file = raw_dir / f"iter{iteration}.json"
    stdout_file = raw_dir / f"iter{iteration}_stdout.txt"
    stderr_file = raw_dir / f"iter{iteration}_stderr.txt"
    timing_file = timings_dir / f"iter{iteration}.json"
    analysis_file = analysis_dir / f"iter{iteration}.json"

    # Prepare command
    prep_start = time.time()
    cmd = [
        "python",
        "-m",
        "code_tokenizer",
        "-d",
        directory,
        "-o",
        str(cli_output_file),
        "--model",
        model,
        "--format",
        "json",  # Use JSON for easier parsing
    ]

    # Print and log command
    formatted_cmd = format_command(cmd)
    console.print(Panel(formatted_cmd, title="Executing Command", border_style="blue"))
    with open(raw_dir / "commands.log", "a") as f:
        f.write(f"\nIteration {iteration}:\n{formatted_cmd}\n")

    prep_time = time.time() - prep_start

    # Execute command
    exec_start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    exec_time = time.time() - exec_start

    # Save stdout/stderr
    if result.stdout:
        stdout_file.write_text(result.stdout)
        console.print(Panel(result.stdout, title="Command Output", border_style="green"))
    if result.stderr:
        stderr_file.write_text(result.stderr)
        console.print(Panel(result.stderr, title="Command Errors", border_style="red"))

    # Parse output
    parse_start = time.time()
    stats = {}
    if cli_output_file.exists():
        try:
            stats = json.loads(cli_output_file.read_text()).get("stats", {})
            # Save analysis data
            analysis_data = {
                "iteration": iteration,
                "stats": stats,
                "command": formatted_cmd,
                "success": True,
                "errors": result.stderr if result.stderr else None,
            }
            analysis_file.write_text(json.dumps(analysis_data, indent=2))
        except json.JSONDecodeError:
            console.print("[red]Failed to parse JSON output[/red]")
    parse_time = time.time() - parse_start

    total_time = prep_time + exec_time + parse_time

    # Save timing information
    timings = {
        "iteration": iteration,
        "preparation": prep_time,
        "execution": exec_time,
        "parsing": parse_time,
        "total": total_time,
        "timestamp": datetime.datetime.now().isoformat(),
    }
    timing_file.write_text(json.dumps(timings, indent=2))

    return total_time, stats, timings


def run_benchmark(directory: str, category: str = "performance", iterations: int = 5) -> Dict:
    """Run benchmark multiple times and collect statistics.

    Args:
        directory: Directory to analyze
        category: Category of benchmark being run
        iterations: Number of benchmark iterations

    Returns:
        Dictionary containing benchmark results
    """
    # Clean old runs first
    base_dir = Path(__file__).parent.parent
    clean_old_runs(base_dir)

    # Create new run directory and category directories
    run_dir, run_id = create_run_directory(base_dir)
    category_dir = create_category_directories(run_dir, category)

    console.print(f"\n[bold blue]Running {category} benchmark on {directory}[/bold blue]")
    console.print(f"[bold]Number of iterations: {iterations}[/bold]")
    console.print(f"[bold]Run directory: {run_dir}[/bold]")

    times: List[float] = []
    all_stats: List[Dict] = []
    all_timings: List[Dict[str, float]] = []

    for i in range(iterations):
        console.print(f"\n[bold cyan]Iteration {i+1}/{iterations}[/bold cyan]")

        execution_time, stats, timings = run_tokenizer(directory, category_dir, run_id, i + 1)
        times.append(execution_time)
        all_stats.append(stats)
        all_timings.append(timings)

        # Print detailed timing for this iteration
        console.print("\n[bold]Timing Breakdown:[/bold]")
        console.print(f"  Preparation: {timings['preparation']:.3f} seconds")
        console.print(f"  Execution: {timings['execution']:.3f} seconds")
        console.print(f"  Parsing: {timings['parsing']:.3f} seconds")
        console.print(f"  [bold]Total: {timings['total']:.3f} seconds[/bold]")

        console.print("\n[bold]Processing Stats:[/bold]")
        console.print(f"  Files processed: {stats.get('files_processed', 0)}")
        console.print(f"  Total tokens: {stats.get('total_tokens', 0):,}")

    # Calculate statistics
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0

    # Calculate averages
    avg_files = statistics.mean(s.get("files_processed", 0) for s in all_stats)
    avg_tokens = statistics.mean(s.get("total_tokens", 0) for s in all_stats)

    # Calculate average timings
    avg_timings = {
        "preparation": statistics.mean(t["preparation"] for t in all_timings),
        "execution": statistics.mean(t["execution"] for t in all_timings),
        "parsing": statistics.mean(t["parsing"] for t in all_timings),
        "total": statistics.mean(t["total"] for t in all_timings),
    }

    results = {
        "metadata": {
            "run_id": run_id,
            "category": category,
            "timestamp": datetime.datetime.now().isoformat(),
            "directory": directory,
            "iterations": iterations,
        },
        "timing": {
            "average": avg_time,
            "min": min_time,
            "max": max_time,
            "std_dev": std_dev,
            "detailed": avg_timings,
        },
        "processing": {
            "avg_files": avg_files,
            "avg_tokens": avg_tokens,
            "files_per_second": avg_files / avg_time if avg_time > 0 else 0,
            "tokens_per_second": avg_tokens / avg_time if avg_time > 0 else 0,
        },
    }

    # Save category results
    category_summary = category_dir / "summary.json"
    json.dump(results, category_summary.open("w"), indent=2)

    # Save run summary (includes all categories)
    run_summary = run_dir / "summary.json"
    if run_summary.exists():
        run_data = json.loads(run_summary.read_text())
        run_data["categories"][category] = results
    else:
        run_data = {
            "run_id": run_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "categories": {category: results},
        }
    json.dump(run_data, run_summary.open("w"), indent=2)

    return results


def print_results(results: Dict) -> None:
    """Print benchmark results in a formatted way."""
    console.print("\n[bold green]=== Benchmark Results ===[/bold green]")

    metadata = results["metadata"]
    console.print(f"\n[bold]Run ID:[/bold] {metadata['run_id']}")
    console.print(f"[bold]Category:[/bold] {metadata['category']}")
    console.print(f"[bold]Timestamp:[/bold] {metadata['timestamp']}")
    console.print(f"[bold]Directory:[/bold] {metadata['directory']}")
    console.print(f"[bold]Iterations:[/bold] {metadata['iterations']}")

    console.print("\n[bold]Timing Statistics:[/bold]")
    timing = results["timing"]
    console.print(f"  Average: {timing['average']:.2f} seconds")
    console.print(f"  Minimum: {timing['min']:.2f} seconds")
    console.print(f"  Maximum: {timing['max']:.2f} seconds")
    console.print(f"  Std Dev: {timing['std_dev']:.2f} seconds")

    console.print("\n[bold]Average Timing Breakdown:[/bold]")
    detailed = timing["detailed"]
    console.print(f"  Preparation: {detailed['preparation']:.3f} seconds")
    console.print(f"  Execution: {detailed['execution']:.3f} seconds")
    console.print(f"  Parsing: {detailed['parsing']:.3f} seconds")
    console.print(f"  [bold]Total: {detailed['total']:.3f} seconds[/bold]")

    console.print("\n[bold]Processing Statistics:[/bold]")
    proc = results["processing"]
    console.print(f"  Average Files: {proc['avg_files']:.1f}")
    console.print(f"  Average Tokens: {proc['avg_tokens']:,.0f}")
    console.print(f"  Files/Second: {proc['files_per_second']:.2f}")
    console.print(f"  Tokens/Second: {proc['tokens_per_second']:,.0f}")


if __name__ == "__main__":
    # Directory to benchmark
    target_dir = str(Path(__file__).parent.parent)

    # Run benchmark
    results = run_benchmark(target_dir, category="performance")

    # Print results
    print_results(results)
