# Given two integers n and k, find all the possible unique combinations of k numbers in range 1 to n

def combinations(n: int, k: list) -> list:
    solution = []
    def backtrack(start, current_combination):
        # if current combination equals height of tree
        if len(current_combination) == k:
            # Add a copy, not a referance to the object that will be modified in other iterations
            solution.append(current_combination.copy())
            return
        for i in range(start, n+1):
            current_combination.append(i)
            backtrack(i+1, current_combination)
            # remove last number added because it is placed in solution after hitting base case
            # output will be [1,2],[1,3],[1,4],[2,3],2[4],[3,4] for n=4,k=2
            current_combination.pop()
    backtrack(1, [])
    return solution

print(combinations(4, 2))
