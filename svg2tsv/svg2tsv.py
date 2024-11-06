#!/usr/bin/env python3
import argparse
import numpy as np
from svgpathtools import svg2paths
import sys
import os


def sample_path_segment(segment, npoints):
    """
    Samples `npoints` evenly spaced points along a path segment.
    """
    t_values = np.linspace(0, 1, npoints)
    return np.array([segment.point(t) for t in t_values])


def extract_path_points_from_svg(file_path, npoints, filter_option):
    # Load all paths and attributes from the SVG file
    paths, attributes = svg2paths(file_path)

    # Filter paths based on the filter_option
    if filter_option == "closed":
        filtered = [
            (path, attr) for path, attr in zip(paths, attributes) if path.isclosed()
        ]
    elif filter_option == "open":
        filtered = [
            (path, attr) for path, attr in zip(paths, attributes) if not path.isclosed()
        ]
    else:
        filtered = list(zip(paths, attributes))  # "all"

    if not filtered:
        print(f"No paths match the filter: {filter_option}")
        sys.exit(1)

    all_path_points = []
    path_names = []

    for idx, (path, attr) in enumerate(filtered):
        name = attr.get("id") or attr.get("name") or f"path{idx+1}"
        path_names.append(name)
        path_points = []
        for segment in path:
            segment_points = sample_path_segment(segment, npoints)
            path_points.extend(segment_points)
        all_path_points.append(path_points)

    return all_path_points, path_names


def main():
    parser = argparse.ArgumentParser(
        description="Extract points from SVG paths and save as a TSV matrix with headers. Each SVG path occupies a column."
    )
    parser.add_argument(
        "-n",
        "--points-per-path",
        type=int,
        default=100,
        help="Number of points to sample per path segment.",
    )
    parser.add_argument(
        "-i", "--input-file", required=True, help="Input SVG file path."
    )
    parser.add_argument(
        "-o", "--output-file", help="Output TSV file to save the matrix."
    )
    parser.add_argument(
        "-f",
        "--filter",
        choices=["all", "closed", "open"],
        default="all",
        help='Filter paths: "all" (default), "closed", or "open".',
    )

    args = parser.parse_args()

    file_path = args.input_file
    npoints = args.points_per_path
    output_file = args.output_file
    filter_option = args.filter

    if not output_file:
        base, _ = os.path.splitext(file_path)
        output_file = f"{base}.tsv"

    # Extract path points and names with filtering
    all_path_points, path_names = extract_path_points_from_svg(
        file_path, npoints, filter_option
    )

    # Find the maximum number of points among all paths to pad shorter paths
    max_points = max(len(points) for points in all_path_points)

    # Prepare the matrix with empty strings for padding, including header row
    matrix = np.full(
        (max_points + 1, len(all_path_points)),
        "",
        dtype="<U26",  # Adjust the Unicode string length as needed
    )

    # Insert headers
    matrix[0, :] = path_names

    # Insert data
    for idx, path_points in enumerate(all_path_points):
        path_points_array = [f"({pt.real:.6f},{pt.imag:.6f})" for pt in path_points]
        num_points = len(path_points_array)
        matrix[1 : num_points + 1, idx] = path_points_array

    # Save the matrix to the output file as TSV
    np.savetxt(output_file, matrix, delimiter="\t", fmt="%s")

    print(f"Matrix saved to {output_file}")


if __name__ == "__main__":
    main()
