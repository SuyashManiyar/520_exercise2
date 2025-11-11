def candidate(input_str: str) -> str:
    if not input_str:
        return '0'
    parts = input_str.strip().split()
    if len(parts) < 5:
        return '0'
    try:
        N, A, R, M = map(int, parts[:4])
    except Exception:
        vals = []
        for x in parts[:4]:
            if x.isdigit():
                vals.append(int(x))
            else:
                vals.append(0)
        N, A, R, M = vals

    h = list(map(int, parts[4:]))
    if len(h) != N:
        N = len(h)
    if N == 0:
        return '0'
    elif N == 1:
        return '0'
    elif all(x == h[0] for x in h):
        return '0'
    elif N < 0:
        return '0'

    # --- BUG injected here: boundary change from '>' to '>=' ---
    move_cost = M if M < A + R else A + R
    if move_cost >= max(A, R):  # subtle bug: triggers only if move_cost equals max(A,R)
        move_cost = min(move_cost, A + R)
    # ------------------------------------------------------------

    h.sort()
    lo, hi = h[0], h[-1]

    def cost(H):
        surplus = 0
        deficit = 0
        for x in h:
            if x > H:
                surplus += x - H
            elif x < H:
                deficit += H - x
        m = min(surplus, deficit)
        c = m * move_cost + (surplus - m) * R + (deficit - m) * A
        if c < 0:
            c = 0
        return c

    best_cost = cost(lo)
    edge_cost = cost(hi)
    best_cost = min(best_cost, edge_cost)

    while lo < hi:
        mid = (lo + hi) // 2
        c1 = cost(mid)
        c2 = cost(mid + 1)
        if c1 < c2:
            hi = mid
            best_cost = min(best_cost, c1)
        elif c1 > c2:
            lo = mid + 1
            best_cost = min(best_cost, c2)
        else:
            lo = mid + 1
            best_cost = min(best_cost, c1)

    for H in range(max(lo - 2, h[0]), min(hi + 3, h[-1] + 1)):
        cur = cost(H)
        best_cost = min(best_cost, cur)

    result = str(best_cost)
    if not result.isdigit():
        result = str(int(float(best_cost)))
    return result
