"""Re-elaborate exact research source and book instances; AuthorityEffect: None."""
from .run_lab import ROOT, COMMITMENTS, build_packet
import re


def ls(values, item=str):
    return '['+', '.join(item(v) for v in values)+']'


def pairs(values):
    return ls(values,lambda p:f'({p[0]}, {p[1]})')


def build_checks():
    base=(ROOT/'research/standing_commitment/lean/StandingCommitment/Base.lean').read_text(encoding='utf-8')
    source=(ROOT/'research/standing_commitment/lean/StandingCommitment/Commitment.lean').read_text(encoding='utf-8')
    imported='import StandingCommitment.Base\n'
    assert source.count(imported)==1
    source=source.replace(imported,'',1)
    lines=[base,source,r'''
namespace Textbook.GrowthLab
open StandingCommitment StandingCommitment.Standing

def adjacent : Commitment where
  holds i j := (i != j) && ((i+1 == j) || (j+1 == i))
  irrefl i := by simp
def evenLabel : Nat → Bool
  | 0 => true
  | n+1 => !(evenLabel n)
def shared_parity : Commitment where
  holds i j := (i != j) && (evenLabel i == evenLabel j)
  irrefl i := by simp
def bounded : Commitment where
  holds i j := (i != j) && decide (i < 4 ∧ j < 4)
  irrefl i := by simp
''']
    names=[]
    packet=build_packet()
    for m in range(16):
        for f in range(4):
            for c in COMMITMENTS:
                row=packet['growth_cases'][f'{m}_{f}_{c}']
                ident=f'{m}_{f}_{c}'
                w='world_'+ident
                lines.append(f'def {w} : World := ⟨{ls(row["data"])}, {ls(row["views"],ls)}, [], [], 0, true, []⟩')
                n='growth_'+ident
                lines.append(f'''theorem {n} :
  demands {c} {w} = {pairs(row['before'])} ∧
  demands {c} (grow {w} 4) = {pairs(row['after'])} ∧
  (demands {c} (grow {w} 4)).length = {len(row['after'])} := by decide
''')
                names.append('Textbook.GrowthLab.'+n)
    lines.append('end Textbook.GrowthLab')
    reports=(ROOT/'research/standing_commitment/lean/StandingCommitment/AxiomReport.lean').read_text(encoding='utf-8')
    native=[line.removeprefix('#print axioms ') for line in reports.splitlines() if line.startswith('#print axioms ')]
    assert len(native)==14
    declared={'StandingCommitment.Standing.'+n for n in re.findall(r'^theorem (\w+)',source,re.M)}
    assert declared==set(native), 'Research theorem census differs from the report list'
    lines.extend('#print axioms '+n for n in names+native)
    return '\n'.join(lines), names+native
