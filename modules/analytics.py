def analytics(filename):
    with open(filename, 'r') as file:
        content = file.read().strip().upper()

    counts = {
        'R': 0,
        'G': 0,
        'Y': 0
    }
    
    for char in content:
        if char in counts:
            counts[char] += 1
        elif char == 'W':
            break
    
    result = f"R: {counts['R']}, G: {counts['G']}, Y: {counts['Y']}"
    return result
