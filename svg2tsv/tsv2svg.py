#!/usr/bin/env python3

import argparse
import numpy as np
import os
import svgwrite
import re


def parse_tuple(s):
    match = re.match(r"\(([^,]+),([^\)]+)\)", s)
    if match:
        return complex(float(match.group(1)), float(match.group(2)))
    return None


def calculate_bounding_box(all_points):
    min_x = min(point.real for path in all_points for point in path)
    min_y = min(point.imag for path in all_points for point in path)
    max_x = max(point.real for path in all_points for point in path)
    max_y = max(point.imag for path in all_points for point in path)
    return min_x, min_y, max_x, max_y


def tsv_to_svg(input_file, output_file, stroke_color="black", stroke_width=1):
    data = np.genfromtxt(input_file, delimiter="\t", dtype=str)

    # Extract headers
    headers = data[0, :]
    all_path_points = []
    path_names = headers.tolist()

    # Process each column
    for idx in range(data.shape[1]):
        path_points = []
        for row in data[1:, idx]:
            point = parse_tuple(row)
            if point:
                path_points.append(point)
        all_path_points.append(path_points)

    if not all_path_points:
        print("No valid points found.")
        return

    # Calculate bounding box
    min_x, min_y, max_x, max_y = calculate_bounding_box(all_path_points)
    width = max_x - min_x
    height = max_y - min_y

    # Create an SVG drawing with calculated size and viewBox
    dwg = svgwrite.Drawing(
        output_file,
        size=(f"{width}px", f"{height}px"),
        viewBox=f"{min_x} {min_y} {width} {height}",
    )

    # Add paths with names from headers
    for name, path_points in zip(path_names, all_path_points):
        if not path_points:
            continue
        path_data = "M " + " L ".join(f"{pt.real},{pt.imag}" for pt in path_points)
        dwg.add(
            dwg.path(
                d=path_data,
                stroke=stroke_color,
                fill="none",
                stroke_width=stroke_width,
                id=name,
            )
        )

    dwg.save()
    print(f"SVG saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a TSV matrix with headers back to an SVG file."
    )
    parser.add_argument(
        "-i", "--input-file", required=True, help="Input TSV file path."
    )
    parser.add_argument("-o", "--output-file", help="Output SVG file to save.")
    parser.add_argument(
        "--stroke-color", default="black", help="Stroke color for SVG paths."
    )
    parser.add_argument(
        "--stroke-width", type=float, default=1.0, help="Stroke width for SVG paths."
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    if not output_file:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.svg"

    tsv_to_svg(input_file, output_file, args.stroke_color, args.stroke_width)


if __name__ == "__main__":
    main()
