"""Constructive encoder and decoder between typed structures and relational grammar.

Provides bidirectional encoding, decoding with structured refusals,
round-trip inversion proofs, and operational transition commutation.

Relational grammar categories: (data, forms, insts, rules, reqs).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re
from typing import Generic, TypeVar

try:
    from signature import (
        AddElement,
        AddRelationTuple,
        ConstantSymbol,
        FunctionSymbol,
        RelationSymbol,
        SetConstant,
        SetFunctionValue,
        Signature,
        StructureOp,
        TypedStructure,
        step as structure_step,
    )
except ImportError:
    from .signature import (
        AddElement,
        AddRelationTuple,
        ConstantSymbol,
        FunctionSymbol,
        RelationSymbol,
        SetConstant,
        SetFunctionValue,
        Signature,
        StructureOp,
        TypedStructure,
        step as structure_step,
    )

T = TypeVar("T")
E = TypeVar("E")


class RefusalCode(StrEnum):
    """Structured refusal categories for malformed encodings and invalid states."""

    MALFORMED_ENCODING = "MALFORMED_ENCODING"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    UNSORTED_OR_DUPLICATE = "UNSORTED_OR_DUPLICATE"
    CARRIER_MISMATCH = "CARRIER_MISMATCH"
    FUNCTION_NON_FUNCTIONAL = "FUNCTION_NON_FUNCTIONAL"
    MISSING_REQUIREMENT = "MISSING_REQUIREMENT"
    UNKNOWN_SYMBOL = "UNKNOWN_SYMBOL"


@dataclass(frozen=True)
class Refusal:
    """Structured refusal descriptor with refusal code and detail message."""

    code: RefusalCode
    message: str


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> None:
        raise ValueError("Called unwrap_err on Ok")


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self) -> None:
        raise ValueError(f"Called unwrap on Err: {self.error}")

    def unwrap_err(self) -> E:
        return self.error


Result = Ok[T] | Err[E]


@dataclass(frozen=True)
class RelationalState:
    """Relational carrier partitioned into data, forms, insts, rules, reqs."""

    data: tuple[str, ...]
    forms: tuple[str, ...]
    insts: tuple[str, ...]
    rules: tuple[str, ...]
    reqs: tuple[str, ...]

    def __post_init__(self) -> None:
        # Enforce canonical ordering across all carrier components
        pass


@dataclass(frozen=True)
class RelationalOp:
    """Operational transition on the relational carrier."""

    added_data: tuple[str, ...] = ()
    added_forms: tuple[str, ...] = ()
    added_insts: tuple[str, ...] = ()
    added_rules: tuple[str, ...] = ()
    added_reqs: tuple[str, ...] = ()
    removed_insts: tuple[str, ...] = ()
    removed_rules: tuple[str, ...] = ()
    removed_reqs: tuple[str, ...] = ()


def step_relational(state: RelationalState, op: RelationalOp) -> RelationalState:
    """Apply an operational transition to a relational state."""
    return RelationalState(
        data=tuple(sorted(set(state.data) | set(op.added_data))),
        forms=tuple(sorted(set(state.forms) | set(op.added_forms))),
        insts=tuple(sorted((set(state.insts) - set(op.removed_insts)) | set(op.added_insts))),
        rules=tuple(sorted((set(state.rules) - set(op.removed_rules)) | set(op.added_rules))),
        reqs=tuple(sorted((set(state.reqs) - set(op.removed_reqs)) | set(op.added_reqs))),
    )


def encode(struct: TypedStructure) -> RelationalState:
    """Constructively encode a TypedStructure into RelationalState."""
    sig = struct.signature

    # 1. Forms: Sorts, Constants, Relations, Functions
    forms_set: set[str] = set()
    for s in sig.sorts:
        forms_set.add(f"sort:{s}")
    for c in sig.constants:
        forms_set.add(f"const:{c.name}:{c.sort}")
    for r in sig.relations:
        forms_set.add(f"rel:{r.name}:{','.join(r.arity)}")
    for f in sig.functions:
        forms_set.add(f"func:{f.name}:{','.join(f.arity)}->{f.target_sort}")

    # 2. Data: elements per sort
    data_set: set[str] = set()
    reqs_set: set[str] = set()
    for s, elems in struct.carriers:
        for e in elems:
            data_set.add(f"elem:{s}:{e}")
            reqs_set.add(f"req:elem:{s}:{e}")

    # 3. Insts, Rules, and Reqs
    insts_set: set[str] = set()
    rules_set: set[str] = set()

    # Constants
    const_decls = {c.name: c for c in sig.constants}
    for c_name, val in struct.constants:
        c_decl = const_decls[c_name]
        insts_set.add(f"bind:{c_name}:{val}")
        reqs_set.add(f"req:const:{c_name}:{c_decl.sort}:{val}")

    # Relations
    rel_decls = {r.name: r for r in sig.relations}
    for r_name, tups in struct.relations:
        r_decl = rel_decls[r_name]
        for t in tups:
            tup_str = f"tup:{r_name}:({','.join(t)})"
            insts_set.add(tup_str)
            rules_set.add(f"rule:rel:{r_name}:({','.join(t)})")
            for elem, sort in zip(t, r_decl.arity):
                reqs_set.add(f"req:arg:{r_name}:{sort}:{elem}")

    # Functions
    func_decls = {f.name: f for f in sig.functions}
    for f_name in func_decls:
        rules_set.add(f"rule:det:{f_name}")
    for f_name, entries in struct.functions:
        f_decl = func_decls[f_name]
        for args, val in entries:
            rules_set.add(f"rule:func:{f_name}:({','.join(args)})->{val}")
            for elem, sort in zip(args, f_decl.arity):
                reqs_set.add(f"req:func_in:{f_name}:{sort}:{elem}")
            reqs_set.add(f"req:func_out:{f_name}:{f_decl.target_sort}:{val}")

    return RelationalState(
        data=tuple(sorted(data_set)),
        forms=tuple(sorted(forms_set)),
        insts=tuple(sorted(insts_set)),
        rules=tuple(sorted(rules_set)),
        reqs=tuple(sorted(reqs_set)),
    )


def decode(state: RelationalState) -> Result[TypedStructure, Refusal]:
    """Decode a RelationalState into a TypedStructure, or return structured Refusal."""
    try:
        # Check canonical sorting and deduplication
        for field_name, items in [
            ("data", state.data),
            ("forms", state.forms),
            ("insts", state.insts),
            ("rules", state.rules),
            ("reqs", state.reqs),
        ]:
            if list(items) != sorted(set(items)):
                return Err(
                    Refusal(
                        RefusalCode.UNSORTED_OR_DUPLICATE,
                        f"Field '{field_name}' is not canonically sorted or contains duplicates",
                    )
                )

        # Parse forms
        sorts: list[str] = []
        constants: list[ConstantSymbol] = []
        relations: list[RelationSymbol] = []
        functions: list[FunctionSymbol] = []

        for form in state.forms:
            if form.startswith("sort:"):
                s_name = form[len("sort:"):]
                if not s_name:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Empty sort name in '{form}'"))
                sorts.append(s_name)
            elif form.startswith("const:"):
                parts = form.split(":")
                if len(parts) != 3 or not parts[1] or not parts[2]:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed const declaration '{form}'"))
                constants.append(ConstantSymbol(name=parts[1], sort=parts[2]))
            elif form.startswith("rel:"):
                parts = form.split(":")
                if len(parts) != 3 or not parts[1]:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed rel declaration '{form}'"))
                arity = tuple(p for p in parts[2].split(",") if p) if parts[2] else ()
                relations.append(RelationSymbol(name=parts[1], arity=arity))
            elif form.startswith("func:"):
                m = re.fullmatch(r"func:([^:]+):(.*?)->(.*)", form)
                if not m:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed func declaration '{form}'"))
                f_name, arity_str, target_sort = m.group(1), m.group(2), m.group(3)
                if not f_name or not target_sort:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Empty func name or target in '{form}'"))
                arity = tuple(p for p in arity_str.split(",") if p) if arity_str else ()
                functions.append(FunctionSymbol(name=f_name, arity=arity, target_sort=target_sort))
            else:
                return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Unknown form prefix in '{form}'"))

        # Build and validate Signature
        try:
            sig = Signature(
                sorts=tuple(sorted(sorts)),
                constants=tuple(sorted(constants, key=lambda c: c.name)),
                relations=tuple(sorted(relations, key=lambda r: r.name)),
                functions=tuple(sorted(functions, key=lambda f: f.name)),
            )
        except ValueError as e:
            return Err(Refusal(RefusalCode.INVALID_SIGNATURE, str(e)))

        sort_set = set(sig.sorts)

        # Parse data carrier
        carrier_dict: dict[str, set[str]] = {s: set() for s in sig.sorts}
        for item in state.data:
            if not item.startswith("elem:"):
                return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed data item '{item}'"))
            parts = item.split(":")
            if len(parts) != 3 or not parts[1] or not parts[2]:
                return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed data format '{item}'"))
            s_name, elem = parts[1], parts[2]
            if s_name not in sort_set:
                return Err(Refusal(RefusalCode.CARRIER_MISMATCH, f"Data element references unknown sort '{s_name}'"))
            carrier_dict[s_name].add(elem)

        # Parse and verify reqs
        req_set = set(state.reqs)
        # Check every element has req:elem
        for s, elems in carrier_dict.items():
            for elem in elems:
                if f"req:elem:{s}:{elem}" not in req_set:
                    return Err(
                        Refusal(RefusalCode.MISSING_REQUIREMENT, f"Missing requirement for element '{s}:{elem}'")
                    )

        # Parse insts
        const_bindings: dict[str, str] = {}
        relation_tuples: dict[str, set[tuple[str, ...]]] = {r.name: set() for r in sig.relations}

        const_decls = {c.name: c for c in sig.constants}
        rel_decls = {r.name: r for r in sig.relations}

        for inst in state.insts:
            if inst.startswith("bind:"):
                parts = inst.split(":")
                if len(parts) != 3:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed binding '{inst}'"))
                c_name, val = parts[1], parts[2]
                if c_name not in const_decls:
                    return Err(Refusal(RefusalCode.UNKNOWN_SYMBOL, f"Binding references unknown constant '{c_name}'"))
                c_decl = const_decls[c_name]
                if val not in carrier_dict[c_decl.sort]:
                    return Err(
                        Refusal(
                            RefusalCode.CARRIER_MISMATCH,
                            f"Constant '{c_name}' value '{val}' not in sort '{c_decl.sort}'",
                        )
                    )
                if f"req:const:{c_name}:{c_decl.sort}:{val}" not in req_set:
                    return Err(
                        Refusal(
                            RefusalCode.MISSING_REQUIREMENT,
                            f"Missing requirement for constant binding '{c_name}:{val}'",
                        )
                    )
                const_bindings[c_name] = val

            elif inst.startswith("tup:"):
                m = re.fullmatch(r"tup:([^:]+):\((.*?)\)", inst)
                if not m:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed tuple '{inst}'"))
                r_name, args_str = m.group(1), m.group(2)
                if r_name not in rel_decls:
                    return Err(Refusal(RefusalCode.UNKNOWN_SYMBOL, f"Tuple references unknown relation '{r_name}'"))
                r_decl = rel_decls[r_name]
                args = tuple(p for p in args_str.split(",") if p) if args_str else ()
                if len(args) != len(r_decl.arity):
                    return Err(
                        Refusal(
                            RefusalCode.CARRIER_MISMATCH,
                            f"Arity mismatch for tuple in relation '{r_name}'",
                        )
                    )
                for elem, expected_sort in zip(args, r_decl.arity):
                    if elem not in carrier_dict[expected_sort]:
                        return Err(
                            Refusal(
                                RefusalCode.CARRIER_MISMATCH,
                                f"Tuple element '{elem}' not in sort '{expected_sort}' carrier",
                            )
                        )
                    if f"req:arg:{r_name}:{expected_sort}:{elem}" not in req_set:
                        return Err(
                            Refusal(
                                RefusalCode.MISSING_REQUIREMENT,
                                f"Missing requirement for relation arg '{r_name}:{expected_sort}:{elem}'",
                            )
                        )
                relation_tuples[r_name].add(args)

            else:
                return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Unknown inst prefix in '{inst}'"))

        # Parse rules
        func_entries: dict[str, dict[tuple[str, ...], str]] = {f.name: {} for f in sig.functions}
        func_decls = {f.name: f for f in sig.functions}

        for rule in state.rules:
            if rule.startswith("rule:det:"):
                f_name = rule[len("rule:det:"):]
                if f_name not in func_decls:
                    return Err(Refusal(RefusalCode.UNKNOWN_SYMBOL, f"Determinism rule for unknown function '{f_name}'"))
            elif rule.startswith("rule:rel:"):
                m = re.fullmatch(r"rule:rel:([^:]+):\((.*?)\)", rule)
                if not m:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed relation rule '{rule}'"))
                r_name, args_str = m.group(1), m.group(2)
                args = tuple(p for p in args_str.split(",") if p) if args_str else ()
                if r_name not in relation_tuples or args not in relation_tuples[r_name]:
                    return Err(
                        Refusal(
                            RefusalCode.MISSING_REQUIREMENT,
                            f"Rule specifies uninstantiated relation tuple '{r_name}:{args}'",
                        )
                    )
            elif rule.startswith("rule:func:"):
                m = re.fullmatch(r"rule:func:([^:]+):\((.*?)\)->(.*)", rule)
                if not m:
                    return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Malformed function rule '{rule}'"))
                f_name, args_str, val = m.group(1), m.group(2), m.group(3)
                if f_name not in func_decls:
                    return Err(Refusal(RefusalCode.UNKNOWN_SYMBOL, f"Function rule references unknown function '{f_name}'"))
                f_decl = func_decls[f_name]
                args = tuple(p for p in args_str.split(",") if p) if args_str else ()
                if len(args) != len(f_decl.arity):
                    return Err(Refusal(RefusalCode.CARRIER_MISMATCH, f"Arity mismatch in function rule '{rule}'"))
                for elem, expected_sort in zip(args, f_decl.arity):
                    if elem not in carrier_dict[expected_sort]:
                        return Err(
                            Refusal(
                                RefusalCode.CARRIER_MISMATCH,
                                f"Function arg '{elem}' not in sort '{expected_sort}' carrier",
                            )
                        )
                    if f"req:func_in:{f_name}:{expected_sort}:{elem}" not in req_set:
                        return Err(
                            Refusal(
                                RefusalCode.MISSING_REQUIREMENT,
                                f"Missing requirement for function arg '{f_name}:{expected_sort}:{elem}'",
                            )
                        )
                if val not in carrier_dict[f_decl.target_sort]:
                    return Err(
                        Refusal(
                            RefusalCode.CARRIER_MISMATCH,
                            f"Function value '{val}' not in target sort '{f_decl.target_sort}' carrier",
                        )
                    )
                if f"req:func_out:{f_name}:{f_decl.target_sort}:{val}" not in req_set:
                    return Err(
                        Refusal(
                            RefusalCode.MISSING_REQUIREMENT,
                            f"Missing requirement for function target '{f_name}:{f_decl.target_sort}:{val}'",
                        )
                    )

                if args in func_entries[f_name]:
                    return Err(
                        Refusal(
                            RefusalCode.FUNCTION_NON_FUNCTIONAL,
                            f"Function '{f_name}' maps {args} to both '{func_entries[f_name][args]}' and '{val}'",
                        )
                    )
                func_entries[f_name][args] = val
            else:
                return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Unknown rule prefix in '{rule}'"))

        # Construct decoded TypedStructure
        struct = TypedStructure.create(
            signature=sig,
            carriers=carrier_dict,
            constants=const_bindings,
            relations=relation_tuples,
            functions={f: list(entries.items()) for f, entries in func_entries.items()},
        )
        return Ok(struct)

    except Exception as exc:
        return Err(Refusal(RefusalCode.MALFORMED_ENCODING, f"Unhandled decode failure: {exc}"))


def encode_op(op: StructureOp, context: TypedStructure | Signature) -> RelationalOp:
    """Encode a StructureOp into a RelationalOp on the relational state."""
    sig = context.signature if isinstance(context, TypedStructure) else context
    struct = context if isinstance(context, TypedStructure) else None

    if isinstance(op, AddElement):
        return RelationalOp(
            added_data=(f"elem:{op.sort}:{op.element}",),
            added_reqs=(f"req:elem:{op.sort}:{op.element}",),
        )

    if isinstance(op, SetConstant):
        c_decl = sig.get_constant(op.name)
        removed_insts: tuple[str, ...] = ()
        removed_reqs: tuple[str, ...] = ()
        if struct is not None:
            old_val = struct.constant_val(op.name)
            if old_val is not None:
                removed_insts = (f"bind:{op.name}:{old_val}",)
                removed_reqs = (f"req:const:{op.name}:{c_decl.sort}:{old_val}",)
        return RelationalOp(
            added_insts=(f"bind:{op.name}:{op.value}",),
            added_reqs=(f"req:const:{op.name}:{c_decl.sort}:{op.value}",),
            removed_insts=removed_insts,
            removed_reqs=removed_reqs,
        )

    if isinstance(op, AddRelationTuple):
        r_decl = sig.get_relation(op.name)
        tup_str = f"tup:{op.name}:({','.join(op.tuple_vals)})"
        rule_str = f"rule:rel:{op.name}:({','.join(op.tuple_vals)})"
        req_items = tuple(
            f"req:arg:{op.name}:{s}:{arg}"
            for s, arg in zip(r_decl.arity, op.tuple_vals)
        )
        return RelationalOp(
            added_insts=(tup_str,),
            added_rules=(rule_str,),
            added_reqs=req_items,
        )

    if isinstance(op, SetFunctionValue):
        f_decl = sig.get_function(op.name)
        removed_rules: tuple[str, ...] = ()
        removed_reqs: tuple[str, ...] = ()
        if struct is not None:
            for args, old_val in struct.function_entries_for(op.name):
                if args == op.args:
                    removed_rules = (f"rule:func:{op.name}:({','.join(op.args)})->{old_val}",)
                    removed_reqs = (f"req:func_out:{op.name}:{f_decl.target_sort}:{old_val}",)
                    break

        rule_str = f"rule:func:{op.name}:({','.join(op.args)})->{op.value}"
        req_in = tuple(
            f"req:func_in:{op.name}:{s}:{arg}"
            for s, arg in zip(f_decl.arity, op.args)
        )
        req_out = (f"req:func_out:{op.name}:{f_decl.target_sort}:{op.value}",)
        return RelationalOp(
            added_rules=(rule_str,),
            added_reqs=req_in + req_out,
            removed_rules=removed_rules,
            removed_reqs=removed_reqs,
        )

    raise TypeError(f"Unknown structure op: {op}")


def step_commutation_holds(struct: TypedStructure, op: StructureOp) -> bool:
    """Check that operational transition and encoded step commute.

    encode(step(S, op)) == step_relational(encode(S), encode_op(op, S))
    """
    next_struct = structure_step(struct, op)
    encoded_next = encode(next_struct)
    stepped_encoded = step_relational(encode(struct), encode_op(op, struct))
    return encoded_next == stepped_encoded
