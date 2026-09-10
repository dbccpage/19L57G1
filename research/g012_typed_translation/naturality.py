"""Signature renamings, functoriality, naturality, and rational distortion vectors.

Formalizes signature morphisms, structure translation functoriality,
commutation between renamings and relational encoding, and exact rational
distortion vectors in Q (fractions.Fraction).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import re
from typing import Mapping

try:
    from codec import RelationalState, encode
    from signature import (
        ConstantSymbol,
        FunctionSymbol,
        RelationSymbol,
        Signature,
        TypedStructure,
    )
except ImportError:
    from .codec import RelationalState, encode
    from .signature import (
        ConstantSymbol,
        FunctionSymbol,
        RelationSymbol,
        Signature,
        TypedStructure,
    )


@dataclass(frozen=True)
class Renaming:
    """Signature renaming morphism sigma: Sigma_1 -> Sigma_2."""

    sort_map: tuple[tuple[str, str], ...] = ()
    const_map: tuple[tuple[str, str], ...] = ()
    rel_map: tuple[tuple[str, str], ...] = ()
    func_map: tuple[tuple[str, str], ...] = ()

    @classmethod
    def create(
        cls,
        sort_map: Mapping[str, str] = {},
        const_map: Mapping[str, str] = {},
        rel_map: Mapping[str, str] = {},
        func_map: Mapping[str, str] = {},
    ) -> Renaming:
        return cls(
            sort_map=tuple(sorted(sort_map.items())),
            const_map=tuple(sorted(const_map.items())),
            rel_map=tuple(sorted(rel_map.items())),
            func_map=tuple(sorted(func_map.items())),
        )

    def rename_sort(self, s: str) -> str:
        s_dict = dict(self.sort_map)
        return s_dict.get(s, s)

    def rename_const(self, c: str) -> str:
        c_dict = dict(self.const_map)
        return c_dict.get(c, c)

    def rename_rel(self, r: str) -> str:
        r_dict = dict(self.rel_map)
        return r_dict.get(r, r)

    def rename_func(self, f: str) -> str:
        f_dict = dict(self.func_map)
        return f_dict.get(f, f)

    def compose(self, other: Renaming) -> Renaming:
        """Functorial composition: (self o other)(x) = self(other(x))."""
        other_sorts = dict(other.sort_map)
        self_sorts = dict(self.sort_map)
        all_sort_keys = set(other_sorts.keys()) | set(self_sorts.keys())
        comp_sorts = {k: self.rename_sort(other.rename_sort(k)) for k in all_sort_keys}

        other_consts = dict(other.const_map)
        self_consts = dict(self.const_map)
        all_const_keys = set(other_consts.keys()) | set(self_consts.keys())
        comp_consts = {k: self.rename_const(other.rename_const(k)) for k in all_const_keys}

        other_rels = dict(other.rel_map)
        self_rels = dict(self.rel_map)
        all_rel_keys = set(other_rels.keys()) | set(self_rels.keys())
        comp_rels = {k: self.rename_rel(other.rename_rel(k)) for k in all_rel_keys}

        other_funcs = dict(other.func_map)
        self_funcs = dict(self.func_map)
        all_func_keys = set(other_funcs.keys()) | set(self_funcs.keys())
        comp_funcs = {k: self.rename_func(other.rename_func(k)) for k in all_func_keys}

        return Renaming.create(
            sort_map=comp_sorts,
            const_map=comp_consts,
            rel_map=comp_rels,
            func_map=comp_funcs,
        )

    def apply_to_signature(self, sig: Signature) -> Signature:
        """Push-forward of signature along renaming."""
        new_sorts = tuple(sorted({self.rename_sort(s) for s in sig.sorts}))
        new_consts = tuple(
            sorted(
                (ConstantSymbol(self.rename_const(c.name), self.rename_sort(c.sort)) for c in sig.constants),
                key=lambda x: x.name,
            )
        )
        new_rels = tuple(
            sorted(
                (RelationSymbol(self.rename_rel(r.name), tuple(self.rename_sort(s) for s in r.arity)) for r in sig.relations),
                key=lambda x: x.name,
            )
        )
        new_funcs = tuple(
            sorted(
                (
                    FunctionSymbol(
                        self.rename_func(f.name),
                        tuple(self.rename_sort(s) for s in f.arity),
                        self.rename_sort(f.target_sort),
                    )
                    for f in sig.functions
                ),
                key=lambda x: x.name,
            )
        )
        return Signature(
            sorts=new_sorts,
            constants=new_consts,
            relations=new_rels,
            functions=new_funcs,
        )

    def apply_to_structure(self, struct: TypedStructure) -> TypedStructure:
        """Functorial push-forward of typed structure sigma_*(S)."""
        new_sig = self.apply_to_signature(struct.signature)

        new_carriers = {
            self.rename_sort(s): set(elems)
            for s, elems in struct.carriers
        }

        new_constants = {
            self.rename_const(c): val
            for c, val in struct.constants
        }

        new_relations = {
            self.rename_rel(r): set(tups)
            for r, tups in struct.relations
        }

        new_functions = {
            self.rename_func(f): dict(entries)
            for f, entries in struct.functions
        }

        return TypedStructure.create(
            signature=new_sig,
            carriers=new_carriers,
            constants=new_constants,
            relations=new_relations,
            functions=new_functions,
        )

    def apply_to_relational_state(self, state: RelationalState) -> RelationalState:
        """Action of renaming on relational carrier sigma_rel(R)."""
        new_data: list[str] = []
        for d in state.data:
            m = re.fullmatch(r"elem:([^:]+):(.*)", d)
            if m:
                s, elem = m.group(1), m.group(2)
                new_data.append(f"elem:{self.rename_sort(s)}:{elem}")
            else:
                new_data.append(d)

        new_forms: list[str] = []
        for f in state.forms:
            if f.startswith("sort:"):
                s = f[len("sort:"):]
                new_forms.append(f"sort:{self.rename_sort(s)}")
            elif f.startswith("const:"):
                parts = f.split(":")
                new_forms.append(f"const:{self.rename_const(parts[1])}:{self.rename_sort(parts[2])}")
            elif f.startswith("rel:"):
                parts = f.split(":")
                ar = [self.rename_sort(s) for s in parts[2].split(",") if s] if parts[2] else []
                new_forms.append(f"rel:{self.rename_rel(parts[1])}:{','.join(ar)}")
            elif f.startswith("func:"):
                m = re.fullmatch(r"func:([^:]+):(.*?)->(.*)", f)
                if m:
                    f_name, ar_str, tgt = m.group(1), m.group(2), m.group(3)
                    ar = [self.rename_sort(s) for s in ar_str.split(",") if s] if ar_str else []
                    new_forms.append(f"func:{self.rename_func(f_name)}:{','.join(ar)}->{self.rename_sort(tgt)}")
                else:
                    new_forms.append(f)
            else:
                new_forms.append(f)

        new_insts: list[str] = []
        for inst in state.insts:
            if inst.startswith("bind:"):
                parts = inst.split(":")
                new_insts.append(f"bind:{self.rename_const(parts[1])}:{parts[2]}")
            elif inst.startswith("tup:"):
                m = re.fullmatch(r"tup:([^:]+):\((.*?)\)", inst)
                if m:
                    r_name, args = m.group(1), m.group(2)
                    new_insts.append(f"tup:{self.rename_rel(r_name)}:({args})")
                else:
                    new_insts.append(inst)
            else:
                new_insts.append(inst)

        new_rules: list[str] = []
        for rule in state.rules:
            if rule.startswith("rule:det:"):
                f_name = rule[len("rule:det:"):]
                new_rules.append(f"rule:det:{self.rename_func(f_name)}")
            elif rule.startswith("rule:rel:"):
                m = re.fullmatch(r"rule:rel:([^:]+):\((.*?)\)", rule)
                if m:
                    r_name, args = m.group(1), m.group(2)
                    new_rules.append(f"rule:rel:{self.rename_rel(r_name)}:({args})")
                else:
                    new_rules.append(rule)
            elif rule.startswith("rule:func:"):
                m = re.fullmatch(r"rule:func:([^:]+):\((.*?)\)->(.*)", rule)
                if m:
                    f_name, args, val = m.group(1), m.group(2), m.group(3)
                    new_rules.append(f"rule:func:{self.rename_func(f_name)}:({args})->{val}")
                else:
                    new_rules.append(rule)
            else:
                new_rules.append(rule)

        new_reqs: list[str] = []
        for req in state.reqs:
            if req.startswith("req:elem:"):
                parts = req.split(":")
                new_reqs.append(f"req:elem:{self.rename_sort(parts[2])}:{parts[3]}")
            elif req.startswith("req:const:"):
                parts = req.split(":")
                new_reqs.append(f"req:const:{self.rename_const(parts[2])}:{self.rename_sort(parts[3])}:{parts[4]}")
            elif req.startswith("req:arg:"):
                parts = req.split(":")
                new_reqs.append(f"req:arg:{self.rename_rel(parts[2])}:{self.rename_sort(parts[3])}:{parts[4]}")
            elif req.startswith("req:func_in:"):
                parts = req.split(":")
                new_reqs.append(f"req:func_in:{self.rename_func(parts[2])}:{self.rename_sort(parts[3])}:{parts[4]}")
            elif req.startswith("req:func_out:"):
                parts = req.split(":")
                new_reqs.append(f"req:func_out:{self.rename_func(parts[2])}:{self.rename_sort(parts[3])}:{parts[4]}")
            else:
                new_reqs.append(req)

        return RelationalState(
            data=tuple(sorted(set(new_data))),
            forms=tuple(sorted(set(new_forms))),
            insts=tuple(sorted(set(new_insts))),
            rules=tuple(sorted(set(new_rules))),
            reqs=tuple(sorted(set(new_reqs))),
        )


def renaming_naturality_commutes(sigma: Renaming, struct: TypedStructure) -> bool:
    """Check naturality commutation: encode(sigma_*(S)) == sigma_rel(encode(S))."""
    renamed_struct = sigma.apply_to_structure(struct)
    encoded_renamed = encode(renamed_struct)

    orig_encoded = encode(struct)
    renamed_encoded = sigma.apply_to_relational_state(orig_encoded)

    return encoded_renamed == renamed_encoded


@dataclass(frozen=True)
class DistortionVector:
    """Exact rational distortion vector measuring boundary translation cost in Q."""

    state_expansion: Fraction
    mark_count_ratio: Fraction
    address_depth_ratio: Fraction

    def as_tuple(self) -> tuple[Fraction, Fraction, Fraction]:
        return (self.state_expansion, self.mark_count_ratio, self.address_depth_ratio)


def compute_distortion(struct: TypedStructure) -> DistortionVector:
    """Compute the exact rational distortion vector for a TypedStructure encoding."""
    state = encode(struct)

    # 1. State expansion ratio: total relational tokens / source atomic items
    total_rel_tokens = (
        len(state.data)
        + len(state.forms)
        + len(state.insts)
        + len(state.rules)
        + len(state.reqs)
    )

    source_carrier_elems = sum(len(elems) for _, elems in struct.carriers)
    source_constants = len(struct.constants)
    source_tuples = sum(len(tups) for _, tups in struct.relations)
    source_func_entries = sum(len(entries) for _, entries in struct.functions)
    source_sig_items = (
        len(struct.signature.sorts)
        + len(struct.signature.constants)
        + len(struct.signature.relations)
        + len(struct.signature.functions)
    )
    source_atoms = max(
        1,
        source_carrier_elems
        + source_constants
        + source_tuples
        + source_func_entries
        + source_sig_items,
    )

    state_expansion = Fraction(total_rel_tokens, source_atoms)

    # 2. Mark count ratio: (insts + rules) / (tuples + constants + function entries)
    rel_marks = len(state.insts) + len(state.rules)
    source_marks = max(1, source_tuples + source_constants + source_func_entries)
    mark_count_ratio = Fraction(rel_marks, source_marks)

    # 3. Address depth ratio: relational address nesting depth (3 levels) vs signature arity depth
    # Relational paths: category : symbol : arguments (depth 3)
    max_arity = max(
        [len(r.arity) for r in struct.signature.relations]
        + [len(f.arity) + 1 for f in struct.signature.functions]
        + [1]
    )
    # Structure arity depth = max_arity + 1
    struct_depth = max_arity + 1
    rel_depth = 3
    address_depth_ratio = Fraction(rel_depth, struct_depth)

    return DistortionVector(
        state_expansion=state_expansion,
        mark_count_ratio=mark_count_ratio,
        address_depth_ratio=address_depth_ratio,
    )
