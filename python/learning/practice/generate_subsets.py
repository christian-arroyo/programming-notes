def generate_subsets(input_nums: list[int], index_subproblem: int, partial_solution: list[int]):
    if index_subproblem == len(input_nums):
        print(partial_solution)
        return
    # Recursive step (internal node worker)
    # Include
    partial_solution.append(input_nums[index_subproblem])
    generate_subsets(input_nums, index_subproblem + 1, partial_solution)
    partial_solution.pop()
    # Exclude
    generate_subsets(input_nums, index_subproblem + 1, partial_solution)

input_nums = [1,2,3]
generate_subsets(input_nums, 0, [])
