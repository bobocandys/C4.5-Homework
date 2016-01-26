from __future__ import division
from math import log

class Tree:
    leaf = True
    prediction = None
    feature = None
    threshold = None
    left = None
    right = None

def predict(tree, point):
    if tree.leaf:
        #print str(tree.prediction)
        return tree.prediction
    i = tree.feature
    if (point.values[i] < tree.threshold):
        return predict(tree.left, point)
    else:
        return predict(tree.right, point)

def most_likely_class(prediction):
    labels = list(prediction.keys())
    probs = list(prediction.values())
    return labels[probs.index(max(probs))]

def accuracy(data, predictions):
    total = 0
    correct = 0
    for i in range(len(data)):
        point = data[i]
        pred = predictions[i]
        total += 1
        guess = most_likely_class(pred)
        if guess == point.label:
            correct += 1
    return float(correct) / total

def split_data(data, feature, threshold):
    left = []
    right = []
    # TODO: split data into left and right by given feature.
    # left should contain points whose values are less than threshold
    # right should contain points with values greater than or equal to threshold
    for point in data:
        if  point.values[feature] < threshold:
        	left.append(point)
        else:
        	right.append(point)
    return (left, right)

def count_labels(data):
    counts = {}
    # TODO: counts should count the labels in data
    # e.g. counts = {'spam': 10, 'ham': 4}
    for point in data:
        if point.label in counts:
            preCount = counts.get(point.label)
            counts[point.label] = preCount + 1
        else:
            counts[point.label] = 1
    return counts

def counts_to_entropy(counts):
    entropy = 0.0
    # TODO: should convert a dictionary of counts into entropy
    totalCount = 0
    for v in counts.itervalues():
        totalCount += v

    for v in counts.itervalues():
        if v != 0 and totalCount != 0:
            prob = v / totalCount
            entropy = entropy - (prob * log(prob, 2))
    return entropy

def get_entropy(data):
    counts = count_labels(data)
    entropy = counts_to_entropy(counts)
    return entropy

# This is a correct but inefficient way to find the best threshold to maximize
# information gain.
def find_best_threshold(data, feature):
    entropy = get_entropy(data)
    best_gain = 0
    best_threshold = None
    for point in data:
        left, right = split_data(data, feature, point.values[feature])
        curr = (get_entropy(left)*len(left) + get_entropy(right)*len(right))/len(data)
        gain = entropy - curr
        if gain > best_gain:
            best_gain = gain
            best_threshold = point.values[feature]
    return (best_gain, best_threshold)

def find_best_threshold_fast(data, feature):
    entropy = get_entropy(data)
    best_gain = 0
    best_threshold = None
    # TODO: Write a more efficient method to find the best threshold.
    sortedData = sorted(data, key=lambda x: x.values[feature])

    countsRight = count_labels(sortedData)
    countsLeft = {}
    for k, v in countsRight.iteritems():
        countsLeft[k] = 0

    curr = (counts_to_entropy(countsLeft)*getTotal(countsLeft) + counts_to_entropy(countsRight)*getTotal(countsRight))/len(sortedData)
    best_gain = entropy - curr
    best_threshold = sortedData[0].values[feature]
    index = 1

    # threshold is at index
    while index < len(sortedData):
        prevValue = sortedData[index - 1].values[feature]
        curThreshold = sortedData[index].values[feature]
        ptLabel = sortedData[index - 1].label
        countsLeft[ptLabel] += 1
        countsRight[ptLabel] -= 1
        if prevValue < curThreshold:
            curr = (counts_to_entropy(countsLeft)*getTotal(countsLeft) + counts_to_entropy(countsRight)*getTotal(countsRight))/len(sortedData)
            gain = entropy - curr
            if gain > best_gain:
                best_gain = gain
                best_threshold = curThreshold

        index += 1
    return (best_gain, best_threshold)

def getTotal(rollingCount):
    total = 0
    for v in rollingCount.itervalues():
        total += v
    return total

def find_best_split(data):
    if len(data) < 2:
        return None, None
    best_feature = None
    best_threshold = None
    best_gain = 0

    # TODO: find the feature and threshold that maximize information gain.
    #print "size " + str(len(data[0].values))
    for feature in range(len(data[0].values)):
        gain, threshold = find_best_threshold_fast(data, feature)
        #print "gain " + str(gain)
        #print "threshold" + str(threshold)
        if gain > best_gain:
            best_gain = gain
            best_feature = feature
            best_threshold = threshold
    return (best_feature, best_threshold)

def make_leaf(data):
    tree = Tree()
    counts = count_labels(data)
    prediction = {}
    for label in counts:
        prediction[label] = float(counts[label])/len(data)
    tree.prediction = prediction
    return tree

def c45(data, max_levels):
    if max_levels <= 0:
        #print "000000000"
        return make_leaf(data)
    # TODO: Construct a decision tree with the data and return it.
    # Your algorithm should return a leaf if the maximum level depth is reached
    # or if there is no split that gains information, otherwise it should greedily
    # choose an feature and threshold to split on and recurse on both partitions
    # of the data.
    if isAllSame(data):
        return make_leaf(data)
    else:
        feature, threshold = find_best_split(data)
        print "picked feature " + str(feature)
        print "picked threshold " + str(threshold)
        print "data size " + str(len(data))
        if (feature == None) or (threshold == None):
            return make_leaf(data)
        else:
            left, right = split_data(data, feature, threshold)
            root = Tree()
            root.leaf = False
            root.feature = feature
            root.threshold = threshold
            print "left size " + str(len(left))
            print "right size " + str(len(right))
            root.right = c45(right, max_levels - 1)
            root.left = c45(left, max_levels - 1)
        return root

def isAllSame(data):
    for index in range(len(data) - 1):
        if data[0].label != data[index + 1].label:
            return False
    return True

def submission(train, test):
    # TODO: Once your tests pass, make your submission as good as you can!
    tree = c45(train, 4)
    predictions = []

    print_tree(tree)

    for point in test:
        predictions.append(predict(tree, point))
    return predictions

# This might be useful for debugging.
def print_tree(tree):
    if tree.leaf:
        print "Leaf", tree.prediction
    else:
        print "Branch", tree.feature, tree.threshold
        print_tree(tree.left)
        print_tree(tree.right)
