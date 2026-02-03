import argparse
import numpy as np
import matplotlib.pyplot as plt

from io_utils import load_dataset, load_model_from_pyfiles
from plot_utils import ensure_dir, save_matplotlib

CENTRAL_GIRDER_ELEMS = [15, 24, 33, 42, 51, 60, 69, 78, 83]


def require_component(ds, comp_name: str):
    comps = list(ds.coords["Component"].values)
    if comp_name not in comps:
        raise KeyError(
            f"Component '{comp_name}' dataset me nahi mila.\n"
            f"Available Components: {comps}"
        )


def get_force(ds, element_id: int, comp_name: str) -> float:
    return float(ds["forces"].sel(Element=element_id, Component=comp_name).values)


def main(dataset_path, nodes_py, elements_py, out_dir):
    ensure_dir(out_dir)

    ds = load_dataset(dataset_path)
    nodes, elems = load_model_from_pyfiles(nodes_py, elements_py)

    for comp in ["Mz_i", "Mz_j", "Vy_i", "Vy_j"]:
        require_component(ds, comp)

    stations, mz_vals, vy_vals = [], [], []

    for e in CENTRAL_GIRDER_ELEMS:
        if e not in elems:
            raise KeyError(f"Element {e} element.py me nahi mila.")

        ni, nj = elems[e]
        if ni not in nodes or nj not in nodes:
            raise KeyError(f"Element {e} ke nodes {ni},{nj} node.py me nahi mile.")

        xi = nodes[ni][0]  # x at i node
        xj = nodes[nj][0]  # x at j node

        mz_i = get_force(ds, e, "Mz_i")
        mz_j = get_force(ds, e, "Mz_j")
        vy_i = get_force(ds, e, "Vy_i")
        vy_j = get_force(ds, e, "Vy_j")

        stations += [xi, xj]
        mz_vals += [mz_i, mz_j]
        vy_vals += [vy_i, vy_j]

    order = np.argsort(stations)
    stations = np.array(stations)[order]
    mz_vals = np.array(mz_vals)[order]
    vy_vals = np.array(vy_vals)[order]

    # BMD
    fig1 = plt.figure()
    plt.plot(stations, mz_vals, marker="o")
    plt.title("Bending Moment Diagram (Central Girder)")
    plt.xlabel("Station (x)")
    plt.ylabel("Mz")
    plt.grid(True)
    save_matplotlib(fig1, f"{out_dir}/task1_BMD.png")

    # SFD
    fig2 = plt.figure()
    plt.plot(stations, vy_vals, marker="o")
    plt.title("Shear Force Diagram (Central Girder)")
    plt.xlabel("Station (x)")
    plt.ylabel("Vy")
    plt.grid(True)
    save_matplotlib(fig2, f"{out_dir}/task1_SFD.png")

    print("✅ Task-1 done:")
    print(f" - {out_dir}/task1_BMD.png")
    print(f" - {out_dir}/task1_SFD.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--nodes_py", required=True)
    ap.add_argument("--elements_py", required=True)
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    main(args.dataset, args.nodes_py, args.elements_py, args.out)
