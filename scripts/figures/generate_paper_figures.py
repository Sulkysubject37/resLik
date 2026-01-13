import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set style for publication
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'font.family': 'serif',
    'figure.dpi': 300,
    'lines.linewidth': 2.0,
    'text.usetex': False,
})

OUTPUT_DIR = "figures"

def ensure_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def draw_architecture_diagram():
    """Figure 1: RLCS Architecture Block Diagram"""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')

    box_props = dict(boxstyle='round,pad=0.5', facecolor='#f0f4f8', edgecolor='#333333', linewidth=1.5)
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#333333')
    
    y_center = 2.5
    spacing = 3.5
    x_start = 1.0
    
    nodes = [
        {'x': x_start, 'text': 'Encoder\n(Learning)', 'label_in': 'Raw Input x', 'label_out': 'Latent z'},
        {'x': x_start + spacing, 'text': 'Sensor Array\n(Sensing)', 'label_in': '', 'label_out': 'Diagnostics d'},
        {'x': x_start + 2*spacing, 'text': 'Control Surface\n(Signaling)', 'label_in': '', 'label_out': 'Signal u'},
        {'x': x_start + 3*spacing, 'text': 'Controller\n(Acting)', 'label_in': '', 'label_out': 'Action a'},
    ]

    for i, node in enumerate(nodes):
        ax.text(node['x'], y_center, node['text'], ha='center', va='center', bbox=box_props, fontsize=10, fontweight='bold')
        
    ax.annotate('', xy=(x_start - 1.2, y_center), xytext=(x_start - 2.5, y_center), arrowprops=arrow_props)
    ax.text(x_start - 1.85, y_center + 0.2, 'Raw Input x', ha='center', va='bottom', fontsize=9, style='italic')

    ax.annotate('', xy=(nodes[1]['x'] - 1.2, y_center), xytext=(nodes[0]['x'] + 1.2, y_center), arrowprops=arrow_props)
    ax.text((nodes[0]['x'] + nodes[1]['x'])/2, y_center + 0.2, 'Latent z', ha='center', va='bottom', fontsize=9, style='italic')

    ax.annotate('', xy=(nodes[2]['x'] - 1.2, y_center), xytext=(nodes[1]['x'] + 1.2, y_center), arrowprops=arrow_props)
    ax.text((nodes[1]['x'] + nodes[2]['x'])/2, y_center + 0.2, 'Diagnostics d', ha='center', va='bottom', fontsize=9, style='italic')

    ax.annotate('', xy=(nodes[3]['x'] - 1.2, y_center), xytext=(nodes[2]['x'] + 1.2, y_center), arrowprops=arrow_props)
    ax.text((nodes[2]['x'] + nodes[3]['x'])/2, y_center + 0.2, 'Signal u', ha='center', va='bottom', fontsize=9, style='italic')

    ax.annotate('', xy=(nodes[3]['x'] + 2.5, y_center), xytext=(nodes[3]['x'] + 1.2, y_center), arrowprops=arrow_props)
    ax.text(nodes[3]['x'] + 1.85, y_center + 0.2, 'Action a', ha='center', va='bottom', fontsize=9, style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig1_architecture.png"), bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, "fig1_architecture.pdf"), bbox_inches='tight')
    plt.close()

def draw_taxonomy_diagram():
    """Figure 2: RLCS Sensor Taxonomy Diagram"""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    center_x = 5
    center_y = 3
    
    ax.text(center_x, center_y, 'Latent\nRepresentation z', ha='center', va='center', 
            bbox=dict(boxstyle="circle,pad=0.5", facecolor='#ffffff', edgecolor='#333333', lw=2),
            fontweight='bold', fontsize=10)

    sensors = [
        {'x': 5, 'y': 5, 'label': 'Population Consistency\n(ResLik)', 'ref': 'Reference: Training Set Statistics', 'color': '#e1f5fe'},
        {'x': 1.5, 'y': 1.5, 'label': 'Temporal Consistency\n(TCS)', 'ref': 'Reference: Short-term History (t-1)', 'color': '#fff3e0'},
        {'x': 8.5, 'y': 1.5, 'label': 'Cross-View Consistency\n(Agreement)', 'ref': 'Reference: Peer Modality/Encoder', 'color': '#e8f5e9'},
    ]

    for s in sensors:
        rect = patches.FancyBboxPatch((s['x']-1.5, s['y']-0.6), 3, 1.2, boxstyle="round,pad=0.1", 
                                     facecolor=s['color'], edgecolor='#333333', lw=1.5)
        ax.add_patch(rect)
        ax.text(s['x'], s['y'] + 0.1, s['label'], ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(s['x'], s['y'] - 0.3, s['ref'], ha='center', va='center', fontsize=8, fontstyle='italic')
        ax.annotate('', xy=(s['x'], s['y'] if s['y'] > center_y else s['y']+0.6), 
                    xytext=(center_x, center_y),
                    arrowprops=dict(arrowstyle="<-", lw=1.5, color='#666666', ls='--'))

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig2_taxonomy.png"), bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, "fig2_taxonomy.pdf"), bbox_inches='tight')
    plt.close()

def plot_reslik_behavior():
    """Figure 3: ResLik Gating Function Behavior"""
    fig, ax = plt.subplots(figsize=(6, 4))
    discrepancy = np.linspace(0, 5, 200)
    scenarios = [
        {'lambda': 1.0, 'tau': 0.0, 'label': r'lambda=1.0, tau=0.0 (Strict)', 'color': '#1f77b4', 'ls': '-'},
        {'lambda': 1.0, 'tau': 1.0, 'label': r'lambda=1.0, tau=1.0 (Dead-zone)', 'color': '#2ca02c', 'ls': '--'},
        {'lambda': 2.0, 'tau': 1.0, 'label': r'lambda=2.0, tau=1.0 (Sharp)', 'color': '#d62728', 'ls': '-.'},
        {'lambda': 0.5, 'tau': 0.0, 'label': r'lambda=0.5, tau=0.0 (Loose)', 'color': '#9467bd', 'ls': ':'},
    ]
    for s in scenarios:
        eff_discrepancy = np.maximum(0, discrepancy - s['tau'])
        gate = np.exp(-s['lambda'] * eff_discrepancy)
        ax.plot(discrepancy, gate, label=s['label'], color=s['color'], linestyle=s['ls'])
    ax.set_xlabel('Normalized Discrepancy')
    ax.set_ylabel('Gate Value')
    ax.grid(True, linestyle=':', alpha=0.6, color='gray')
    ax.legend(fontsize=9, frameon=True, fancybox=False, edgecolor='gray')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig3_reslik_response.png"))
    plt.savefig(os.path.join(OUTPUT_DIR, "fig3_reslik_response.pdf"))
    plt.close()

def plot_multisensor_scenario():
    """Figure 4: Multi-Sensor Time Series (Drift vs Shock)"""
    t = np.arange(0, 50)
    reslik_sig = np.ones_like(t, dtype=float)
    reslik_sig[20:] = np.linspace(1.0, 0.2, 30)
    tcs_sig = np.ones_like(t, dtype=float)
    tcs_sig[40] = 0.1
    tcs_sig[41:] = 0.95
    agree_sig = np.ones_like(t, dtype=float)
    agree_sig[10:15] = 0.3
    fig, axs = plt.subplots(3, 1, figsize=(7, 6), sharex=True)
    c_reslik, c_tcs, c_agree = '#1f77b4', '#d62728', '#2ca02c'
    axs[0].plot(t, reslik_sig, color=c_reslik, label='ResLik (Population)')
    axs[0].axvline(x=20, color='gray', linestyle=':', alpha=0.8)
    axs[0].text(21, 0.3, 'Drift Starts', fontsize=9, color='#333333')
    axs[0].set_ylabel('Reliability')
    axs[0].set_ylim(0, 1.15)
    axs[0].legend(loc='lower left', fontsize=9, frameon=False)
    axs[0].grid(True, linestyle=':', alpha=0.5)
    axs[1].plot(t, tcs_sig, color=c_tcs, label='TCS (Temporal)')
    axs[1].axvline(x=40, color='gray', linestyle=':', alpha=0.8)
    axs[1].text(41, 0.3, 'Shock Event', fontsize=9, color='#333333')
    axs[1].set_ylabel('Consistency')
    axs[1].set_ylim(0, 1.15)
    axs[1].legend(loc='lower left', fontsize=9, frameon=False)
    axs[1].grid(True, linestyle=':', alpha=0.5)
    axs[2].plot(t, agree_sig, color=c_agree, label='Agreement (Cross-View)')
    axs[2].axvline(x=10, color='gray', linestyle=':', alpha=0.8)
    axs[2].text(11, 0.5, 'Sensor Conflict', fontsize=9, color='#333333')
    axs[2].set_ylabel('Similarity')
    axs[2].set_ylim(0, 1.15)
    axs[2].legend(loc='lower left', fontsize=9, frameon=False)
    axs[2].grid(True, linestyle=':', alpha=0.5)
    axs[2].set_xlabel('Time Step (t)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "fig4_multisensor.png"))
    plt.savefig(os.path.join(OUTPUT_DIR, "fig4_multisensor.pdf"))
    plt.close()

if __name__ == "__main__":
    ensure_dir()
    print("Generating Fig 1: Architecture...")
    draw_architecture_diagram()
    print("Generating Fig 2: Taxonomy...")
    draw_taxonomy_diagram()
    print("Generating Fig 3: ResLik Response...")
    plot_reslik_behavior()
    print("Generating Fig 4: Multi-Sensor...")
    plot_multisensor_scenario()
    print("Done.")
