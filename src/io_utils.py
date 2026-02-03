import importlib.util
import xarray as xr


def load_dataset(path: str) -> xr.Dataset:
    return xr.open_dataset(path)


def _load_py_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    spec.loader.exec_module(mod)
    return mod


def _iter_public_vars(mod):
    """Yield (name, value) for non-dunder variables."""
    for name in dir(mod):
        if name.startswith("__"):
            continue
        try:
            value = getattr(mod, name)
        except Exception:
            continue
        yield name, value


def _looks_like_nodes_dict(obj):
    if not isinstance(obj, dict) or len(obj) == 0:
        return False
    k, v = next(iter(obj.items()))
    if not isinstance(k, (int, str)):
        return False
    if not isinstance(v, (list, tuple)) or len(v) != 3:
        return False
    return all(isinstance(t, (int, float)) for t in v)


def _looks_like_nodes_rows(obj):
    if not isinstance(obj, (list, tuple)) or len(obj) == 0:
        return False
    r = obj[0]
    if not isinstance(r, (list, tuple)) or len(r) != 4:
        return False
    return isinstance(r[0], (int, float, str)) and all(isinstance(t, (int, float)) for t in r[1:])


def _looks_like_elems_dict(obj):
    if not isinstance(obj, dict) or len(obj) == 0:
        return False
    k, v = next(iter(obj.items()))
    if not isinstance(k, (int, str)):
        return False
    if not isinstance(v, (list, tuple)) or len(v) != 2:
        return False
    return all(isinstance(t, (int, float, str)) for t in v)


def _looks_like_elems_rows(obj):
    if not isinstance(obj, (list, tuple)) or len(obj) == 0:
        return False
    r = obj[0]
    if not isinstance(r, (list, tuple)) or len(r) != 3:
        return False
    return all(isinstance(t, (int, float, str)) for t in r)


def _normalize_nodes(nodes_obj):
    nodes = {}
    if isinstance(nodes_obj, dict):
        for nid, xyz in nodes_obj.items():
            x, y, z = xyz
            nodes[int(nid)] = (float(x), float(y), float(z))
    else:
        for row in nodes_obj:
            nid = int(row[0])
            nodes[nid] = (float(row[1]), float(row[2]), float(row[3]))
    return nodes


def _normalize_elems(elems_obj):
    elems = {}
    if isinstance(elems_obj, dict):
        for eid, conn in elems_obj.items():
            ni, nj = conn
            elems[int(eid)] = (int(ni), int(nj))
    else:
        for row in elems_obj:
            eid = int(row[0])
            elems[eid] = (int(row[1]), int(row[2]))
    return elems


def load_model_from_pyfiles(nodes_py_path: str, elements_py_path: str):
    """
    Auto-detect nodes and elements variables from node.py and element.py without needing exact variable names.
    """
    node_mod = _load_py_module_from_path("node_mod", nodes_py_path)
    elem_mod = _load_py_module_from_path("elem_mod", elements_py_path)

    nodes_obj = None
    nodes_candidates = []
    for name, val in _iter_public_vars(node_mod):
        if _looks_like_nodes_dict(val) or _looks_like_nodes_rows(val):
            nodes_candidates.append(name)
            if nodes_obj is None:
                nodes_obj = val

    if nodes_obj is None:
        avail = [n for n, _ in _iter_public_vars(node_mod)]
        raise AttributeError(
            f"node.py me nodes detect nahi hua.\n"
            f"Candidates found: {nodes_candidates}\n"
            f"Available vars: {avail}\n"
            f"Expected formats:\n"
            f"  dict: {{node_id:(x,y,z)}}\n"
            f"  rows: [[node_id,x,y,z], ...]"
        )

    elems_obj = None
    elems_candidates = []
    for name, val in _iter_public_vars(elem_mod):
        if _looks_like_elems_dict(val) or _looks_like_elems_rows(val):
            elems_candidates.append(name)
            if elems_obj is None:
                elems_obj = val

    if elems_obj is None:
        avail = [n for n, _ in _iter_public_vars(elem_mod)]
        raise AttributeError(
            f"element.py me elements detect nahi hua.\n"
            f"Candidates found: {elems_candidates}\n"
            f"Available vars: {avail}\n"
            f"Expected formats:\n"
            f"  dict: {{elem_id:(node_i,node_j)}}\n"
            f"  rows: [[elem_id,node_i,node_j], ...]"
        )

    nodes = _normalize_nodes(nodes_obj)
    elems = _normalize_elems(elems_obj)
    return nodes, elems
