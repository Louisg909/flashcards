
class Queue:
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        self.front = None
        self.back = None
        self.length = 0

    def isEmpty(self):
        return self.front == None

    def peak(self):
        return self.front.value

    def enqueue(self, data):
        self.length += 1
        new = Queue.Node(data)
        if self.front == None:
            self.front = new
            self.back = self.front
        else:
            self.back.next = new
            self.back = new

    def dequeue(self):
        self.length -= 1
        data = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.back is None
        return data

    def __repr__(self):
        def regress(node):
            if node.next == None:
                return f'{node.value}]'
            else:
                string = regress(node.next)
                return f'{node.value}, {string}'
        string = regress(self.front)
        return f'[{string}'
        


if __name__ == '__main__':
    cheese = Queue()
    poop = [234,25,1,25,6,3,42]
    cheese.enqueue('I was first')
    [cheese.enqueue(n) for n in poop]
    cheese.enqueue(12)
    cheese.enqueue(10)
    cheese.enqueue(16)
    print(cheese)
    cheese.enqueue('Hi guys')
    print(cheese)
    value = cheese.dequeue()
    print(value)
    print(cheese)



