def tower_of_hanoi(n):
    solution = []
    def helper(n, src, dest, aux):
        if n == 1:
            # print(f"Move disk from {src} to {dest}")
            solution.append([src, dest])
            return
        else:
            helper(n-1, src, aux, dest)
            # print(f"Move disk from {src} to {dest}")
            solution.append([src, dest])
            helper(n-1, aux, dest, src)
    helper(n, 1, 2, 3)
    return solution
print(tower_of_hanoi(3))
