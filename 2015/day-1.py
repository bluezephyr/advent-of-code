
with open("input-day-1", encoding = 'utf-8') as f:
    for line in f:
        left = line.count('(')
        right = line.count(')')
    print(f"{left} (, {right} ) --> {left - right} floors")
