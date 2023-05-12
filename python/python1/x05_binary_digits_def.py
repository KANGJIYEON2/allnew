def binary():
    input_num = int(input("input binary num: "))
    binary_list = []
    for x in range(4, 16):
        if x % 2 != 0:
            binary_list.append(1)
        else:
            binary_list.append(0)
    return binary_list

print(binary())
