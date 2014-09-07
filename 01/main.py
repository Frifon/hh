"""
    The complexity of this algorithm is O(N * log(2, N)),
    where N is the number of rectangles.
    This algorithm uses such ideas as a segment tree with lazy propagation,
    scan-line and coordinate compression.
"""


def main():
    fin = open('input.txt', 'r')
    fout = open('output.txt', 'w')

    class node:
        def __init__(self):
            self.min = 0
            self.cnt = 1
            self.add = 0

    class SegmentTree:

        def __init__(self, x_set):
            t = len(x_set)
            self.pw = 1
            while self.pw < t:
                self.pw *= 2
            self.T = [node() for i in range(self.pw * 2)]
            for i in range(self.pw, self.pw * 2):
                if i - self.pw < t - 1:
                    self.T[i].cnt = x_set[i - self.pw + 1] - x_set[i - self.pw]
                if i - self.pw >= t:
                    x_set.append(x_set[-1] + 1)
            self.len = x_set[-1] - x_set[0] + 1
            for i in range(self.pw - 1, 0, -1):
                self.T[i].cnt = self.T[i * 2].cnt + self.T[i * 2 + 1].cnt

        def push(self, v):
            if v < self.pw:
                self.T[v * 2].add += self.T[v].add
                self.T[v * 2 + 1].add += self.T[v].add
                self.T[v].add = 0

        def get_min(self, v):
            return self.T[v].min + self.T[v].add

        def update(self, v, tl, tr, l, r, add):
            if tl > r or tr < l or l > r:
                return
            if l <= tl <= tr <= r:
                self.T[v].add += add
            else:
                self.push(v)
                tm = (tl + tr) // 2
                self.update(v * 2, tl, tm, l, r, add)
                self.update(v * 2 + 1, tm + 1, tr, l, r, add)
                Min = min(self.get_min(v * 2), self.get_min(v * 2 + 1))
                self.T[v].min = Min
                self.T[v].cnt = 0
                if Min == self.get_min(v * 2):
                    self.T[v].cnt += self.T[v * 2].cnt
                if Min == self.get_min(v * 2 + 1):
                    self.T[v].cnt += self.T[v * 2 + 1].cnt

        def get_ans(self):
            return self.len - self.T[1].cnt if self.get_min(1) == 0 else 0

    def get_num(x):
        l = 0
        r = len(x_set)
        while (r - l > 1):
            m = (l + r) // 2
            if x_set[m] <= x:
                l = m
            else:
                r = m
        return l

    x_set = set()

    Rect = fin.readlines()
    for i in range(len(Rect)):
        Rect[i] = list(map(int, Rect[i].split()))
        x_set.add(Rect[i][0])
        x_set.add(Rect[i][2])

    if len(Rect) == 0:
        fout.write('0')
    else:
        ScanLine = []
        for x1, y1, x2, y2 in Rect:
            ScanLine.append([y1, 0, x1, x2])
            ScanLine.append([y2, 1, x1, x2])
        ScanLine.sort()
        x_set = sorted(list(x_set))
        tree = SegmentTree(x_set)
        last_y = ScanLine[0][0]
        ans = 0
        for y, Type, x1, x2 in ScanLine:
            ans += tree.get_ans() * (y - last_y)
            add = 1 if Type == 0 else -1
            tree.update(1, 0, tree.pw - 1, get_num(x1), get_num(x2) - 1, add)
            last_y = y
        fout.write(str(ans))

    fin.close()
    fout.close()

main()
