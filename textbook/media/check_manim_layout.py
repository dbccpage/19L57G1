"""Check actual Manim text bounds at each settled animation state.

AuthorityEffect: None. These geometry checks do not certify mathematical
claims or measure whether a viewer has enough time to read a caption.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from manim import Text, config, tempconfig
import render_manim_suite as suite


def check_text_bounds(scene) -> None:
    texts = {
        id(member): member
        for mob in scene.mobjects
        for member in mob.get_family()
        if isinstance(member, Text)
    }
    visible = list(texts.values())
    for text in visible:
        assert text.get_left()[0] >= -config.frame_width / 2, text.text
        assert text.get_right()[0] <= config.frame_width / 2, text.text
        assert text.get_bottom()[1] >= -config.frame_height / 2, text.text
        assert text.get_top()[1] <= config.frame_height / 2, text.text
    for index, left in enumerate(visible):
        for right in visible[index + 1:]:
            dx = min(left.get_right()[0], right.get_right()[0]) - max(left.get_left()[0], right.get_left()[0])
            dy = min(left.get_top()[1], right.get_top()[1]) - max(left.get_bottom()[1], right.get_bottom()[1])
            assert dx <= 0.01 or dy <= 0.01, f"Overlapping text: {left.text!r} / {right.text!r}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, default=Path("artifacts2/manim_layout"))
    parser.add_argument("--scene", choices=[slug for _, slug in suite.SCENES], action="append")
    args = parser.parse_args()
    with tempconfig({"media_dir": str(args.work_dir.resolve()), "quality": "low_quality",
                     "skip_animations": True, "write_to_movie": False,
                     "save_last_frame": True, "disable_caching": True,
                     "verbosity": "ERROR", "progress_bar": "none"}):
        for class_name, slug in suite.SCENES:
            if args.scene and slug not in args.scene:
                continue
            base = getattr(suite, class_name)

            class CheckedScene(base):
                states = 0

                def play(self, *animations, **kwargs):
                    super().play(*animations, **kwargs)
                    check_text_bounds(self)
                    self.states += 1

            config.output_file = slug
            scene = CheckedScene()
            scene.render()
            print(f"PASS: {slug}: {scene.states} settled states")


if __name__ == "__main__":
    main()
