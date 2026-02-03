import argparse
import numpy as np
import plotly.graph_objects as go

from io_utils import load_dataset, load_model_from_pyfiles
from plot_utils import ensure_dir

GIRDERS = {
    "Girder 1": [13, 22, 31, 40, 49, 58, 67, 76, 81],
    "Girder 2": [14, 23, 32, 41, 50, 59, 68, 77, 82],
    "Girder 3": [15, 24, 33, 42, 51, 60, 69, 78, 83],
    "Girder 4": [16, 25, 34, 43, 52, 61, 70, 79, 84],
    "Girder 5": [17, 26, 35, 44, 53, 62, 71, 80, 85],
}


def require_component(ds, comp_name: str):
    comps = list(ds.coords["Component"].values)
    if comp_name not in comps:
        raise KeyError(
            f"Component '{comp_name}' dataset me nahi mila.\n"
            f"Available Components: {comps}"
        )


def get_force(ds, element_id: int, comp_name: str) -> float:
    return float(ds["forces"].sel(Element=element_id, Component=comp_name).values)


def build_girder_node_path(nodes, elems, elem_list):
    """
    Assumes elem_list already ordered along the girder (as provided).
    node sequence = [node_i of first] + [node_j of each element]
    """
    first_e = elem_list[0]
    ni, _ = elems[first_e]
    node_ids = [ni]
    for e in elem_list:
        _, nj = elems[e]
        node_ids.append(nj)

    pts = np.array([nodes[n] for n in node_ids], dtype=float)  # (x,y,z)
    return pts


def main(dataset_path, nodes_py, elements_py, out_dir):
    ensure_dir(out_dir)

    ds = load_dataset(dataset_path)
    nodes, elems = load_model_from_pyfiles(nodes_py, elements_py)

    for comp in ["Mz_i", "Mz_j", "Vy_i", "Vy_j"]:
        require_component(ds, comp)

    shear_scale = 1.0
    moment_scale = 1.0

    fig_sfd = go.Figure()
    fig_bmd = go.Figure()

    for gname, elist in GIRDERS.items():
        for e in elist:
            if e not in elems:
                raise KeyError(f"{gname}: element {e} element.py me nahi mila.")

        base_pts = build_girder_node_path(nodes, elems, elist)

        # Baseline frame
        fig_sfd.add_trace(go.Scatter3d(
            x=base_pts[:, 0], y=base_pts[:, 1], z=base_pts[:, 2],
            mode="lines", name=f"{gname} frame"
        ))
        fig_bmd.add_trace(go.Scatter3d(
            x=base_pts[:, 0], y=base_pts[:, 1], z=base_pts[:, 2],
            mode="lines", name=f"{gname} frame"
        ))

        vy_nodes, mz_nodes = [], []
        for idx, e in enumerate(elist):
            vy_i = get_force(ds, e, "Vy_i")
            vy_j = get_force(ds, e, "Vy_j")
            mz_i = get_force(ds, e, "Mz_i")
            mz_j = get_force(ds, e, "Mz_j")

            if idx == 0:
                vy_nodes.append(vy_i)
                mz_nodes.append(mz_i)
            vy_nodes.append(vy_j)
            mz_nodes.append(mz_j)

        vy_nodes = np.array(vy_nodes, dtype=float)
        mz_nodes = np.array(mz_nodes, dtype=float)

        sfd_pts = base_pts.copy()
        sfd_pts[:, 1] = sfd_pts[:, 1] + shear_scale * vy_nodes

        bmd_pts = base_pts.copy()
        bmd_pts[:, 1] = bmd_pts[:, 1] + moment_scale * mz_nodes

        fig_sfd.add_trace(go.Scatter3d(
            x=sfd_pts[:, 0], y=sfd_pts[:, 1], z=sfd_pts[:, 2],
            mode="lines+markers", name=f"{gname} SFD"
        ))
        fig_bmd.add_trace(go.Scatter3d(
            x=bmd_pts[:, 0], y=bmd_pts[:, 1], z=bmd_pts[:, 2],
            mode="lines+markers", name=f"{gname} BMD"
        ))

        for k in range(len(base_pts)):
            fig_sfd.add_trace(go.Scatter3d(
                x=[base_pts[k, 0], sfd_pts[k, 0]],
                y=[base_pts[k, 1], sfd_pts[k, 1]],
                z=[base_pts[k, 2], sfd_pts[k, 2]],
                mode="lines", showlegend=False
            ))
            fig_bmd.add_trace(go.Scatter3d(
                x=[base_pts[k, 0], bmd_pts[k, 0]],
                y=[base_pts[k, 1], bmd_pts[k, 1]],
                z=[base_pts[k, 2], bmd_pts[k, 2]],
                mode="lines", showlegend=False
            ))

    fig_sfd.update_layout(
        title="3D Shear Force Diagram (All Girders)",
        scene=dict(xaxis_title="X", yaxis_title="Y (extrusion)", zaxis_title="Z")
    )
    fig_bmd.update_layout(
        title="3D Bending Moment Diagram (All Girders)",
        scene=dict(xaxis_title="X", yaxis_title="Y (extrusion)", zaxis_title="Z")
    )

    fig_sfd.write_html(f"{out_dir}/task2_3d_SFD.html")
    fig_bmd.write_html(f"{out_dir}/task2_3d_BMD.html")

    print("✅ Task-2 done:")
    print(f" - {out_dir}/task2_3d_SFD.html")
    print(f" - {out_dir}/task2_3d_BMD.html")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--nodes_py", required=True)
    ap.add_argument("--elements_py", required=True)
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()

    main(args.dataset, args.nodes_py, args.elements_py, args.out)
