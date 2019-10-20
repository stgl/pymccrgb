""" Convenience functions for plotting point cloud features """

import numpy as np

from copy import copy

from itertools import combinations
from skimage.color import lab2rgb

from mpl_toolkits.mplot3d import Axes3D

import matplotlib
import matplotlib.pyplot as plt


def initialize_plot_settings():
    plt.style.use("ggplot")
    matplotlib.rcParams["figure.figsize"] = (8, 8)
    matplotlib.rcParams["font.size"] = 14
    matplotlib.rcParams["axes.labelsize"] = 18
    matplotlib.rcParams["xtick.labelsize"] = 14
    matplotlib.rcParams["ytick.labelsize"] = 14
    matplotlib.rcParams["legend.fontsize"] = 14

    matplotlib.rcParams["axes.labelcolor"] = "k"

    matplotlib.rcParams["xtick.direction"] = "in"
    matplotlib.rcParams["ytick.direction"] = "in"
    matplotlib.rcParams["axes.spines.right"] = False
    matplotlib.rcParams["axes.spines.top"] = False
    matplotlib.rcParams["axes.grid"] = False

    matplotlib.rcParams["axes.facecolor"] = "w"
    matplotlib.rcParams["axes.edgecolor"] = "k"
    matplotlib.rcParams["xtick.color"] = "k"
    matplotlib.rcParams["ytick.color"] = "k"

    matplotlib.rcParams["legend.frameon"] = False

    matplotlib.rcParams["savefig.dpi"] = 300
    matplotlib.rcParams["savefig.pad_inches"] = 0


def style_plot(func):
    initialize_plot_settings()
    return func


def color_bins(bins, L=50, **kwargs):
    """ Define colors for histograms of CIELab colors """
    colors = []
    for i, bin in enumerate(bins[:-1]):
        if "b" in kwargs:
            a = (bins[i] + bins[i + 1]) / 2
            b = kwargs["b"]
        if "a" in kwargs:
            a = kwargs["a"]
            b = (bins[i] + bins[i + 1]) / 2
        c = np.array([L, a, b]).reshape(1, 1, 3)
        color = lab2rgb(c)[0]
        colors.append(color)
    nrows = bins.shape[0] - 1
    colors = np.array(colors).reshape(nrows, 3)
    return colors


@style_plot
def plot_features(data, colors, names):
    for tup in combinations(names, r=2):
        name1, name2 = tup
        i = names.index(name1)
        j = names.index(name2)

        plt.figure()
        plt.scatter(data[:, i], data[:, j], marker="o", linestyle="None", c=colors)
        plt.xlabel(name1)
        plt.ylabel(name2)


@style_plot
def plot_labels(x, y, labels, mask=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    if mask is not None:
        x = x[mask]
        y = y[mask]
        labels = labels[mask]

    plt.scatter(x, y, c=labels, s=2)


@style_plot
def plot_points(data, axes="xy", cmax=2 ** 8, ax=None):
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    colors = data[:, 3:6]

    if axes == "xy":
        x = x
        y = y
    if axes == "xz":
        x = x
        y = z
    if axes == "yz":
        x = y
        y = z
    else:
        raise ValueError("axes must be one of 'xy', 'xz', or 'yz'. Got " + str(axes))

    if ax is None:
        fig, ax = plt.subplots(1, 1)
    ax.scatter(x, y, marker=".", linestyle="None", c=colors / cmax)
    ax.axis("equal")


@style_plot
def plot_points_3d(data, ax=None, **kwargs):
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    colors = copy(data[:, 3:6])
    colors /= colors.max()

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, marker=".", c=colors, **kwargs)

    # ax.set_aspect('equal')
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.xaxis.set_major_locator(plt.MaxNLocator(3))
    ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    ax.zaxis.set_major_locator(plt.MaxNLocator(3))


@style_plot
def plot_histogram_by_class_method(data, labels1, labels2, updated, xlabel="NGRDVI"):
    brown = "#8c564b"
    grn = "#2ca02c"

    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    xl = [-0.5, 0.5]

    mask = labels1 == 1
    freq, bins = np.histogram(data[mask], bins=50, density=True)
    wid = np.diff(bins)[0]

    ax[0].bar(
        bins[:-1],
        freq,
        facecolor=brown,
        alpha=0.8,
        width=wid,
        align="edge",
        label="Ground",
    )

    mask = labels1 == 0
    freq, bins = np.histogram(data[mask], bins=50, density=True)
    wid = np.diff(bins)[0]

    ax[0].bar(
        bins[:-1],
        freq,
        facecolor=grn,
        width=wid,
        alpha=0.8,
        align="edge",
        label="Non-ground",
    )

    ax[0].set_xlim(xl)
    ax[0].set_ylabel("Density")
    ax[0].text(0.035, 0.925, "A", fontsize=20, transform=ax[0].transAxes)

    ax[0].legend(loc="best", fontsize=12)

    mask = labels2 == 1
    freq, bins = np.histogram(data[mask], bins=50, density=True)
    wid = np.diff(bins)[0]

    ax[1].bar(bins[:-1], freq, facecolor=brown, width=wid, alpha=0.8, align="edge")

    mask = labels2 == 0
    freq, bins = np.histogram(data[mask], bins=50, density=True)
    wid = np.diff(bins)[0]

    ax[1].bar(bins[:-1], freq, facecolor=grn, width=wid, alpha=0.8, align="edge")

    ax[1].set_xlim(xl)
    ax[1].set_xlabel(xlabel)
    ax[1].text(0.035, 0.925, "B", fontsize=20, transform=ax[1].transAxes)

    mask = updated & labels1
    freq, bins = np.histogram(data[mask], bins=50, density=True)
    wid = np.diff(bins)[0]

    ax[2].bar(bins[:-1], freq, facecolor=grn, width=wid, alpha=0.8, align="edge")

    ax[2].set_xlim(xl)
    ax[2].text(0.035, 0.925, "C", fontsize=20, transform=ax[2].transAxes)

    for axis in ax:
        axis.xaxis.set_major_locator(plt.MaxNLocator(3))
        axis.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.tight_layout()


@style_plot
def plot_results(data, labels_mcc, labels_pred, downsample=None):
    if downsample is not None:
        data = data[::downsample]
        labels_mcc = labels_mcc[::downsample]
        labels_pred = labels_pred[::downsample]

    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    xt = x.min()
    yt = y.min()
    zt = z.max() + 10

    fig = plt.figure(figsize=(16, 4))

    ax = fig.add_subplot(1, 4, 1, projection="3d")
    plot_points_3d(data, ax=ax)
    ax.text(xt, yt, zt, "A", fontsize=20)
    xl = ax.set_xlim()
    yl = ax.set_ylim()
    zl = ax.set_zlim()

    minor_subplots = []

    ax = fig.add_subplot(1, 4, 2, projection="3d")
    mask = labels_mcc == 1
    plot_points_3d(data[mask, :], ax=ax)
    ax.text(xt, yt, zt, "B", fontsize=20)

    minor_subplots.append(ax)

    ax = fig.add_subplot(1, 4, 3, projection="3d")
    mask = labels_pred == 1
    plot_points_3d(data[mask, :], ax=ax)
    ax.text(xt, yt, zt, "C", fontsize=20)

    minor_subplots.append(ax)

    ax = fig.add_subplot(1, 4, 4, projection="3d")
    mask = (labels_pred == 0) & (labels_mcc == 1)
    plot_points_3d(data[mask, :], ax=ax)
    ax.text(xt, yt, zt, "D", fontsize=20)

    minor_subplots.append(ax)

    for ax in minor_subplots:
        ax.set_xlim(xl)
        ax.set_ylim(yl)
        ax.set_zlim(zl)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

    plt.tight_layout()
