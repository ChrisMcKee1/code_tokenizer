"""Performance tests for code tokenizer."""

import concurrent.futures
import time
from pathlib import Path

import pytest

from code_tokenizer.core.tokenizer import count_tokens
from code_tokenizer.services.filesystem_service import MockFileSystemService
from code_tokenizer.services.tokenizer_service import TokenizerService


class TestPerformance:
    """Test performance of different components."""

    @pytest.mark.performance
    @pytest.mark.benchmark
    def test_token_counting_performance(self):
        """Benchmark token counting performance with different inputs."""
        # Test data
        test_cases = {
            "small": "Hello, World!" * 10,
            "medium": "def test_function():\n    pass\n" * 100,
            "large": "".join([f"line_{i} = value_{i}\n" for i in range(1000)]),
            "mixed": "\n".join(
                [
                    "# Python code",
                    "def hello():",
                    "    print('Hello!')",
                    "# JSON data",
                    '{"key": "value"}',
                    "# Markdown",
                    "## Heading",
                    "Some text",
                ]
                * 50
            ),
        }

        # Warm up the tokenizer
        warmup_text = "warmup" * 100
        for _ in range(5):
            count_tokens(warmup_text, "gpt-4o")

        results = {}
        num_runs = 3  # Number of runs for each test case

        # Benchmark each test case
        for name, text in test_cases.items():
            best_tokens_per_sec = 0
            token_count = 0

            # Run multiple times and take the best performance
            for _ in range(num_runs):
                start_time = time.time()
                tokens = count_tokens(text, "gpt-4o")
                duration = time.time() - start_time
                tokens_per_sec = tokens / duration

                if tokens_per_sec > best_tokens_per_sec:
                    best_tokens_per_sec = tokens_per_sec
                    token_count = tokens

            results[name] = {
                "tokens": token_count,
                "chars": len(text),
                "duration": duration,
                "tokens_per_sec": best_tokens_per_sec,
            }

        # Print results
        print("\nToken Counting Performance:")
        for name, stats in results.items():
            print(f"\n{name.title()} Text:")
            print(f"- Tokens: {stats['tokens']:,}")
            print(f"- Characters: {stats['chars']:,}")
            print(f"- Duration: {stats['duration']:.4f} seconds")
            print(f"- Tokens/sec: {stats['tokens_per_sec']:,.0f}")

        # Verify performance thresholds
        assert (
            results["medium"]["tokens_per_sec"] > 1000
        ), "Token counting performance below threshold"

    @pytest.mark.performance
    @pytest.mark.benchmark
    def test_file_processing_performance(self, temp_dir):
        """Test file processing performance."""
        # Create test files
        num_files = 100
        files_created = []

        for i in range(num_files):
            file_path = temp_dir / f"test_{i}.py"
            content = f"""
def function_{i}():
    # Some comments
    x = {i} * 2
    return x + {i}

class TestClass_{i}:
    def method_{i}(self):
        pass

# Main execution
value = function_{i}()
"""
            file_path.write_text(content)
            files_created.append(file_path)

        # Initialize tokenizer service
        config = {
            "base_dir": str(temp_dir),
            "model_name": "gpt-4o",
            "max_tokens_per_file": 5000,
            "output_format": "markdown",
        }
        service = TokenizerService(config)

        # Measure processing time
        start_time = time.time()
        service.process_directory(str(temp_dir))
        duration = time.time() - start_time

        # Calculate metrics
        total_size = sum(f.stat().st_size for f in files_created)
        files_per_second = num_files / duration
        bytes_per_second = total_size / duration

        # Print performance metrics
        print("\nFile Processing Performance:")
        print(f"- Files processed: {num_files}")
        print(f"- Total size: {total_size:,} bytes")
        print(f"- Duration: {duration:.2f} seconds")
        print(f"- Files/second: {files_per_second:.2f}")
        print(f"- MB/second: {(bytes_per_second / 1_048_576):.2f}")

        # Assert reasonable performance
        assert files_per_second >= 1, "File processing performance below threshold"
        assert bytes_per_second >= 1000, "Data processing performance below threshold"

    @pytest.mark.performance
    @pytest.mark.benchmark
    def test_concurrent_processing_performance(self, temp_dir):
        """Test performance of concurrent file processing."""
        # Create test files
        num_files = 50
        test_files = []

        for i in range(num_files):
            content = f"Test content for file {i}\n" * 20
            file_path = Path(temp_dir) / f"test_{i}.txt"
            file_path.write_text(content)
            test_files.append(str(file_path))

        config = {
            "base_dir": temp_dir,
            "model_name": "gpt-4o",
            "max_tokens_per_file": 2000,
        }
        tokenizer = TokenizerService(config)

        # Sequential processing
        start_time = time.time()
        sequential_results = [tokenizer.process_file(f) for f in test_files[:10]]
        sequential_duration = time.time() - start_time

        # Concurrent processing
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            concurrent_results = list(executor.map(tokenizer.process_file, test_files[:10]))
        concurrent_duration = time.time() - start_time

        # Print results
        print("\nConcurrent Processing Performance:")
        print(f"Sequential processing: {sequential_duration:.4f} seconds")
        print(f"Concurrent processing: {concurrent_duration:.4f} seconds")
        print(f"Speedup: {sequential_duration / concurrent_duration:.2f}x")

        # Verify results are the same
        assert len(sequential_results) == len(concurrent_results)
        for seq, conc in zip(sequential_results, concurrent_results):
            assert seq["success"] == conc["success"]
            if seq["success"]:
                assert seq["tokens"] == conc["tokens"]

    def _measure_concurrent_processing(self, num_files):
        """Implementation of concurrent processing measurement."""
        pass

    def _measure_sequential_processing(self, num_files):
        """Implementation of sequential processing measurement."""
        pass


def test_large_file_performance(mock_fs: MockFileSystemService):
    """Test performance with a large file."""
    # Create a large file with repeated content
    content = "def test_function():\n    pass\n" * 1000
    mock_fs.add_file("/test/large_file.py", content)

    service = TokenizerService(mock_fs)
    service.process_files(["/test/large_file.py"])
