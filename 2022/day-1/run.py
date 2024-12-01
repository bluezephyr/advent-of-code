def create_elf_list(filename):
    with open(filename, encoding='utf-8') as f:
        elves = []
        elf = []
        for line in f:
            value = line.strip()
            if value != "":
                elf.append(int(value))
            else:
                elves.append(sum(elf))
                elf = []
        elves.append(sum(elf))
        enumeration = [(index, value) for index, value in enumerate(elves)]
        enumeration.sort(key=lambda x: x[1], reverse=True)
        return enumeration


if __name__ == '__main__':
    elves = create_elf_list("input.txt")
    max_elf = elves[0]
    print(elves)
    print(f"Elf {max_elf[0]+1} is carrying {max_elf[1]} Calories")
    print(f"Answer 1: {max_elf[1]}")

    top_3_sum = 0
    for i in range(3):
        top_3_sum += elves[i][1]
    print(f"Answer 2: {top_3_sum}")
