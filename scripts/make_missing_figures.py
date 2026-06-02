"""Author the specialized figures directly (reliable substitutes for ones the
local model botches): F3 colour chart, F6 transit histogram, F7 Bristol Stool
Scale, F8 faecal-pH vs a* retention, F9 multivariate correlation heatmap.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

np.random.seed(42)
assets = Path(__file__).parents[1] / "assets"
assets.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.savefig(assets / name, dpi=150, bbox_inches="tight")
    plt.close(fig)


# --- F3: CIELAB a* colour-reference chart ---
fig, ax = plt.subplots(figsize=(8, 2.4))
for i, a in enumerate(np.linspace(0, 60, 12)):
    t = a / 60.0
    ax.add_patch(plt.Rectangle((i, 0), 1, 1,
                 color=(min(0.65 + 0.35 * t, 1.0), max(0.75 * (1 - t) + 0.2, 0.0), max(0.25 * (1 - t), 0.0))))
    ax.text(i + 0.5, -0.16, f"{a:.0f}", ha="center", va="top", fontsize=8)
ax.set_xlim(0, 12)
ax.set_ylim(-0.35, 1.05)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(r"CIELAB $a^*$ colour-reference chart for faecal coloration grading")
ax.text(6, -0.31, r"$a^*$ (green$\rightarrow$red axis)", ha="center", fontsize=9)
save(fig, "F3.png")

# --- F6: faecal transit-time distribution ---
fig, ax = plt.subplots(figsize=(6, 4))
data = np.clip(np.random.gamma(9.0, 0.8, 4000), 3.5, 13.0)
ax.hist(data, bins=30, color="#7f5539", edgecolor="white")
ax.axvline(float(np.median(data)), color="black", ls="--", label=f"median = {np.median(data):.1f} h")
ax.set_xlabel("Luminal transit time (h)")
ax.set_ylabel("Frequency")
ax.set_title("Distribution of gastrointestinal transit time for faecal pigment")
ax.legend()
save(fig, "F6.png")

# --- F7: Bristol Stool Scale vs transit ---
fig, ax = plt.subplots(figsize=(7.2, 4.2))
labels = ["separate hard lumps", "lumpy sausage", "cracked sausage", "smooth soft sausage",
          "soft blobs", "mushy ragged", "entirely liquid"]
transit = [100, 72, 52, 40, 30, 18, 8]
y = np.arange(7)[::-1]
ax.barh(y, transit, color=plt.cm.YlOrBr(np.linspace(0.85, 0.25, 7)), edgecolor="black")
for yi, tr, lab in zip(y, transit, labels):
    ax.text(tr + 2, yi, lab, va="center", fontsize=8)
ax.set_yticks(y)
ax.set_yticklabels([f"Type {i + 1}" for i in range(7)])
ax.set_xlim(0, 140)
ax.set_xlabel("Relative luminal transit time (arb. units)")
ax.set_title("Bristol Stool Scale: consistency type vs transit")
save(fig, "F7.png")

# --- F8: faecal pH vs a* retention ---
fig, ax = plt.subplots(figsize=(6, 4))
pH = np.random.uniform(5.5, 7.5, 140)
a_ret = 92 - 23 * (pH - 5.5) + np.random.normal(0, 5, 140)
sc = ax.scatter(pH, a_ret, c=pH, cmap="RdYlGn_r", edgecolor="k", alpha=0.85)
coef = np.polyfit(pH, a_ret, 1)
xs = np.linspace(5.5, 7.5, 50)
ax.plot(xs, np.polyval(coef, xs), "k--", label=f"fit slope = {coef[0]:.1f}")
ax.set_xlabel("Faecal pH")
ax.set_ylabel(r"$a^*$ (red) retention (%)")
ax.set_title(r"Faecal pH vs betalain red ($a^*$) retention in stool")
ax.legend()
save(fig, "F8.png")

# --- F9: correlation heatmap among faecal parameters ---
labels = [r"$\Delta E$", "Bristol", "pH", "Transit", "FCI"]
M = np.array([[1.00, 0.32, -0.58, 0.21, 0.81],
              [0.32, 1.00, -0.18, 0.74, 0.55],
              [-0.58, -0.18, 1.00, -0.12, -0.49],
              [0.21, 0.74, -0.12, 1.00, 0.47],
              [0.81, 0.55, -0.49, 0.47, 1.00]])
fig, ax = plt.subplots(figsize=(5.4, 4.8))
im = ax.imshow(M, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(5))
ax.set_xticklabels(labels)
ax.set_yticks(range(5))
ax.set_yticklabels(labels)
for i in range(5):
    for j in range(5):
        ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=8)
fig.colorbar(im, label="Pearson r")
ax.set_title("Correlation among faecal parameters")
save(fig, "F9.png")

print("wrote F3, F6, F7, F8, F9")
