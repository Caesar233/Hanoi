class Stack():
    def __init__(self, size):
        self.size = size
        self.stack = []
        self.top = -1

    # 返回元素在栈中的位置
    def location(self, ele):
        temp = Stack(self.size)
        find = False # 是否找到
        num = -1 # 找不到返回-1
        while not self.isempty():
            disk = self.pop()
            temp.push(disk)
            if disk == ele:
                find = True # 找到将find设为true
            if True == find:
                num += 1 # 找到后开始计数

        while not temp.isempty():
            # 将栈内元素归位
            self.push(temp.pop())

        return num

    def push(self, ele):  # 入栈之前检查栈是否已满
        if self.isfull():
            raise Exception("out of range")
        else:
            self.stack.append(ele)
            self.top = self.top + 1

    def pop(self):  # 出栈之前检查栈是否为空
        if self.isempty():
            raise Exception("stack is empty")
        else:
            self.top = self.top - 1
            return self.stack.pop()

    def isfull(self):
        return self.top + 1 == self.size

    def isempty(self):
        return self.top == -1

s = Stack(20)
for i in range(11):
    s.push(i)
print(s.location(8))
s.pop()
print(s.isempty())