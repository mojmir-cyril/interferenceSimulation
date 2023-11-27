import matplotlib.pyplot as plt
import numpy as np

def create_non_overlapping_circles_image(width, height, num_circles, output_path, min_circle_offset):
    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
    fig.set_facecolor('black')  # nastavení černého pozadí pro celý obrázek
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('black')  # nastavení černého pozadí pro osu

    circle_radii = np.random.uniform(5, 50, num_circles)

    for radius in circle_radii:
        while True:
            circle_x = np.random.uniform(radius, width - radius)
            circle_y = np.random.uniform(radius, height - radius)
            # Kontrola, zda se nový kruh nepřekrývá s již existujícími kruhy
            overlap = any(np.linalg.norm([circle_x - x, circle_y - y]) < radius + existing_radius + min_circle_offset
                          for x, y, existing_radius in zip(circle_xs, circle_ys, circle_radii))
            if not overlap:
                break

        circle_xs.append(circle_x)
        circle_ys.append(circle_y)
        circle_color = 'lightgray'  # šedá barva kruhu

        circle = plt.Circle((circle_x, circle_y), radius, color=circle_color, edgecolor='black')
        ax.add_patch(circle)

    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.show()


# Nastavte parametry podle potřeby
width = 1024
height = 768
num_circles = 70
output_path = r"random_circles_image_matplotlib.png"
min_circle_offset = 10

circle_xs = []
circle_ys = []

create_non_overlapping_circles_image(width, height, num_circles, output_path, min_circle_offset)
