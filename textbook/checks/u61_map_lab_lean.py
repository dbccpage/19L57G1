"""Kernel-check the map lab's exact native correspondence; AuthorityEffect: None."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from booklean import BOTH, NONE, PROPEXT, QUOT, main  # noqa: E402
from textbook.map_lab.lean_cases import build_checks  # noqa: E402
from textbook.map_lab.native_paths_lean import expected_native_reports  # noqa: E402

if __name__ == "__main__":
    source, names = build_checks()
    expected = {n: BOTH for n in names}
    for name in names:
        if '.representation_' in name:
            expected[name] = PROPEXT
    for name in ('Textbook.MapLab.factor_chain', 'Compression.factor_unique_on_image',
                 'Compression.factor_not_unique_off_image', 'ObsDescent.classConstant_pair_iff',
                 'ObsDescent.fiberConstant_fixed_D_not_classConstant'):
        expected[name] = NONE
    for name in ('Textbook.MapLab.blue_class_constant', 'Textbook.MapLab.triangle_not_class_constant',
                 'Textbook.MapLab.pair_not_class_constant'):
        expected[name] = PROPEXT
    for name in ('ObsDescent.descend_unique', 'ObsDescent.descend_iff_factorsOn_all'):
        expected[name] = QUOT
    expected.update(expected_native_reports())
    raise SystemExit(main(source, expected, "MapLab"))
