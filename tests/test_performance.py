"""Performance tests for code tokenizer."""

import concurrent.futures
import random
import string
import time
from pathlib import Path

from code_tokenizer.core.tokenizer import count_tokens
from code_tokenizer.services.tokenizer_service import TokenizerService


class TestPerformance:
    """Test performance of different components."""

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

        results = {}

        # Benchmark each test case
        for name, text in test_cases.items():
            start_time = time.time()
            token_count = count_tokens(text, "claude-3-sonnet")
            duration = time.time() - start_time

            results[name] = {
                "tokens": token_count,
                "chars": len(text),
                "duration": duration,
                "tokens_per_sec": token_count / duration,
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
        for stats in results.values():
            assert stats["tokens_per_sec"] > 1000, "Token counting performance below threshold"

    def test_file_processing_performance(self, temp_dir):
        """Benchmark file processing performance."""
        # Create test files
        file_sizes = {"tiny": 100, "small": 1000, "medium": 10000, "large": 100000}

        files_created = {}
        for size_name, size in file_sizes.items():
            # Create 5 files of each size
            for i in range(5):
                content = "".join(
                    random.choices(string.ascii_letters + string.digits + "\n", k=size)
                )
                file_path = Path(temp_dir) / f"{size_name}_{i}.txt"
                file_path.write_text(content)
                files_created[str(file_path)] = size

        # Initialize tokenizer service
        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "max_tokens_per_file": 5000,
            "output_format": "markdown",
        }
        tokenizer = TokenizerService(config)

        # Measure processing time for each file
        results = {}
        for file_path, size in files_created.items():
            start_time = time.time()
            result = tokenizer.process_file(file_path)
            duration = time.time() - start_time

            size_category = next(name for name, s in file_sizes.items() if size == s)
            if size_category not in results:
                results[size_category] = []
            results[size_category].append(
                {
                    "duration": duration,
                    "tokens": result["tokens"] if result["success"] else 0,
                    "chars": size,
                }
            )

        # Calculate and print averages
        print("\nFile Processing Performance:")
        for category, measurements in results.items():
            avg_duration = sum(m["duration"] for m in measurements) / len(measurements)
            avg_tokens = sum(m["tokens"] for m in measurements) / len(measurements)
            avg_chars = sum(m["chars"] for m in measurements) / len(measurements)

            print(f"\n{category.title()} Files (avg of {len(measurements)}):")
            print(f"- Size: {avg_chars:,.0f} chars")
            print(f"- Tokens: {avg_tokens:,.0f}")
            print(f"- Duration: {avg_duration:.4f} seconds")
            print(f"- Processing speed: {avg_chars/avg_duration:,.0f} chars/sec")

        # Verify performance thresholds
        for measurements in results.values():
            avg_duration = sum(m["duration"] for m in measurements) / len(measurements)
            avg_chars = sum(m["chars"] for m in measurements) / len(measurements)
            processing_speed = avg_chars / avg_duration
            assert processing_speed > 10000, "File processing performance below threshold"

    def test_concurrent_processing_performance(self, temp_dir):
        """Test performance of concurrent file processing."""
        # Create test files
        num_files = 50
        file_size = 1000
        test_files = []

        for i in range(num_files):
            content = f"Test content for file {i}\n" * 20
            file_path = Path(temp_dir) / f"test_{i}.txt"
            file_path.write_text(content)
            test_files.append(str(file_path))

        config = {
            "base_dir": temp_dir,
            "model_name": "claude-3-sonnet",
            "max_tokens_per_file": 2000,
        }
        tokenizer = TokenizerService(config)

        # Sequential processing
        start_time = time.time()
        sequential_results = [tokenizer.process_file(f) for f in test_files]
        sequential_duration = time.time() - start_time

        # Concurrent processing
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            concurrent_results = list(executor.map(tokenizer.process_file, test_files))
        concurrent_duration = time.time() - start_time

        # Print results
        print("\nConcurrent Processing Performance:")
        print(f"Sequential processing: {sequential_duration:.4f} seconds")
        print(f"Concurrent processing: {concurrent_duration:.4f} seconds")
        print(f"Speedup: {sequential_duration/concurrent_duration:.2f}x")

        # Verify results are the same
        assert len(sequential_results) == len(concurrent_results)
        for seq, conc in zip(sequential_results, concurrent_results):
            assert seq["success"] == conc["success"]
            if seq["success"]:
                assert seq["tokens"] == conc["tokens"]

        # Verify performance improvement
        assert (
            concurrent_duration < sequential_duration
        ), "Concurrent processing not faster than sequential"
