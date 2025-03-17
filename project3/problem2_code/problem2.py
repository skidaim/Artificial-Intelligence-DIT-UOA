from csp import CSP, backtracking_search, mrv, forward_checking, min_conflicts

variables = ['Bed', 'Desk', 'Chair', 'Sofa']

furniture_dimensions = {
    'Bed': [(200, 100), (100, 200)],  # (l, w) for 0° and 90°
    'Desk': [(80, 160), (160, 80)],
    'Chair': [(44, 41), (41, 44)],
    'Sofa': [(103, 221), (221, 103)]
}

GRID_WIDTH = 300
GRID_LENGTH = 400

domains = {}
for var in variables:
    domains[var] = [(x, y, o) for x in range(GRID_WIDTH) for y in range(GRID_LENGTH) for o in range(2)]


neighbors = {
    'Bed': ['Desk', 'Chair', 'Sofa'],
    'Desk': ['Bed', 'Chair', 'Sofa'],
    'Chair': ['Bed', 'Desk', 'Sofa'],
    'Sofa': ['Bed', 'Desk', 'Chair'],
}

# Constraints
def constraints(F1, pos1, F2, pos2):
    (x1, y1, o1) = pos1
    (x2, y2, o2) = pos2

    l1, w1 = furniture_dimensions[F1][o1]  # w and l for F1's orientation
    l2, w2 = furniture_dimensions[F2][o2]  # w and l for F2's orientation

    if (x1+w1 > 300) or (y1+l1 > 400) or (x2+w2 > 300) or (y2+l2 > 400):
        return False

    # no furniture must be at the square of the door with height x width 100x100
    if not ((x1 > 100 or y1 > 100) and (x2 > 100 or y2 > 100)):
        return False
    # No overlap constraint (furniture must not overlap)
    if not ((x1 + w1 < x2 or x2 + w2 < x1) or (y1 + l1 < y2 or y2 + l2 < y1)):
            return False
        

    # bed must be attached to a wall
    if F1 == 'Bed':
        if not (x1 == 0 or x1 + w1   == 300 or y1 == 0 or y1 + l1 == 400):
            return False
    elif F2 == 'Bed':
        if not (x2 == 0 or x2 + w2 == 300 or y2 == 0 or y2 + l2 == 400):
            return False

    # desk must be attatched to a wall and illuminated by the window
    if F1 == 'Desk':
        if not (x1 + w1 == 300 or (y1 == 0 and x1 + w1 > 200)):
            return False
    elif F2 == 'Desk':
        if not (x2 == 0 or (y2 == 0 and x2 + w2 > 200)):
            return False

    return True

room_csp = CSP(variables, domains, neighbors, constraints)

mc_solution = min_conflicts(room_csp)

print("Min-Conflicts Solution:", mc_solution)

#visualize it

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_room(furniture_positions):

    room_width = 300
    room_length = 400
    
    furniture_dimensions = {
    'Bed': [(200, 100), (100, 200)],
    'Desk': [(80, 160), (160, 80)],
    'Chair': [(44, 41), (41, 44)],
    'Sofa': [(103, 221), (221, 103)]
    }
    
    fig, ax = plt.subplots(figsize=(8, 10))
    ax.set_xlim(0, room_width)
    ax.set_ylim(0, room_length)
    ax.set_aspect('equal')
    
    # Draw the room
    ax.add_patch(patches.Rectangle((0, 0), room_width, room_length, fill=None, edgecolor='black', linewidth=2))
    ax.text(250, 390, "Balcony Door", ha='center', fontsize=10, color='blue')
    ax.text(20, 20, "Room Door", ha='center', fontsize=10, color='blue')
    
    for furniture, (x, y, r) in furniture_positions.items():
        length, width = furniture_dimensions[furniture][r]
        rect = patches.Rectangle((x, y), width, length, edgecolor='red', facecolor='lightblue', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + width / 2, y + length / 2, furniture, ha='center', va='center', fontsize=8, color='black')
    
    ax.set_title("Room Layout with Furniture")
    ax.set_xlabel("Width (cm)")
    ax.set_ylabel("Length (cm)")
    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    plt.show()

furniture_positions = mc_solution
visualize_room(furniture_positions)
