"""Merge multiple PDF files into one PDF."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence, Union

from pypdf import PdfReadError, PdfWriter


PathInput = Union[str, Path]


def merge_pdfs(input_paths: Sequence[PathInput], output_path: PathInput) -> None:
    """Append every page from each input PDF to the output PDF in order."""
    if not input_paths:
        raise ValueError("Provide at least one input PDF.")

    sources = [Path(path) for path in input_paths]
    output = Path(output_path)
    output_resolved = output.resolve()

    for source in sources:
        if not source.is_file():
            raise FileNotFoundError(f"Input PDF not found: {source}")
        if source.resolve() == output_resolved:
            raise ValueError("The output PDF cannot also be an input PDF.")

    with PdfWriter() as writer:
        for source in sources:
            writer.append(str(source))
        writer.write(str(output))


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the PDF merger command-line interface."""
    parser = argparse.ArgumentParser(
        description="Merge PDF files into a single output PDF."
    )
    parser.add_argument("output", type=Path, help="path for the merged PDF")
    parser.add_argument(
        "inputs",
        type=Path,
        nargs="+",
        metavar="PDF",
        help="one or more input PDFs, in the order they should be merged",
    )
    args = parser.parse_args(argv)

    try:
        merge_pdfs(args.inputs, args.output)
    except (OSError, PdfReadError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())