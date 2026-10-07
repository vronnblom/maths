"""Equality helpers (docs/plan/06 §6.1, "Equality helpers (and their pitfalls)").

Every helper returns True when the claim holds and False when it is decided to be false. When
SymPy cannot decide, it raises Undecidable (an AssertionError): **an undecidable comparison fails,
it never passes**. Never compare SymPy objects with `==`: it is structural, so a correct answer
in another form would fail, and `simplify(...) == 0` silently misses zeros SymPy doesn't spot.

These functions are pure. mathcheck/__init__.py wraps them so that each True result counts as one
mathcheck assertion for the test that made it (the coverage plugin needs that count, §6.1).
"""

from __future__ import annotations

import random

import mpmath
import sympy as sp


class Undecidable(AssertionError):
    """SymPy could neither prove nor refute the claim. Counts as a failure."""


def _sympify(v):
    if isinstance(v, (tuple, list)):
        return tuple(_sympify(e) for e in v)
    if isinstance(v, (sp.Basic, bool)):
        return sp.sympify(v)
    return sp.sympify(v, strict=True)  # numbers; strings are refused (they would be parsed)


def _check_symbols(a, b):
    """Two different symbols with one name (e.g. a plain Symbol('x') against mathcheck's real x)
    never compare equal; say so instead of failing mysteriously."""
    seen: dict[str, sp.Symbol] = {}
    for e in (a, b):
        for s in getattr(e, "free_symbols", ()):
            other = seen.setdefault(s.name, s)
            if other is not s and other != s:
                raise Undecidable(f"two different symbols are called {s.name!r} ({other.assumptions0} vs "
                                  f"{s.assumptions0}): use mathcheck's symbols (from mathcheck import x)")


def _decide_zero(d) -> bool:
    """True if d is zero, False if it is not; Undecidable otherwise."""
    if d.has(sp.nan, sp.zoo):
        raise Undecidable(f"the difference {d} is undefined (nan or complex infinity)")
    z = d.is_zero
    if z is None:
        d = sp.simplify(d)
        z = d.is_zero
    if z is None:
        z = d.equals(0)
    if z is None:
        raise Undecidable(f"SymPy cannot decide whether {d} is zero")
    return bool(z)


def equal(a, b) -> bool:
    """a and b are the same value: expressions, numbers, tuples (elementwise), sets, True/False."""
    a, b = _sympify(a), _sympify(b)
    if isinstance(a, tuple) or isinstance(b, tuple):
        if not (isinstance(a, tuple) and isinstance(b, tuple)):
            return False
        return len(a) == len(b) and all(equal(p, q) for p, q in zip(a, b))
    _check_symbols(a, b)
    if isinstance(a, sp.Set) or isinstance(b, sp.Set):
        if not (isinstance(a, sp.Set) and isinstance(b, sp.Set)):
            return False
        empty = a.symmetric_difference(b).is_empty
        if empty is None:
            raise Undecidable(f"SymPy cannot decide whether {a} and {b} are the same set")
        return bool(empty)
    if isinstance(a, sp.logic.boolalg.BooleanAtom) or isinstance(b, sp.logic.boolalg.BooleanAtom):
        if not (isinstance(a, sp.logic.boolalg.BooleanAtom) and isinstance(b, sp.logic.boolalg.BooleanAtom)):
            return False
        return a is b  # sp.true and sp.false are singletons
    if not (isinstance(a, sp.Expr) and isinstance(b, sp.Expr)):
        raise Undecidable(f"equal() compares values, not {type(a).__name__} and {type(b).__name__}")
    if a.has(sp.nan, sp.zoo) or b.has(sp.nan, sp.zoo):
        raise Undecidable(f"{a} or {b} is undefined (nan or complex infinity), so it equals nothing")
    infinite = (sp.S.Infinity, sp.S.NegativeInfinity)
    if any(a is i or b is i for i in infinite):  # oo - oo is nan, so compare the singletons themselves
        return a is b
    if a.has(sp.oo, -sp.oo) or b.has(sp.oo, -sp.oo):
        r = a.equals(b)
        if r is None:
            raise Undecidable(f"SymPy cannot decide whether {a} equals {b}")
        return bool(r)
    return _decide_zero(a - b)


def equal_up_to_constant(F, f, var, domain=None) -> bool:
    """F is an antiderivative of f with respect to var: F' = f (on `domain` if given)."""
    dF = sp.diff(_sympify(F), var)
    if domain is not None:
        return equal_on_domain(dF, f, var, domain)
    return equal(dF, f)


def _as_interval(domain) -> sp.Interval:
    if isinstance(domain, sp.Interval):
        return domain
    lo, hi = domain
    return sp.Interval.open(lo, hi)


def _assumptions(domain: sp.Interval) -> dict:
    lo, hi = domain.inf, domain.sup
    if lo.is_extended_nonnegative:
        return {"positive": True} if (lo.is_positive or domain.left_open) else {"nonnegative": True}
    if hi.is_extended_nonpositive:
        return {"negative": True} if (hi.is_negative or domain.right_open) else {"nonpositive": True}
    return {"real": True}


def equal_on_domain(a, b, var, domain, n=20) -> bool:
    """a = b for every var in `domain` (an sp.Interval, or (lo, hi) for the open interval).

    Symbolically with the strongest assumption the domain gives (positive, negative, …), and
    numerically at n random points of the domain. Both must agree; undecidable fails.
    """
    a, b = _sympify(a), _sympify(b)
    domain = _as_interval(domain)
    d = sp.Dummy(var.name, **_assumptions(domain))
    symbolic = equal(a.xreplace({var: d}), b.xreplace({var: d}))
    if not symbolic:
        return False
    if not numeric_spot_check(a, b, var, domain, n=n):
        raise AssertionError(f"SymPy says {a} = {b} on {domain}, but they differ numerically there")
    return True


def _sample_points(domain: sp.Interval, n: int, seed: int) -> list:
    lo, hi = domain.inf, domain.sup
    lo = (hi - 200 if hi.is_finite else sp.Integer(-100)) if lo.is_infinite else lo
    hi = (lo + 200 if lo.is_finite else sp.Integer(100)) if hi.is_infinite else hi
    rng = random.Random(seed)
    lo, hi = mpmath.mpf(sp.N(lo, 40)), mpmath.mpf(sp.N(hi, 40))
    # Interior points only, away from the endpoints (which may be excluded or singular).
    return [lo + (hi - lo) * mpmath.mpf(rng.uniform(0.001, 0.999)) for _ in range(n)]


def numeric_spot_check(a, b, var, interval, n=50, tol=1e-9, seed=0) -> bool:
    """|a - b| <= tol * (1 + |b|) at n random points of `interval`, with mpmath at 30 digits.

    Points where either side is undefined or not finite are skipped, but at least half of the
    points must be usable; otherwise the check fails (it cannot have checked anything).
    """
    a, b = _sympify(a), _sympify(b)
    domain = _as_interval(interval)
    fa = sp.lambdify(var, a, modules="mpmath")
    fb = sp.lambdify(var, b, modules="mpmath")
    used = 0
    with mpmath.workdps(30):
        for p in _sample_points(domain, n, seed):
            try:
                va, vb = mpmath.mpmathify(fa(p)), mpmath.mpmathify(fb(p))
            except (ZeroDivisionError, ValueError, OverflowError, TypeError):
                continue
            if not (mpmath.isfinite(va) and mpmath.isfinite(vb)):
                continue
            used += 1
            if abs(va - vb) > tol * (1 + abs(vb)):
                return False
    if used < (n + 1) // 2:
        raise Undecidable(f"numeric_spot_check could evaluate both sides at only {used} of {n} points of {domain}")
    return True
