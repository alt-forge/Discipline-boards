import matplotlib.pyplot as plt

def view_table(filename, output_filename):
    with open(filename, 'r') as file:
        content = file.read().strip()
    
    color_map = {
        'R': 'red',
        'G': 'green', 
        'Y': 'yellow',
        'W': 'white'
    }
    
    rows = []
    current_row = []
    
    for char in content.upper():
        if char == 'W':
            break
        if char in color_map:
            current_row.append(char)
            if len(current_row) == 7:
                rows.append(current_row)
                current_row = []
    
    if current_row:
        while len(current_row) < 7:
            current_row.append('')
        rows.append(current_row)
    
    n_rows = len(rows)
    if n_rows == 0:
        print("Нет данных для отображения")
        return

    cell_size = 0.7
    font_size = 8
    
    fig, ax = plt.subplots(figsize=(7*cell_size, n_rows*cell_size))
    
    ax.set_xlim(0, 7)
    ax.set_ylim(0, n_rows)
    ax.set_aspect('equal')
    ax.axis('off')
    
    cell_number = 1
    
    for i, row in enumerate(rows):
        for j, char in enumerate(row):
            if char:
                color = color_map.get(char, 'white')
                
                rect = plt.Rectangle((j, n_rows-i-1), 1, 1, 
                                    facecolor=color, 
                                    edgecolor='black',
                                    linewidth=1)
                ax.add_patch(rect)
                
                ax.text(j + 0.1, n_rows-i-1 + 0.1, str(cell_number),
                       fontsize=font_size,
                       fontweight='bold',
                       color='black',
                       ha='left',
                       va='bottom')
                
                cell_number += 1
            else:
                cell_number += 1
    
    for i in range(n_rows + 1):
        ax.axhline(y=i, color='black', linewidth=0.5)
    for j in range(8):
        ax.axvline(x=j, color='black', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')

