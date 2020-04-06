class MyArray:
    def __init__(self):
        self.length = 0
        self.data = {}

    def get(self, index):
        return self.data[index]

    def push(self, item):
        self.data[self.length] = item
        self.length += 1

    def pop(self):
        last_item = self.data[self.length - 1]
        del self.data[self.length - 1]
        self.length -= 1
        return last_item

    def delete(self, index):
        self.shift_items(index)

    def shift_items(self, index):
        while(index < self.length -1):
            self.data[index] = self.data[index+1]
            index += 1
        # delete last element
        del self.data[self.length -1]


a1 = MyArray()
a1.push('hi')
a1.push('there')
a1.push('friend')
print(a1.data)
print(a1.delete(2))
print(a1.data)
print(a1.length)
