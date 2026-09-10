"""Typed finite structure signatures and structures.

Defines multi-sorted relational signatures with constants, relations, and
functions, alongside canonical typed structures, validation checks,
and operational transition steps.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class ConstantSymbol:
    """A constant symbol declared with its sort."""

    name: str
    sort: str


@dataclass(frozen=True)
class RelationSymbol:
    """A relation symbol declared with an arity tuple of sorts."""

    name: str
    arity: tuple[str, ...]


@dataclass(frozen=True)
class FunctionSymbol:
    """A function symbol declared with argument sorts and target sort."""

    name: str
    arity: tuple[str, ...]
    target_sort: str


@dataclass(frozen=True)
class Signature:
    """Multi-sorted signature with constants, relations, and functions."""

    sorts: tuple[str, ...]
    constants: tuple[ConstantSymbol, ...] = ()
    relations: tuple[RelationSymbol, ...] = ()
    functions: tuple[FunctionSymbol, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "sorts", tuple(sorted(self.sorts)))
        object.__setattr__(self, "constants", tuple(sorted(self.constants, key=lambda c: c.name)))
        object.__setattr__(self, "relations", tuple(sorted(self.relations, key=lambda r: r.name)))
        object.__setattr__(self, "functions", tuple(sorted(self.functions, key=lambda f: f.name)))
        self.validate()

    def validate(self) -> None:
        """Validate signature sanity: no duplicate symbols, all sorts defined."""
        # Sorts unique
        if len(self.sorts) != len(set(self.sorts)):
            raise ValueError(f"Duplicate sorts in signature: {self.sorts}")
        sort_set = set(self.sorts)

        # Constants unique and sorts valid
        const_names = [c.name for c in self.constants]
        if len(const_names) != len(set(const_names)):
            raise ValueError(f"Duplicate constants in signature: {const_names}")
        for c in self.constants:
            if c.sort not in sort_set:
                raise ValueError(f"Constant '{c.name}' references unknown sort '{c.sort}'")

        # Relations unique and arities valid
        rel_names = [r.name for r in self.relations]
        if len(rel_names) != len(set(rel_names)):
            raise ValueError(f"Duplicate relations in signature: {rel_names}")
        for r in self.relations:
            for s in r.arity:
                if s not in sort_set:
                    raise ValueError(f"Relation '{r.name}' references unknown sort '{s}'")

        # Functions unique and sorts valid
        func_names = [f.name for f in self.functions]
        if len(func_names) != len(set(func_names)):
            raise ValueError(f"Duplicate functions in signature: {func_names}")
        for f in self.functions:
            for s in f.arity:
                if s not in sort_set:
                    raise ValueError(f"Function '{f.name}' references unknown argument sort '{s}'")
            if f.target_sort not in sort_set:
                raise ValueError(f"Function '{f.name}' references unknown target sort '{f.target_sort}'")

    def get_sort(self, name: str) -> str:
        if name not in self.sorts:
            raise KeyError(f"Sort '{name}' not found")
        return name

    def get_constant(self, name: str) -> ConstantSymbol:
        for c in self.constants:
            if c.name == name:
                return c
        raise KeyError(f"Constant '{name}' not found")

    def get_relation(self, name: str) -> RelationSymbol:
        for r in self.relations:
            if r.name == name:
                return r
        raise KeyError(f"Relation '{name}' not found")

    def get_function(self, name: str) -> FunctionSymbol:
        for f in self.functions:
            if f.name == name:
                return f
        raise KeyError(f"Function '{name}' not found")


@dataclass(frozen=True)
class TypedStructure:
    """Canonical finite typed structure over a signature.

    Carriers, constants, relations, and functions are represented as canonically
    sorted nested tuples for deterministic structural equality.
    """

    signature: Signature
    # (sort_name, (elem, ...))
    carriers: tuple[tuple[str, tuple[str, ...]], ...]
    # (const_name, elem)
    constants: tuple[tuple[str, str], ...] = ()
    # (rel_name, ((arg0, arg1, ...), ...))
    relations: tuple[tuple[str, tuple[tuple[str, ...], ...]], ...] = ()
    # (func_name, (((arg0, ...), val), ...))
    functions: tuple[tuple[str, tuple[tuple[tuple[str, ...], str], ...]], ...] = ()

    @classmethod
    def create(
        cls,
        signature: Signature,
        carriers: Mapping[str, Sequence[str]] | Sequence[tuple[str, Sequence[str]]],
        constants: Mapping[str, str] | Sequence[tuple[str, str]] = (),
        relations: Mapping[str, Sequence[Sequence[str]]] | Sequence[tuple[str, Sequence[Sequence[str]]]] = (),
        functions: Mapping[str, Sequence[tuple[Sequence[str], str]]] | Sequence[tuple[str, Sequence[tuple[Sequence[str], str]]]] = (),
    ) -> TypedStructure:
        """Construct a canonical TypedStructure with canonical sorting."""
        c_dict: dict[str, set[str]] = {s: set() for s in signature.sorts}
        if isinstance(carriers, Mapping):
            for s, elems in carriers.items():
                if s not in c_dict:
                    raise ValueError(f"Unknown sort in carriers: {s}")
                c_dict[s].update(elems)
        else:
            for s, elems in carriers:
                if s not in c_dict:
                    raise ValueError(f"Unknown sort in carriers: {s}")
                c_dict[s].update(elems)

        canonical_carriers = tuple(
            (s, tuple(sorted(c_dict[s])))
            for s in signature.sorts
        )

        # Constants
        k_dict: dict[str, str] = {}
        if isinstance(constants, Mapping):
            k_dict.update(constants)
        else:
            for k, val in constants:
                k_dict[k] = val
        canonical_constants = tuple(
            (c.name, k_dict[c.name])
            for c in signature.constants
            if c.name in k_dict
        )

        # Relations
        r_dict: dict[str, set[tuple[str, ...]]] = {r.name: set() for r in signature.relations}
        if isinstance(relations, Mapping):
            for r, tups in relations.items():
                if r not in r_dict:
                    raise ValueError(f"Unknown relation: {r}")
                for t in tups:
                    r_dict[r].add(tuple(t))
        else:
            for r, tups in relations:
                if r not in r_dict:
                    raise ValueError(f"Unknown relation: {r}")
                for t in tups:
                    r_dict[r].add(tuple(t))
        canonical_relations = tuple(
            (r.name, tuple(sorted(r_dict[r.name])))
            for r in signature.relations
        )

        # Functions
        f_dict: dict[str, dict[tuple[str, ...], str]] = {f.name: {} for f in signature.functions}
        if isinstance(functions, Mapping):
            for f, entries in functions.items():
                if f not in f_dict:
                    raise ValueError(f"Unknown function: {f}")
                if isinstance(entries, Mapping):
                    for args, val in entries.items():
                        f_dict[f][tuple(args)] = val
                else:
                    for args, val in entries:
                        f_dict[f][tuple(args)] = val
        else:
            for f, entries in functions:
                if f not in f_dict:
                    raise ValueError(f"Unknown function: {f}")
                if isinstance(entries, Mapping):
                    for args, val in entries.items():
                        f_dict[f][tuple(args)] = val
                else:
                    for args, val in entries:
                        f_dict[f][tuple(args)] = val
        canonical_functions = tuple(
            (f.name, tuple(sorted(((args, val) for args, val in f_dict[f.name].items()), key=lambda x: x[0])))
            for f in signature.functions
        )

        struct = cls(
            signature=signature,
            carriers=canonical_carriers,
            constants=canonical_constants,
            relations=canonical_relations,
            functions=canonical_functions,
        )
        struct.validate()
        return struct

    def validate(self) -> None:
        """Validate structure conformance with signature and typing."""
        self.signature.validate()

        carrier_map = {s: set(elems) for s, elems in self.carriers}
        for s in self.signature.sorts:
            if s not in carrier_map:
                raise ValueError(f"Missing carrier for sort '{s}'")

        # Validate constants
        const_map = dict(self.constants)
        for c in self.signature.constants:
            if c.name in const_map:
                val = const_map[c.name]
                if val not in carrier_map[c.sort]:
                    raise ValueError(
                        f"Constant '{c.name}' value '{val}' not in sort '{c.sort}' carrier"
                    )

        # Validate relations
        for r_name, tups in self.relations:
            rel = self.signature.get_relation(r_name)
            for tup in tups:
                if len(tup) != len(rel.arity):
                    raise ValueError(
                        f"Tuple {tup} arity mismatch for relation '{r_name}', expected {len(rel.arity)}"
                    )
                for idx, (elem, expected_sort) in enumerate(zip(tup, rel.arity)):
                    if elem not in carrier_map[expected_sort]:
                        raise ValueError(
                            f"Tuple {tup} element '{elem}' at index {idx} not in sort '{expected_sort}' carrier"
                        )

        # Validate functions
        for f_name, entries in self.functions:
            func = self.signature.get_function(f_name)
            seen_args: set[tuple[str, ...]] = set()
            for args, val in entries:
                if len(args) != len(func.arity):
                    raise ValueError(
                        f"Function entry {args}->{val} arity mismatch for '{f_name}', expected {len(func.arity)}"
                    )
                for idx, (arg_elem, expected_sort) in enumerate(zip(args, func.arity)):
                    if arg_elem not in carrier_map[expected_sort]:
                        raise ValueError(
                            f"Function entry arg '{arg_elem}' at index {idx} not in sort '{expected_sort}' carrier"
                        )
                if val not in carrier_map[func.target_sort]:
                    raise ValueError(
                        f"Function entry value '{val}' not in target sort '{func.target_sort}' carrier"
                    )
                if args in seen_args:
                    raise ValueError(f"Function '{f_name}' has non-functional duplicate mapping for {args}")
                seen_args.add(args)

    def carrier_for(self, sort: str) -> tuple[str, ...]:
        for s, elems in self.carriers:
            if s == sort:
                return elems
        raise KeyError(f"Sort '{sort}' not found")

    def tuples_for(self, rel: str) -> tuple[tuple[str, ...], ...]:
        for r, tups in self.relations:
            if r == rel:
                return tups
        raise KeyError(f"Relation '{rel}' not found")

    def function_entries_for(self, func: str) -> tuple[tuple[tuple[str, ...], str], ...]:
        for f, entries in self.functions:
            if f == func:
                return entries
        raise KeyError(f"Function '{func}' not found")

    def constant_val(self, const: str) -> str | None:
        for c, val in self.constants:
            if c == const:
                return val
        return None


# Operational transitions
@dataclass(frozen=True)
class StructureOp:
    """Base class for structure transitions."""


@dataclass(frozen=True)
class AddElement(StructureOp):
    sort: str
    element: str


@dataclass(frozen=True)
class SetConstant(StructureOp):
    name: str
    value: str


@dataclass(frozen=True)
class AddRelationTuple(StructureOp):
    name: str
    tuple_vals: tuple[str, ...]


@dataclass(frozen=True)
class SetFunctionValue(StructureOp):
    name: str
    args: tuple[str, ...]
    value: str


def step(struct: TypedStructure, op: StructureOp) -> TypedStructure:
    """Apply an operational transition step to a typed structure."""
    if isinstance(op, AddElement):
        struct.signature.get_sort(op.sort)
        carriers = {s: set(elems) for s, elems in struct.carriers}
        carriers[op.sort].add(op.element)
        return TypedStructure.create(
            signature=struct.signature,
            carriers=carriers,
            constants=struct.constants,
            relations=struct.relations,
            functions=struct.functions,
        )

    if isinstance(op, SetConstant):
        c_decl = struct.signature.get_constant(op.name)
        carrier = struct.carrier_for(c_decl.sort)
        if op.value not in carrier:
            raise ValueError(f"Element '{op.value}' not in carrier for sort '{c_decl.sort}'")
        consts = dict(struct.constants)
        consts[op.name] = op.value
        return TypedStructure.create(
            signature=struct.signature,
            carriers=struct.carriers,
            constants=consts,
            relations=struct.relations,
            functions=struct.functions,
        )

    if isinstance(op, AddRelationTuple):
        r_decl = struct.signature.get_relation(op.name)
        if len(op.tuple_vals) != len(r_decl.arity):
            raise ValueError(f"Arity mismatch for relation '{op.name}': {op.tuple_vals}")
        for elem, s in zip(op.tuple_vals, r_decl.arity):
            if elem not in struct.carrier_for(s):
                raise ValueError(f"Element '{elem}' not in sort '{s}' carrier")
        rels = {r: set(tups) for r, tups in struct.relations}
        rels[op.name].add(op.tuple_vals)
        return TypedStructure.create(
            signature=struct.signature,
            carriers=struct.carriers,
            constants=struct.constants,
            relations=rels,
            functions=struct.functions,
        )

    if isinstance(op, SetFunctionValue):
        f_decl = struct.signature.get_function(op.name)
        if len(op.args) != len(f_decl.arity):
            raise ValueError(f"Arity mismatch for function '{op.name}': {op.args}")
        for elem, s in zip(op.args, f_decl.arity):
            if elem not in struct.carrier_for(s):
                raise ValueError(f"Arg '{elem}' not in sort '{s}' carrier")
        if op.value not in struct.carrier_for(f_decl.target_sort):
            raise ValueError(f"Value '{op.value}' not in sort '{f_decl.target_sort}' carrier")
        funcs = {f: dict(entries) for f, entries in struct.functions}
        funcs[op.name][op.args] = op.value
        return TypedStructure.create(
            signature=struct.signature,
            carriers=struct.carriers,
            constants=struct.constants,
            relations=struct.relations,
            functions=funcs,
        )

    raise TypeError(f"Unknown structure operation: {op}")
