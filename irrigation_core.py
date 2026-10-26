"""
irrigation_core.py - Farm Irrigation Optimizer (main program / logic only)

No UI code here. The Streamlit front end (app.py) imports this file.

Algorithms (written by hand, using heapq as the priority queue):
  - Dijkstra                 : water routing
  - Greedy + Priority Queue  : irrigation schedule
  - Prim's MST               : minimum network cost
"""
import heapq
import math

INF = 10 ** 9


# ------------------------------------------------------------------
# ALGORITHMS
# ------------------------------------------------------------------
def build_graph(nodes, pipes):
    g = {n: [] for n in nodes}
    for a, b, w in pipes:
        g[a].append((b, w))
        g[b].append((a, w))
    return g


def dijkstra(g, src):
    dist = {n: INF for n in g}
    prev = {n: None for n in g}
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def get_path(prev, node):
    path = []
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path


def schedule(need, water, flow_rate, start_min):
    """Greedy: the driest field (largest deficit) is served first."""
    pq = []
    for f, (deficit, litres) in need.items():
        if deficit > 0:
            heapq.heappush(pq, (-deficit, f, litres))   # negative => max-priority
    clock, plan = start_min, []
    while pq and water > 0:
        _, f, litres = heapq.heappop(pq)
        give = litres if litres < water else water
        plan.append((f, give, clock))
        water -= give
        clock += give / flow_rate * 60
    return plan


def prim(g, start="Source"):
    seen = {start}
    pq = []
    for v, w in g[start]:
        heapq.heappush(pq, (w, start, v))
    mst, total = [], 0
    while pq:
        w, u, v = heapq.heappop(pq)
        if v in seen:
            continue
        seen.add(v)
        mst.append((u, v, w))
        total += w
        for nxt, nw in g[v]:
            if nxt not in seen:
                heapq.heappush(pq, (nw, v, nxt))
    return mst, total, len(seen) == len(g)


# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def to_num(x):
    """Convert a table cell to float, or None if empty / invalid."""
    try:
        if x is None or str(x).strip() == "" or str(x).lower() == "nan":
            return None
        return float(x)
    except ValueError:
        return None


def parse_time(text):
    """'06:00', '6:30', '6:30 PM' -> minutes since midnight (None if invalid)."""
    t = (text or "").strip().upper()
    ampm = None
    if t.endswith("AM") or t.endswith("PM"):
        ampm, t = t[-2:], t[:-2].strip()
    parts = t.split(":")
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        return None
    h, m = int(parts[0]), int(parts[1])
    if ampm:
        if not 1 <= h <= 12:
            return None
        h = h % 12 + (12 if ampm == "PM" else 0)
    if not (0 <= h < 24 and 0 <= m < 60):
        return None
    return h * 60 + m


def fmt_time(minutes):
    t = int(round(minutes))
    h, m = (t // 60) % 24, t % 60
    return f"{h % 12 or 12}:{m:02d} {'AM' if h < 12 else 'PM'}"


def make_svg(nodes, pipes, mst, scheduled):
    """Draw the pipe network as an SVG string (no plotting library needed)."""
    W, H, R = 560, 440, 160
    cx, cy = W / 2, H / 2
    pos = {}
    for i, n in enumerate(nodes):
        ang = 2 * math.pi * i / len(nodes) - math.pi / 2
        pos[n] = (cx + R * math.cos(ang), cy + R * math.sin(ang))

    in_mst = set()
    for u, v, _ in mst:
        in_mst.add((u, v))
        in_mst.add((v, u))

    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'style="background:#f8f9fa;border-radius:10px">']
    for a, b, w in pipes:                                   # edges
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if (a, b) in in_mst:
            s.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="#2d6a4f" stroke-width="4"/>')
        else:
            s.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                     f'stroke="#999" stroke-width="2" stroke-dasharray="6,4"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'<rect x="{mx - 14:.0f}" y="{my - 10:.0f}" width="28" height="18" rx="4" fill="white"/>')
        s.append(f'<text x="{mx:.0f}" y="{my + 4:.0f}" font-size="12" text-anchor="middle" '
                 f'fill="#222">{w:g}</text>')
    for n in nodes:                                         # nodes
        x, y = pos[n]
        if n == "Source":
            s.append(f'<rect x="{x - 32:.0f}" y="{y - 16:.0f}" width="64" height="32" rx="6" fill="#8ecae6" stroke="#333"/>')
            s.append(f'<text x="{x:.0f}" y="{y + 5:.0f}" font-size="13" text-anchor="middle" fill="#111">Source</text>')
        else:
            col = "#95d5b2" if n in scheduled else "#dddddd"
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="{col}" stroke="#333"/>')
            s.append(f'<text x="{x:.0f}" y="{y + 5:.0f}" font-size="14" text-anchor="middle" fill="#111">{n}</text>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------
# MAIN ENTRY POINT (called by the UI)
# ------------------------------------------------------------------
def run_optimizer(water, fields_rows, pipes_rows, flow, start_text):
    """
    Validate the inputs and run every algorithm.

    water       : litres available
    fields_rows : [[name, soil_moisture, target_moisture, area], ...]
    pipes_rows  : [[from, to, cost], ...]
    flow        : litres per hour
    start_text  : e.g. "06:00" or "6:00 AM"

    Returns a dict with routes, schedule, mst_total, connected and svg.
    Raises ValueError with a friendly message if any input is invalid.
    """
    if water is None or to_num(water) is None or to_num(water) <= 0:
        raise ValueError("Enter Water Available above 0.")
    water = to_num(water)
    flow = to_num(flow)
    start_min = parse_time(start_text)
    if flow is None or flow <= 0:
        raise ValueError("Enter a valid Flow Rate (L/hour).")
    if start_min is None:
        raise ValueError("Enter Start Time like 06:00 (or 6:00 AM).")

    # ----- fields -----
    names, need = [], {}
    for i, row in enumerate(fields_rows):
        f = chr(65 + i)
        moist, target, area = to_num(row[1]), to_num(row[2]), to_num(row[3])
        if moist is None or target is None or area is None:
            raise ValueError(f"Field {f}: fill soil moisture, target moisture and area.")
        if not (0 <= moist <= 100 and 0 <= target <= 100) or area <= 0:
            raise ValueError(f"Field {f}: moisture must be 0-100 and area above 0.")
        deficit = max(0, target - moist)
        need[f] = (deficit, deficit * area * 0.01)           # litres = deficit% x area x 0.01
        names.append(f)

    # ----- pipes -----
    valid = {"SOURCE": "Source", **{f: f for f in names}}
    pipes = []
    for j, row in enumerate(pipes_rows, 1):
        a = "" if row[0] is None else str(row[0]).strip().upper()
        b = "" if row[1] is None else str(row[1]).strip().upper()
        c = to_num(row[2])
        if a not in valid or b not in valid:
            raise ValueError(f"Pipe {j}: 'From' and 'To' must be Source or one of {', '.join(names)}.")
        if a == b:
            raise ValueError(f"Pipe {j}: a pipe cannot start and end at the same point.")
        if c is None or c <= 0:
            raise ValueError(f"Pipe {j}: enter a cost above 0.")
        pipes.append((valid[a], valid[b], c))

    # ----- run algorithms -----
    nodes = ["Source"] + names
    g = build_graph(nodes, pipes)
    dist, prev = dijkstra(g, "Source")
    mst, total, connected = prim(g)
    plan = schedule(need, water, flow, start_min)

    routes = []
    for f, _, _ in plan:
        if dist[f] < INF:
            routes.append({"field": f, "path": get_path(prev, f), "cost": dist[f]})
        else:
            routes.append({"field": f, "path": None, "cost": None})

    return {
        "routes": routes,
        "schedule": [{"field": f, "litres": litres, "time": fmt_time(t)} for f, litres, t in plan],
        "mst_total": total,
        "connected": connected,
        "svg": make_svg(nodes, pipes, mst, {f for f, _, _ in plan}),
    }
