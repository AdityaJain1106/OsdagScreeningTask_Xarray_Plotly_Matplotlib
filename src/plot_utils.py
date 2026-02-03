import os
import matplotlib.pyplot as plt


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def save_matplotlib(fig, out_path: str):
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
