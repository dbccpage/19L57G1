"""Publication figures. AuthorityEffect: None."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from nsa000.gauges import Castle, better, height_measure, width_measure
from nsa000.ties import cost_two_orientations, iso_classes


def sandcastle_figure(path: Path) -> Path:
    tall = Castle("A", height=3.0, width=1.0)
    wide = Castle("B", height=1.0, width=3.0)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    labels = ["height measure", "width measure"]
    winners = [
        better(tall, wide, height_measure),
        better(tall, wide, width_measure),
    ]
    colors = ["#3d5a80" if w == "A" else "#ee6c4d" for w in winners]
    ax.bar(labels, [1, 1], color=colors)
    ax.set_ylim(0, 1.4)
    ax.set_ylabel("winner (unit bar)")
    ax.set_title("Same two castles; opposite winners")
    for i, w in enumerate(winners):
        ax.text(i, 1.05, f"winner {w}", ha="center")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def tie_figure(path: Path) -> Path:
    items = cost_two_orientations()
    classes = iso_classes(items)
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    ax.bar(
        ["concrete responses", "iso-classes after flip"],
        [len(items), len(classes)],
        color=["#293241", "#98c1d9"],
    )
    ax.set_ylim(0, 4)
    ax.set_title("A tie remains after the cheap quotient")
    ax.set_ylabel("count")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def write_default(export_dir: Path) -> tuple[Path, Path]:
    a = sandcastle_figure(export_dir / "fig_sandcastles.png")
    b = tie_figure(export_dir / "fig_tie.png")
    return a, b
