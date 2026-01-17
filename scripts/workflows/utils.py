import matplotlib.pyplot as plt
import numpy as np
import os

# Shared Style
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'font.family': 'serif',
    'figure.dpi': 150,
    'lines.linewidth': 2.0,
})

def plot_simulation(time_steps, metrics, title, filename, events=None):
    """
    Generic plotter for multi-sensor simulation data.
    
    Args:
        time_steps (list/array): X-axis values.
        metrics (dict): Key is label, Value is list/array of y-values.
        title (str): Chart title.
        filename (str): Output filename (e.g., 'robotics_sim.png').
        events (list of dict): Optional vertical lines e.g. [{'t': 20, 'label': 'Rain'}]
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd']
    
    for i, (label, values) in enumerate(metrics.items()):
        color = colors[i % len(colors)]
        ax.plot(time_steps, values, label=label, color=color, alpha=0.9)
        
    if events:
        for e in events:
            ax.axvline(x=e['t'], color='gray', linestyle=':', alpha=0.8)
            ax.text(e['t'] + 0.5, 0.5, e['label'], rotation=90, va='center', fontsize=9, color='#333333')
            
    ax.set_title(title)
    ax.set_xlabel("Time Step (t)")
    ax.set_ylabel("Score / Metric")
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower left', frameon=True, fancybox=False)
    
    # Ensure figures directory exists
    os.makedirs("figures", exist_ok=True)
    out_path = os.path.join("figures", filename)
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated plot: {out_path}")
