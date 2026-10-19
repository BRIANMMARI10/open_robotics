"""Matplotlib visualization helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from orient_print.models.orientation import OrientationSequence
from orient_print.phase1_baseline.analysis import BaselineReport
from orient_print.phase1_planning.deposition_analysis import DepositionCandidate


def _face_colors(mesh: trimesh.Trimesh, highlight_indices: set[int], highlight_rgba: tuple) -> np.ndarray:
    colors = np.tile([0.7, 0.7, 0.75, 0.6], (len(mesh.faces), 1))
    for i in highlight_indices:
        colors[i] = highlight_rgba
    return colors


def plot_baseline_overhangs(
    mesh: trimesh.Trimesh,
    report: BaselineReport,
    output_path: Path | None = None,
    show: bool = False,
) -> None:
    """Color overhang faces red on the mesh."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    overhang_set = set(report.overhang_face_indices)
    colors = _face_colors(mesh, overhang_set, (0.9, 0.2, 0.2, 0.9))

    verts = mesh.vertices
    tris = [verts[f] for f in mesh.faces]
    coll = Poly3DCollection(tris, facecolors=colors, edgecolors="none")
    ax.add_collection3d(coll)

    _set_axes_equal(ax, mesh.bounds)
    ax.set_title(
        f"Baseline overhangs (>{report.overhang_angle_threshold_deg:.0f}°): "
        f"{report.overhang_face_count} faces, {100 * report.overhang_area_fraction:.1f}% area"
    )
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_zlabel("Z [mm]")

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)


def plot_deposition_candidates(
    mesh: trimesh.Trimesh,
    candidates: list[DepositionCandidate],
    top_n: int,
    output_path: Path | None = None,
    show: bool = False,
) -> None:
    """Bar chart of top deposition direction scores."""
    top = candidates[:top_n]
    labels = [f"[{c.direction[0]:+.0f},{c.direction[1]:+.0f},{c.direction[2]:+.0f}]" for c in top]
    areas = [c.printable_area_mm2 for c in top]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(labels[::-1], areas[::-1], color="steelblue")
    ax.set_xlabel("Printable area [mm²]")
    ax.set_title(f"Top {len(top)} deposition direction candidates")
    plt.tight_layout()

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)


def plot_orientation_sequence(
    mesh: trimesh.Trimesh,
    sequence: OrientationSequence,
    output_path: Path | None = None,
    show: bool = False,
) -> None:
    """One subplot per orientation step showing covered faces."""
    n = len(sequence.steps)
    if n == 0:
        return

    cols = min(3, n)
    rows = (n + cols - 1) // cols
    fig = plt.figure(figsize=(5 * cols, 4 * rows))

    cmap = plt.cm.Set1

    for i, step in enumerate(sequence.steps):
        ax = fig.add_subplot(rows, cols, i + 1, projection="3d")
        covered = set(step.printable_face_indices)
        colors = _face_colors(mesh, covered, (*cmap(i % 9)[:3], 0.95))

        verts = mesh.vertices
        tris = [verts[f] for f in mesh.faces]
        coll = Poly3DCollection(tris, facecolors=colors, edgecolors="none")
        ax.add_collection3d(coll)

        d = step.deposition_direction
        _set_axes_equal(ax, mesh.bounds)
        ax.set_title(f"Step {step.index}: d=[{d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f}]\n{step.notes}")

    fig.suptitle(f"Orientation sequence ({sequence.num_reorientations} reorientations)")
    plt.tight_layout()

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)


def _set_axes_equal(ax, bounds: np.ndarray) -> None:
    mins, maxs = bounds[0], bounds[1]
    center = (mins + maxs) / 2
    radius = float(np.max(maxs - mins) / 2) * 1.1
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)
