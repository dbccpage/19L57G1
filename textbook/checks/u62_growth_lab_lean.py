"""Check actual research proofs and growth instances; AuthorityEffect: None."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from booklean import main, PROPEXT, BOTH, NONE  # noqa: E402
from textbook.growth_lab.lean_cases import build_checks  # noqa: E402
if __name__ == '__main__':
    source,names=build_checks()
    expected={n:BOTH for n in names}
    expected['StandingCommitment.Standing.pairsOf_cons']=NONE
    expected['StandingCommitment.Standing.pairsOf_length_cons']=PROPEXT
    expected['StandingCommitment.Standing.filter_of_false']=PROPEXT
    raise SystemExit(main(source,expected,'GrowthLab'))
