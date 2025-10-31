#!/usr/bin/env python3
"""
Meta meme: "Is this a butterfly?" template re-imagined minimally
Captioned to hit the metaphysical angle.

Output: meta_meme_prediction_is_intervention.png/.pdf
"""
import matplotlib.pyplot as plt


def main():
    plt.rcParams['figure.dpi'] = 300
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor('white')

    # Minimal meme layout
    ax.text(1.0, 8.5, 'builder', fontsize=18, fontweight='bold')
    ax.text(6.2, 8.5, 'reverse oracle', fontsize=18, fontweight='bold')

    # Dialogue
    ax.text(1.0, 6.0, '“Is this a prediction?”', fontsize=16)
    ax.text(6.2, 4.8, '“It draws on the map.”', fontsize=16)

    # Bottom caption
    ax.text(5.0, 1.2, 'prediction IS intervention', ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(5.0, 0.5, 'Greenhouse & Company — Dark intelligence research for crypto', ha='center', va='center', fontsize=10, color='#6b6b6b')

    plt.tight_layout()
    plt.savefig('meta_meme_prediction_is_intervention.png', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    plt.savefig('meta_meme_prediction_is_intervention.pdf', bbox_inches='tight', facecolor='white', pad_inches=0.2)
    print('✅ Generated meta_meme_prediction_is_intervention.[png|pdf]')


if __name__ == '__main__':
    main()


