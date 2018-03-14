from graphviz_generator import GraphvizGenerator

cfg = []
ht = {}

class Token:
    def __init__(self, val, is_term):
        self.val = val
        self.is_term = is_term
    
    def __eq__(self, other):
        return (self.val, self.is_term) == (other.val, other.is_term)
    
    def __hash__(self):
        return hash((self.val, self.is_term))
    

class Production:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return self.left.val + '->' + ''.join(map(lambda x:x.val, self.right))


class Item:
    def __init__(self, pid, pos=0):
        self.pid = pid
        self.pos = pos
        self.prod = cfg[pid]
    
    def next_token(self):
        prod = cfg[self.pid]
        if self.pos < len(prod.right):
            return prod.right[self.pos]
        else:
            return None

    def __hash__(self):
        return hash((self.pid, self.pos))

    def __eq__(self, other):
        return (self.pid, self.pos) == (other.pid, other.pos)
    
    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        r = list(map(lambda x: x.val, self.prod.right))
        r.insert(self.pos, '.')
        return '('+str(self.pid)+') ' + self.prod.left.val + ' -> ' + ''.join(r)

class State:
    def __init__(self, root):
        # root should be tuple
        self.root = root
        self.items = self.closure()
    
    def go_to(self, token):
        j = set()
        for item in self.items:
            if item.next_token() and item.next_token() == token:
                j.add(Item(item.pid, item.pos + 1))
        if not j:
            return None
        return State(tuple(j))
    
    def closure(self):
        res = set()
        res |= set(self.root)
        while True:
            addon = set()
            for item in res:
                if item.next_token() and not item.next_token().is_term:
                    for p in ht[item.next_token()]:
                        if Item(p) not in res:
                            addon.add(Item(p))
            if not addon:
                break
            else:
                res |= addon
        return res
    
    def __hash__(self):
        return hash(self.root)
    
    def __eq__(self, other):
        return True
    
    def __ne__(self, other):
        return False


def generate():
    states = {State((Item(0),))}
    while True:
        addon = set()
        for state in states:
            for item in state.items:
                new_state = state.go_to(item.next_token())
                if new_state and new_state not in states:
                    addon.add(new_state)
        if not addon:
            break
        else:
            states |= addon
    return states
    
def main():
    fs = Token('S\'', False)
    s = Token('S', False)
    d = Token('$', True)
    lp = Token('(', True)
    rp = Token(')', True)
    l = Token('L', False)
    x = Token('x', True)
    colon = Token(',', True)

    cfg.append(Production(fs, [s, d]))
    cfg.append(Production(s, [lp,l,rp]))
    cfg.append(Production(s, [x]))
    cfg.append(Production(l, [s]))
    cfg.append(Production(l, [l, colon, s]))

    ht[fs] = [0]
    ht[s] = [1,2]
    ht[l] = [3,4]    
    GraphvizGenerator.generate(generate())


main()