# Function to generate all binary strings of size n. Example, n ==5, 00000, 00001....

def generate_binary_strings(n):
    array = []
    def helper(n, slate, array):
        if n == 0:
            array.append(slate)
        else:
            helper(n-1, slate + '0', array)
            helper(n-1, slate + '1', array)
    helper(n, "", array)
    return array


print(generate_binary_strings(5))
      