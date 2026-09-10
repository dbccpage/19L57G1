"""Target X300: Observer-Relative Information, Channels & Loss.

This module formalizes:
1. Exact additive operational entropy and information divergence metrics in Q
   over discrete dyadic observation alphabets, as well as exact Hartley capacity metrics.
2. Operational communication channels between distributed observers, Markov compositions,
   encoding/decoding schemes, and transmission fidelity.
3. Data processing inequality (DPI): operational post-processing cannot increase mutual information
   (I(X; Z) <= I(X; Y) for any Markov chain X -> Y -> Z).
4. Memory retention limits, sequential degradation, and lossy coarse-graining projections.
5. Landauer operational erasure cost accounting (Delta H >= 0 and Delta Q >= kB * T * ln(2) * Delta H).

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any, Callable, Generic, Iterable, Mapping, TypeVar

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def _int_log2(n: int) -> int:
    if not _is_power_of_two(n):
        raise ValueError(f"{n} is not a power of two")
    return n.bit_length() - 1


# -----------------------------------------------------------------------------
# 1. Discrete Distribution with Exact Rational Arithmetic
# -----------------------------------------------------------------------------

class DiscreteDistribution(Generic[T]):
    """Discrete probability distribution with exact rational probabilities in Q."""

    def __init__(self, probabilities: Mapping[T, Fraction | int | float | str | tuple[int, int]]) -> None:
        raw: dict[T, Fraction] = {}
        for key, val in probabilities.items():
            if isinstance(val, tuple) and len(val) == 2:
                frac = Fraction(val[0], val[1])
            elif isinstance(val, (int, str)):
                frac = Fraction(val)
            elif isinstance(val, Fraction):
                frac = val
            elif isinstance(val, float):
                frac = Fraction(val).limit_denominator(1_000_000_000)
            else:
                frac = Fraction(val)

            if frac < 0:
                raise ValueError(f"Negative probability for {key}: {frac}")
            if frac > 0:
                raw[key] = frac

        total = sum(raw.values(), Fraction(0))
        if total == 0:
            raise ValueError("Distribution cannot have sum of probabilities equal to 0")
        if total != Fraction(1):
            # Normalize if sum != 1
            raw = {k: v / total for k, v in raw.items()}

        self._probs: dict[T, Fraction] = dict(sorted(raw.items(), key=lambda item: str(item[0])))

    @classmethod
    def uniform(cls, elements: Iterable[T]) -> DiscreteDistribution[T]:
        elems = list(elements)
        if not elems:
            raise ValueError("Cannot create uniform distribution over empty set")
        p = Fraction(1, len(elems))
        return cls({x: p for x in elems})

    @classmethod
    def point_mass(cls, value: T) -> DiscreteDistribution[T]:
        return cls({value: Fraction(1)})

    @classmethod
    def pure_dyadic(cls, lengths: Mapping[T, int]) -> DiscreteDistribution[T]:
        """Create a pure dyadic distribution where P(x) = 2^{-lengths[x]}.

        Must satisfy Kraft-McMillan equality: sum_x 2^{-lengths[x]} == 1.
        """
        probs: dict[T, Fraction] = {}
        total = Fraction(0)
        for item_key, code_len in lengths.items():
            if code_len < 0:
                raise ValueError(f"Negative code length: {code_len}")
            p = Fraction(1, 1 << code_len)
            probs[item_key] = p
            total += p
        if total != Fraction(1):
            raise ValueError(f"Kraft equality failed: sum is {total} != 1")
        return cls(probs)

    def prob(self, item: T) -> Fraction:
        return self._probs.get(item, Fraction(0))

    def support(self) -> tuple[T, ...]:
        return tuple(self._probs.keys())

    def items(self) -> tuple[tuple[T, Fraction], ...]:
        return tuple(self._probs.items())

    def is_dyadic(self) -> bool:
        """Check if all probabilities have denominators that are powers of 2."""
        return all(_is_power_of_two(p.denominator) for p in self._probs.values())

    def is_pure_dyadic(self) -> bool:
        """Check if all probabilities are of the form 2^{-k} (numerator == 1, denom power of 2)."""
        return all(p.numerator == 1 and _is_power_of_two(p.denominator) for p in self._probs.values())

    def pure_dyadic_lengths(self) -> dict[T, int]:
        """Return the integer bit lengths l_x = -log2(P(x)) for pure dyadic distribution."""
        if not self.is_pure_dyadic():
            raise ValueError("Distribution is not pure dyadic")
        return {x: _int_log2(p.denominator) for x, p in self._probs.items()}

    def exact_hartley_capacity(self) -> int | None:
        """Return exact Hartley capacity in bits if |support| is a power of 2, else None."""
        n = len(self._probs)
        if _is_power_of_two(n):
            return _int_log2(n)
        return None

    def hartley_entropy(self) -> float:
        """Hartley capacity metric H0 = log2(|support|)."""
        return math.log2(len(self._probs))

    def exact_dyadic_shannon_entropy(self) -> Fraction:
        """Return exact rational Shannon entropy H in Q for pure dyadic distribution.

        H(P) = sum_x P(x) * (-log2(P(x))) = sum_x l_x * 2^{-l_x} in Q.
        """
        if not self.is_pure_dyadic():
            raise ValueError("Exact rational Shannon entropy requires a pure dyadic distribution")
        h = Fraction(0)
        for p in self._probs.values():
            l_x = _int_log2(p.denominator)
            h += p * l_x
        return h

    def shannon_entropy(self, base: float = 2.0) -> float:
        """Compute general Shannon entropy: - sum p log(p)."""
        ent = 0.0
        for p in self._probs.values():
            if p > 0:
                p_float = float(p)
                ent -= p_float * math.log(p_float, base)
        return max(0.0, ent)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DiscreteDistribution):
            return False
        return self._probs == other._probs

    def __repr__(self) -> str:
        items_str = ", ".join(f"{k}: {v}" for k, v in self._probs.items())
        return f"DiscreteDistribution({{{items_str}}})"


# -----------------------------------------------------------------------------
# 2. Exact Operational Divergence, Cross-Entropy & Joint Measures
# -----------------------------------------------------------------------------

def exact_dyadic_divergence(p: DiscreteDistribution[T], q: DiscreteDistribution[T]) -> Fraction:
    """Exact relative entropy (KL divergence) D(P || Q) in Q for pure dyadic distributions.

    D(P || Q) = sum_{x in supp(P)} P(x) * log2(P(x) / Q(x))
              = sum_{x in supp(P)} 2^{-l_x} * (m_x - l_x) in Q.
    """
    if not p.is_pure_dyadic() or not q.is_pure_dyadic():
        raise ValueError("Both distributions must be pure dyadic for exact rational divergence")

    div = Fraction(0)
    for x, p_val in p.items():
        q_val = q.prob(x)
        if q_val == 0:
            raise ValueError(f"Support of P not contained in support of Q at item: {x}")
        l_x = _int_log2(p_val.denominator)
        m_x = _int_log2(q_val.denominator)
        div += p_val * (m_x - l_x)
    return div


def exact_dyadic_cross_entropy(p: DiscreteDistribution[T], q: DiscreteDistribution[T]) -> Fraction:
    """Exact cross-entropy H(P, Q) in Q for pure dyadic distributions."""
    return p.exact_dyadic_shannon_entropy() + exact_dyadic_divergence(p, q)


def shannon_divergence(p: DiscreteDistribution[T], q: DiscreteDistribution[T], base: float = 2.0) -> float:
    """General Kullback-Leibler divergence D(P || Q)."""
    div = 0.0
    for x, p_val in p.items():
        q_val = q.prob(x)
        if q_val == 0:
            return float("inf")
        pf = float(p_val)
        qf = float(q_val)
        div += pf * math.log(pf / qf, base)
    return max(0.0, div)


def product_distribution(
    p1: DiscreteDistribution[T], p2: DiscreteDistribution[U]
) -> DiscreteDistribution[tuple[T, U]]:
    """Compute product distribution of two independent discrete distributions."""
    joint_probs: dict[tuple[T, U], Fraction] = {}
    for x, px in p1.items():
        for y, py in p2.items():
            joint_probs[(x, y)] = px * py
    return DiscreteDistribution(joint_probs)


def marginal_x(joint: DiscreteDistribution[tuple[T, U]]) -> DiscreteDistribution[T]:
    """Compute marginal distribution P_X from joint distribution P_{X, Y}."""
    m: dict[T, Fraction] = {}
    for (x, _), p in joint.items():
        m[x] = m.get(x, Fraction(0)) + p
    return DiscreteDistribution(m)


def marginal_y(joint: DiscreteDistribution[tuple[T, U]]) -> DiscreteDistribution[U]:
    """Compute marginal distribution P_Y from joint distribution P_{X, Y}."""
    m: dict[U, Fraction] = {}
    for (_, y), p in joint.items():
        m[y] = m.get(y, Fraction(0)) + p
    return DiscreteDistribution(m)


def mutual_information(joint: DiscreteDistribution[tuple[T, U]], base: float = 2.0) -> float:
    """Compute mutual information I(X; Y) = H(X) + H(Y) - H(X, Y)."""
    px = marginal_x(joint)
    py = marginal_y(joint)
    hx = px.shannon_entropy(base=base)
    hy = py.shannon_entropy(base=base)
    hxy = joint.shannon_entropy(base=base)
    mi = hx + hy - hxy
    return max(0.0, mi)


def exact_dyadic_mutual_information(joint: DiscreteDistribution[tuple[T, U]]) -> Fraction:
    """Compute exact rational mutual information I(X; Y) = H(X) + H(Y) - H(X, Y) in Q.

    Requires joint and both marginals to be pure dyadic.
    """
    px = marginal_x(joint)
    py = marginal_y(joint)
    if not (joint.is_pure_dyadic() and px.is_pure_dyadic() and py.is_pure_dyadic()):
        raise ValueError("Exact rational mutual information requires pure dyadic joint and marginals")
    return px.exact_dyadic_shannon_entropy() + py.exact_dyadic_shannon_entropy() - joint.exact_dyadic_shannon_entropy()


# -----------------------------------------------------------------------------
# 3. Operational Communication Channels & Markov Compositions
# -----------------------------------------------------------------------------

class Channel(Generic[T, U]):
    """Operational communication channel W: T -> U represented by transition probabilities W(u | t) in Q."""

    def __init__(
        self,
        transitions: Mapping[T, DiscreteDistribution[U] | Mapping[U, Fraction | int | float | str]],
        input_alphabet: Iterable[T] | None = None,
    ) -> None:
        self._table: dict[T, DiscreteDistribution[U]] = {}
        for x, dist in transitions.items():
            if isinstance(dist, DiscreteDistribution):
                self._table[x] = dist
            else:
                self._table[x] = DiscreteDistribution(dist)

        if input_alphabet is not None:
            for x in input_alphabet:
                if x not in self._table:
                    raise ValueError(f"Input symbol {x} missing transition distribution")

        outputs: set[U] = set()
        for d in self._table.values():
            outputs.update(d.support())
        self._output_alphabet: tuple[U, ...] = tuple(sorted(outputs, key=str))
        self._input_alphabet: tuple[T, ...] = tuple(sorted(self._table.keys(), key=str))

    @property
    def input_alphabet(self) -> tuple[T, ...]:
        return self._input_alphabet

    @property
    def output_alphabet(self) -> tuple[U, ...]:
        return self._output_alphabet

    def transition(self, x: T) -> DiscreteDistribution[U]:
        if x not in self._table:
            raise KeyError(f"Symbol {x} not in channel input alphabet")
        return self._table[x]

    def prob(self, y: U, x: T) -> Fraction:
        return self.transition(x).prob(y)

    def apply(self, input_dist: DiscreteDistribution[T]) -> DiscreteDistribution[U]:
        """Compute output distribution P_Y(y) = sum_x P_X(x) * W(y | x)."""
        out: dict[U, Fraction] = {}
        for x, px in input_dist.items():
            if x not in self._table:
                raise ValueError(f"Input distribution support item {x} not accepted by channel")
            trans = self._table[x]
            for y, py_given_x in trans.items():
                out[y] = out.get(y, Fraction(0)) + px * py_given_x
        return DiscreteDistribution(out)

    def joint_distribution(self, input_dist: DiscreteDistribution[T]) -> DiscreteDistribution[tuple[T, U]]:
        """Compute joint distribution P_{X, Y}(x, y) = P_X(x) * W(y | x)."""
        joint: dict[tuple[T, U], Fraction] = {}
        for x, px in input_dist.items():
            for y, py_given_x in self.transition(x).items():
                joint[(x, y)] = px * py_given_x
        return DiscreteDistribution(joint)

    def compose(self, next_channel: Channel[U, V]) -> Channel[T, V]:
        """Markov channel concatenation: (W2 o W1)(z | x) = sum_y W1(y | x) * W2(z | y)."""
        composed_table: dict[T, DiscreteDistribution[V]] = {}
        for x in self._input_alphabet:
            z_probs: dict[V, Fraction] = {}
            for y, py_given_x in self.transition(x).items():
                w2_dist = next_channel.transition(y)
                for z, pz_given_y in w2_dist.items():
                    z_probs[z] = z_probs.get(z, Fraction(0)) + py_given_x * pz_given_y
            composed_table[x] = DiscreteDistribution(z_probs)
        return Channel(composed_table, input_alphabet=self._input_alphabet)

    # Standard channel constructors
    @staticmethod
    def identity(alphabet: Iterable[T]) -> Channel[T, T]:
        return Channel({x: DiscreteDistribution.point_mass(x) for x in alphabet})

    @staticmethod
    def deterministic(mapping: Mapping[T, U]) -> Channel[T, U]:
        return Channel({x: DiscreteDistribution.point_mass(y) for x, y in mapping.items()})

    @staticmethod
    def binary_symmetric(crossover_prob: Fraction | float) -> Channel[int, int]:
        """Binary Symmetric Channel (BSC) with error probability p."""
        p = Fraction(crossover_prob) if not isinstance(crossover_prob, Fraction) else crossover_prob
        q = Fraction(1) - p
        return Channel({
            0: DiscreteDistribution({0: q, 1: p}),
            1: DiscreteDistribution({0: p, 1: q}),
        })

    @staticmethod
    def binary_erasure(erasure_prob: Fraction | float, erasure_symbol: str = "e") -> Channel[int, int | str]:
        """Binary Erasure Channel (BEC) with erasure probability epsilon."""
        eps = Fraction(erasure_prob) if not isinstance(erasure_prob, Fraction) else erasure_prob
        rem = Fraction(1) - eps
        return Channel({
            0: DiscreteDistribution({0: rem, erasure_symbol: eps}),
            1: DiscreteDistribution({1: rem, erasure_symbol: eps}),
        })

    @staticmethod
    def coarse_graining(projection: Callable[[T], U], input_alphabet: Iterable[T]) -> Channel[T, U]:
        """Lossy or deterministic coarse-graining projection channel."""
        mapping = {x: projection(x) for x in input_alphabet}
        return Channel.deterministic(mapping)

    @staticmethod
    def constant_reset(reset_val: U, input_alphabet: Iterable[T]) -> Channel[T, U]:
        """Complete memory erasure channel mapping all inputs to a fixed reset state."""
        return Channel({x: DiscreteDistribution.point_mass(reset_val) for x in input_alphabet})


# -----------------------------------------------------------------------------
# 4. Data Processing Inequality (DPI)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class DPICertificate:
    """Certificate of Data Processing Inequality verification for Markov chain X -> Y -> Z."""
    i_xy: float
    i_xz: float
    delta_i: float  # I(X; Y) - I(X; Z) >= 0
    passed: bool
    is_sufficient_statistic: bool  # Delta I == 0 within numerical precision
    exact_rational_diff: Fraction | None = None


def verify_data_processing_inequality(
    input_dist: DiscreteDistribution[T],
    channel1: Channel[T, U],
    channel2: Channel[U, V],
    tolerance: float = 1e-12,
) -> DPICertificate:
    """Verify operational Data Processing Inequality:

    For Markov chain X -> Y -> Z,
        I(X; Z) <= I(X; Y), or Delta I = I(X; Y) - I(X; Z) >= 0.
    """
    # Joint distribution P_{X, Y}
    joint_xy = channel1.joint_distribution(input_dist)
    i_xy = mutual_information(joint_xy)

    # Composed channel W_{Z | X} = W2 o W1
    composed = channel1.compose(channel2)
    joint_xz = composed.joint_distribution(input_dist)
    i_xz = mutual_information(joint_xz)

    delta_i = i_xy - i_xz
    passed = delta_i >= -tolerance
    is_sufficient = abs(delta_i) <= tolerance

    # If pure dyadic, compute exact rational difference
    exact_diff: Fraction | None = None
    try:
        if (
            joint_xy.is_pure_dyadic()
            and marginal_x(joint_xy).is_pure_dyadic()
            and marginal_y(joint_xy).is_pure_dyadic()
            and joint_xz.is_pure_dyadic()
            and marginal_x(joint_xz).is_pure_dyadic()
            and marginal_y(joint_xz).is_pure_dyadic()
        ):
            exact_ixy = exact_dyadic_mutual_information(joint_xy)
            exact_ixz = exact_dyadic_mutual_information(joint_xz)
            exact_diff = exact_ixy - exact_ixz
            if exact_diff < 0:
                passed = False
    except Exception:
        pass

    return DPICertificate(
        i_xy=i_xy,
        i_xz=i_xz,
        delta_i=delta_i,
        passed=passed,
        is_sufficient_statistic=is_sufficient,
        exact_rational_diff=exact_diff,
    )


# -----------------------------------------------------------------------------
# 5. Distributed Observers, Protocols & Transmission Fidelity
# -----------------------------------------------------------------------------

@dataclass
class DistributedObserver(Generic[T]):
    """Observer with discrete local state/alphabet and memory retention."""
    name: str
    alphabet: tuple[T, ...]
    memory: T | None = None

    def store(self, value: T) -> None:
        if value not in self.alphabet:
            raise ValueError(f"Value {value} not in observer {self.name} alphabet")
        self.memory = value

    def readout(self) -> T | None:
        return self.memory

    def erase_memory(self, reset_state: T) -> None:
        if reset_state not in self.alphabet:
            raise ValueError(f"Reset state {reset_state} not in alphabet")
        self.memory = reset_state


class OperationalCommunicationProtocol(Generic[T, U, V]):
    """Operational communication system between distributed observers:

    Source M -> Encoder E(M) -> Channel W(Y | X) -> Decoder D(Y) -> Estimated M_hat.
    """

    def __init__(
        self,
        message_distribution: DiscreteDistribution[T],
        encoder: Callable[[T], U] | Mapping[T, U],
        channel: Channel[U, V],
        decoder: Callable[[V], T] | Mapping[V, T],
    ) -> None:
        self.message_dist = message_distribution
        self.encode: Callable[[T], U] = encoder if callable(encoder) else (lambda m: encoder[m])
        self.channel = channel
        self.decode: Callable[[V], T] = decoder if callable(decoder) else (lambda y: decoder[y])

    def transmission_fidelity(self) -> Fraction:
        """Exact average transmission fidelity F in Q:

        F = sum_{m in M} P_M(m) * sum_{y: D(y) = m} W(y | E(m)).
        """
        fid = Fraction(0)
        for m, pm in self.message_dist.items():
            u = self.encode(m)
            trans = self.channel.transition(u)
            for y, py_given_u in trans.items():
                if self.decode(y) == m:
                    fid += pm * py_given_u
        return fid

    def error_probability(self) -> Fraction:
        """Exact operational block error probability P_e = 1 - F."""
        return Fraction(1) - self.transmission_fidelity()

    def mutual_information_transferred(self) -> float:
        """Mutual information I(M; M_hat) between transmitted and decoded message."""
        joint_m_mhat: dict[tuple[T, T], Fraction] = {}
        for m, pm in self.message_dist.items():
            u = self.encode(m)
            trans = self.channel.transition(u)
            for y, py_given_u in trans.items():
                m_hat = self.decode(y)
                pair = (m, m_hat)
                joint_m_mhat[pair] = joint_m_mhat.get(pair, Fraction(0)) + pm * py_given_u
        return mutual_information(DiscreteDistribution(joint_m_mhat))


# -----------------------------------------------------------------------------
# 6. Memory Retention Limits & Lossy Coarse-Graining
# -----------------------------------------------------------------------------

class MemoryRetentionModel(Generic[T]):
    """Model of sequential memory retention and progressive decay over time steps."""

    def __init__(
        self,
        initial_distribution: DiscreteDistribution[T],
        step_transition: Channel[T, T],
    ) -> None:
        self.initial_dist = initial_distribution
        self.step_channel = step_transition

    def distribution_at_step(self, steps: int) -> DiscreteDistribution[T]:
        if steps < 0:
            raise ValueError("Steps must be non-negative")
        dist = self.initial_dist
        for _ in range(steps):
            dist = self.step_channel.apply(dist)
        return dist

    def retained_mutual_information(self, steps: int) -> float:
        """Compute I(M_0; M_k) retained between initial memory and state after k steps."""
        if steps == 0:
            joint = DiscreteDistribution({(x, x): p for x, p in self.initial_dist.items()})
            return mutual_information(joint)

        current_channel = self.step_channel
        for _ in range(steps - 1):
            current_channel = current_channel.compose(self.step_channel)

        joint = current_channel.joint_distribution(self.initial_dist)
        return mutual_information(joint)

    def verify_monotonic_retention_loss(self, max_steps: int = 5) -> list[float]:
        """Verify that retained information is monotonically non-increasing:

        I(M_0; M_{k+1}) <= I(M_0; M_k).
        """
        retained: list[float] = []
        for k in range(max_steps + 1):
            info = self.retained_mutual_information(k)
            retained.append(info)
            if k > 0:
                assert retained[k] <= retained[k - 1] + 1e-12, (
                    f"Retention monotonicity violated at step {k}: {retained[k]} > {retained[k-1]}"
                )
        return retained


def coarse_grain_loss(
    distribution: DiscreteDistribution[T],
    projection: Callable[[T], U],
) -> tuple[DiscreteDistribution[U], float]:
    """Compute coarse-grained distribution and information loss Delta H = H(S) - H(pi(S)) >= 0."""
    projected: dict[U, Fraction] = {}
    for x, p in distribution.items():
        y = projection(x)
        projected[y] = projected.get(y, Fraction(0)) + p
    coarse_dist = DiscreteDistribution(projected)

    h_fine = distribution.shannon_entropy()
    h_coarse = coarse_dist.shannon_entropy()
    loss = max(0.0, h_fine - h_coarse)
    return coarse_dist, loss


# -----------------------------------------------------------------------------
# 7. Landauer Operational Erasure Cost Accounting
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class LandauerReceipt:
    """Operational audit receipt for memory erasure."""
    initial_entropy_bits: float
    final_entropy_bits: float
    erased_entropy_bits: float
    exact_erased_entropy_q: Fraction | None
    temperature_kelvin: float
    minimal_heat_dissipated_joules: float
    operational_non_reversibility: bool


class LandauerAccounting:
    """Accounting for operational erasure of observer memory state."""

    BOLTZMANN_CONSTANT = 1.380649e-23  # J/K

    def __init__(
        self,
        initial_distribution: DiscreteDistribution[T],
        reset_state: T,
        temperature_kelvin: float = 300.0,
    ) -> None:
        self.initial_dist = initial_distribution
        self.reset_state = reset_state
        self.temperature = temperature_kelvin

    def compute_erasure_cost(self) -> LandauerReceipt:
        h_init = self.initial_dist.shannon_entropy()
        # After reset, all probability is in reset_state -> H_final = 0
        h_final = 0.0
        erased_bits = h_init - h_final

        exact_q: Fraction | None = None
        if self.initial_dist.is_pure_dyadic():
            exact_q = self.initial_dist.exact_dyadic_shannon_entropy()

        # Landauer minimal dissipation Q >= kB * T * ln(2) * Delta H
        heat = self.BOLTZMANN_CONSTANT * self.temperature * math.log(2.0) * erased_bits
        is_irreversible = len(self.initial_dist.support()) > 1

        return LandauerReceipt(
            initial_entropy_bits=h_init,
            final_entropy_bits=h_final,
            erased_entropy_bits=erased_bits,
            exact_erased_entropy_q=exact_q,
            temperature_kelvin=self.temperature,
            minimal_heat_dissipated_joules=heat,
            operational_non_reversibility=is_irreversible,
        )
