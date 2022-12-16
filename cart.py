data = []
features = [i for i in range(11)]
alphas = []
q = []


class Node:
    def __init__(self, element=None, parent=None, left=None, right=None):
        self.element = element
        self.parent = parent
        self.left = left
        self.right = right


class LBTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def find_root(self):
        return self.root

    def left(self, p):
        return p.left

    def right(self, p):
        return p.right

    def parent(self, p):
        return p.parent

    def num_child(self, p):
        num = 0
        if p.left != None:
            num += 1
        if p.right != None:
            num += 1
        return num

    def add_root(self, e):
        if self.root != None:
            print('The root already exists!')
        else:
            self.size = 1
            self.root = Node(e)
            return self.root

    def add_left(self, p, e):
        if p.left != None:
            print('The left child already exists!')
        else:
            self.size += 1
            p.left = Node(e, p)
            return p.left

    def add_right(self, p, e):
        if p.right != None:
            print('The right child already exists!')
        else:
            self.size += 1
            p.right = Node(e, p)
            return p.right

    def replace(self, p, e):
        old = p.element
        p.element = e
        return old

    def delete(self, p):
        if p.parent.left == p:
            p.parent.left = None
        if p.parent.right == p:
            p.parent.right = None
        return p.element


def get_data(file, length):
    # get and deal with the data
    global data
    with open(file) as f:
        for i in range(length-1):
            r = f.readline()
            x = r.split(', ')
            x[-1] = x[-1][:-1]
            data.append(x)
        r = f.readline()
        x = r.split(', ')
        data.append(x)
    data.pop(0)


def divide_point(sub_data, feature_n):  # feature 0, feature 1...
    # find the point used to divide data sets for feature_n
    # also return the corresponding conditional gini
    d1 = 0
    d2 = 0
    cd1 = 0
    cd2 = 0
    gini = 10000
    point = None
    left_gini = None
    right_gini = None
    sub_d = len(sub_data)
    for i in range(sub_d):
        n = float(sub_data[i][feature_n])
        for j in range(sub_d):
            if float(sub_data[j][feature_n]) <= n:
                d1 += 1
                if int(sub_data[j][-1]) > 6:
                    cd1 += 1
            else:
                d2 += 1
                if int(sub_data[j][-1]) > 6:
                    cd2 += 1
        if d1 == 0 or d2 == 0:
            continue
        gini_d1 = 1-cd1**2/d1**2-(d1-cd1)**2/d1**2
        gini_d2 = 1-cd2**2/d2**2-(d2-cd2)**2/d2**2
        new_gini = d1/sub_d*gini_d1+d2/sub_d*gini_d2
        if new_gini < gini:
            gini = new_gini
            point = n
            left_gini = gini_d1
            right_gini = gini_d2
    return point, gini, left_gini, right_gini, new_gini


def divide_with_feature(data_set):
    # find the specific feature used to divide the data set
    # also return the subsets
    g = 10000
    p = None
    feature = None
    D1 = []
    D2 = []
    left_gini = None
    right_gini = None
    if len(features) > 1:
        for i in features:
            point, gini, gini_d1, gini_d2, new_gini = divide_point(data_set, i)
            if gini < g:
                g = gini
                p = point
                feature = i
                left_gini = gini_d1
                right_gini = gini_d2
    else:
        feature = features[0]
        p, gini, left_gini, right_gini = divide_point(data_set, feature)
    if gini <= 0.45:
        for j in data_set:
            if float(j[feature]) <= p:
                D1.append(j)
            else:
                D2.append(j)

        return feature, p, D1, D2, left_gini, right_gini, new_gini
    else:
        return False, False, False, False, False, False,False


def root_gini():
    c1 = 0
    for d in data:
        if int(d[-1]) <= 6:
            c1 += 1
    part = c1/len(data)
    root_gini = 1-part**2-(1-part)**2
    return root_gini


def create_tree():
    # create a tree and set the tree root
    global t0, features
    t0 = LBTree()
    feature, p, D1, D2, left_gini, right_gini = divide_with_feature(data)
    t0.add_root([feature, len(data), root_gini(), p])
    features.remove(feature)
    return D1, D2, left_gini, right_gini


def if_leaf(data_set):
    # check how many datas in each class
    c1 = 0
    for d in data_set:
        if int(d[-1]) > 6:
            c1 += 1
    return c1


def create_node(parent, left_or_right, result):
    # create the tree nodes except its root
    global t0
    if left_or_right == 'left':
        t0.add_left(parent, result)
    else:
        t0.add_right(parent, result)


def create_bunch(data_set, parent, left_or_right, initial_gini):
    # decide the tree nodes except its root
    global features
    feature = None
    # decide when to create a leaf node
    c1 = if_leaf(data_set)
    c2 = len(data_set)-c1
    if c1 != 0 and c2 != 0 and features != []:
        feature, p, D1, D2, left_gini, right_gini, new_gini = divide_with_feature(
            data_set)
    if c1 == 0 or c2 == 0 or features == [] or feature == False:
        if c2 < c1:
            result = Trueaz
        else:
            result = False
        create_node(parent, left_or_right, [
                    result, len(data_set), initial_gini])
        return

    features.remove(feature)
    create_node(parent, left_or_right, [
                feature, len(data_set), initial_gini, p])
    if left_or_right == 'left':
        child = parent.left
    else:
        child = parent.right
    create_bunch(D1, child, 'left', left_gini)
    create_bunch(D2, child, 'right', right_gini)
    features.append(feature)


def create_CT():
    # Creating the whole classification tree
    get_data('train.csv', 1120)
    D1, D2, left_gini, right_gini = create_tree()
    create_bunch(D1, t0.root, 'left', left_gini)
    create_bunch(D2, t0.root, 'right', right_gini)


def DFSearchLeaf(t):
    global CTt, Tt, sub_data_num
    if t:
        if t.left == None and t.right == None:
            CTt += t.element[1]*t.element[2]
            Tt += 1
            sub_data_num += t.element[1]
        DFSearchLeaf(t.left)
        DFSearchLeaf(t.right)


# def alpha(node):
#     global CTt
#     global Tt
#     global a
#     global sub_data_num
#     CTt = 0
#     Tt = 0
#     sub_data_num = 0
#     if node.left == None and node.right == None:
#         return
#     DFSearchLeaf(node)
#     CTt = CTt/sub_data_num
#     a = (node.element[2]-CTt)/(Tt-1)
#     node.element.append(a)
#     alphas.append(a)
#     alpha(node.left)
#     alpha(node.right)


# def prune():
#     global alphas, q, CTt, ctt
#     CTt = 0
#     alphas.sort()
#     DFSearchLeaf(t0.root)
#     ctt = CTt/len(data)
#     for i in range(len(alphas)):
#         q = []
#         BFSearch(t0.root, i)


# def BFSearch(t, i):
#     global q, CTt, Tt, ctt
#     if t.element[-1] == alphas[i]:
#         left = t.left
#         right = t.right
#         t.left = None
#         t.right = None
#         CTt = 0
#         DFSearchLeaf(t0.root)
#         CTt = CTt/len(data)
#         print('complete CTt', CTt)
#         if CTt/ctt > 0.9:
#             t.left = left
#             t.right = right
#             print(t.left, t.right)
#         else:
#             ctt = CTt
#         print('ctt', ctt)
#         return
#     if t.left != None:
#         q.append(t.left)
#     if t.right != None:
#         q.append(t.right)
#     if len(q) != 0:
#         BFSearch(q.pop(0), i)


def test_CT():
    # use the test data to get the accuracy rate
    global data
    correct = 0
    data = []
    get_data('test.csv', 481)
    for d in data:
        if predict(t0.root, d):
            correct = correct+1
    accuracy = correct/len(data)
    return accuracy


def predict(node, d):
    # predict the class of the data d and return whether the result is right or not
    if node.left == None and node.right == None:
        if (int(d[-1]) > 6 and node.element[0]) or (int(d[-1]) <= 6 and node.element[0] == False):
            return True
        else:
            return False

    if float(d[node.element[0]]) <= node.element[-2]:
        return predict(node.left, d)
    else:
        return predict(node.right, d)


def DFSearch(t):
    if t:
        print(t)
        DFSearch(t.left)
        DFSearch(t.right)


if __name__ == "__main__":
    create_CT()
    alpha(t0.root)
    prune()
    print(test_CT())
    print(len(alphas))
