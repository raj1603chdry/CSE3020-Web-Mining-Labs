import math

class Node:
    def __init__(self, name):
        self.name = name
        self.label = None
        self.decisionAttr = None
        self.decisionGain = None
        self.decisionValue = None
        self.branches = []

    def printTree(self):
        self.printTreeRecurse(0)

    def printTreeRecurse(self, level):
        print ('\t' * level + self.name),
        if self.decisionAttr and self.decisionGain:
            print ('split by ' + str(self.decisionAttr) + ' for a gain of ' + str(self.decisionGain)),
        if self.label:
            print (' ' + self.label),
        #print ('\n'),
        level += 1
        for branch in self.branches:
            branch.printTreeRecurse(level)

    def predictOutcome(self, cases, a):
        predictions = []
        for c in cases:
            outcome = self.predictOutcomeRecurse(c, attributes)
            predictions.append(outcome)
        return predictions

    def predictOutcomeRecurse(self, case, a):
        if self.name == '':

            # Leaf nodes
            if self.label == '+':
                return 'Yes'
            elif self.label == '-':
                return 'No'

        index = a.index(self.decisionAttr)

        if self.decisionValue == case[index]:
            return self.branches[0].predictOutcomeRecurse(case, a)

        if self.decisionGain:
            # Traverse to the branch where branch.decisionValue is in the case
            for b in self.branches:
                if b.decisionValue == case[index]:
                    return b.predictOutcomeRecurse(case, a)


# Returns the root node of the constructed decision tree
def constructDecisionTree(examples, targetAttribute, attributes):
    root = Node('')

    # Examples are all positive
    # The last attribute in the example is

    if all(isPositive(example[-1]) for example in examples):
        root.label = '+'
        return root

    # Examples are all negative
    elif all(not isPositive(example[-1]) for example in examples):
        root.label = '-'
        return root

    # Attributes is empty
    elif not attributes:
        root.label = getMostCommonLabel(examples)
        return root
    else:
        result = getHighestInfoGainAttr(attributes, examples)
        attr = result[0]
        gain = result[1]
        attrIndex = result[2]

        root.decisionAttr = attr
        root.decisionGain = gain

        possibleValues = uniqueValues(attrIndex, examples)

        for value in possibleValues:
            newBranch = Node(attr + ' = ' + value)
            newBranch.decisionAttr = attr
            newBranch.decisionValue = value
            root.branches.append(newBranch)
            branchExamples = sorted(row for row in examples if row[attrIndex] == value)

            if not branchExamples:
                leaf = Node(getMostCommonValue(targetAttribute, examples, possibleValues))
                newBranch.branches.append(leaf)
            else:
                newExamples = []
                for example in branchExamples:
                    newExample = []
                    for i in range(len(example)):
                        if not i == attrIndex:
                            newExample.append(example[i])
                    newExamples.append(newExample)

                newBranch.branches.append(constructDecisionTree(newExamples, targetAttribute, [a for a in attributes if not a == attr]))

    return root


# Determines whether a word is positive ('yes', 'true', etc.)
def isPositive(word):
    word = word.lower()
    return word == 'yes' or word == 'true' or word == 'y' or word == 't'


# Returns the most common label (+ or -) in the given list of nodes
def getMostCommonLabel(nodes):
    pCount = 0
    nCount = 0

    for node in nodes:
        if node.label == '+':
            pCount += 1
        elif node.label == '-':
            nCount += 1

    if pCount >= nCount:
        return '+'
    else:
        return '-'


# Returns the attribute with the highest information gain, as well as the info gain value
def getHighestInfoGainAttr(attributes, examples):
    totalRows = len(examples)
    # Divide examples into positive and negative
    posExamples = sorted(row for row in examples if isPositive(row[-1]))
    negExamples = sorted(row for row in examples if not isPositive(row[-1]))

    # Get the expected info needed for the entire data set
    allExpectedInfo = computeExpectedInfo(len(posExamples), len(negExamples))

    valuesGain = []

    # Compute the entropy & gain of each attribute
    for i, attr in enumerate(attributes):

        # Don't check the target attribute
        if attributes[-1] == attributes[i]:
            break

        values = uniqueValues(i, examples)

        # Lists for the expected info & probability of each value
        valuesExpectedInfo = []
        valuesProbability = []

        # Compute the expected info needed for each value
        for value in values:
            # Count how many positive & negative examples there are for the value
            posExamplesOfValue = sorted(row for row in posExamples if row[i]==value)
            negExamplesOfValue = sorted(row for row in negExamples if row[i]==value)
            numPos = len(posExamplesOfValue)
            numNeg = len(negExamplesOfValue)
            # Compute the expected info & probability of the value & add them to the lists
            valueExpectedInfo = computeExpectedInfo(numPos, numNeg)
            valueProbability = float(numPos + numNeg) / float(totalRows)
            valuesExpectedInfo.append(valueExpectedInfo)
            valuesProbability.append(valueProbability)

        # Compute entropy & gain of value and add gain to the list
        valueEntropy = computeEntropy(valuesExpectedInfo, valuesProbability)
        valueGain = allExpectedInfo - valueEntropy
        valuesGain.append(valueGain)

    # The index of the attribute with the max gain
    index = valuesGain.index(max(valuesGain))

    return [attributes[index], valuesGain[index], index]


# Returns the expected info needed
# count1 is usually the number of positive examples
# count2 is usually num of negative examples
def computeExpectedInfo(count1, count2):
    count1 = float(count1)
    count2 = float(count2)
    total = count1 + count2
    prob1 = count1/total
    prob2 = count2/total

    # Can't call log(0)
    if prob1 > 0.0 and prob2 > 0.0:
        return -prob1 * math.log(prob1, 2.0) - prob2 * math.log(prob2, 2.0)
    elif prob1 > 0.0:
        return -prob1 * math.log(prob1, 2.0)
    elif prob2 > 0.0:
        return -prob2 * math.log(prob2, 2.0)
    else:
        print ('There was an error computing expected info.')
        return 0


# Compute entropy where p is a list of probabilities for each value and e is a
# list of expected info for each value. p and e should be the same length.
def computeEntropy(p, e):
    entropy = 0.0
    for i in range(len(p)):
        entropy += p[i] * e[i]
    return entropy


# Returns a list of the unique values of the given attribute (given by index) in the given examples
def uniqueValues(attrIndex, examples):
    values = []
    for e in examples:
        if e[attrIndex] not in values:
            values.append(e[attrIndex])
    return values


# Returns the most common value of the attribute in the examples
# Values param is the possible value for that attribute
def getMostCommonValue(attr, examples, values):
    valueCounts = []

    for value in values:
        valueCount = 0
        for example in examples:
            if example[attr] == value:
                valueCount += 1
        valueCounts.append(valueCount)

    maxIndex = valueCounts.index(max(valueCounts))
    return values[maxIndex]


# Returns the decision tree from a file containing training data
# where the first line contains the attributes separated by commas
# and each other line contains a data example
def constructTreeFromFile(filepath):
    f = open(filepath, 'r')
    attrLine = f.readline()
    attributes = [a.strip() for a in attrLine.split(',')]
    examples = []
    for line in f:
        example = [item.strip() for item in line.split(',')]
        examples.append(example)

    # The last attribute is always the target attribute
    return constructDecisionTree(examples, attributes[-1], attributes)


# Returns a list of test cases for the decision tree (examples that don't have
def parseTestCases(filepath):
    f = open(filepath, 'r')
    cases = []
    for line in f:
        case = [item.strip() for item in line.split(',')]
        cases.append(case)

    return cases


def getAttributesFromFile(filepath):
    f = open(filepath, 'r')
    attrLine = f.readline()
    return [a.strip() for a in attrLine.split(',')]


trainingPath = input('Please enter the path to a file containing training data:\n')
tree = constructTreeFromFile(trainingPath)
tree.printTree()

attributes = getAttributesFromFile(trainingPath)
attributes.pop(-1)

testingPath =   input('Please enter the path to a file containing cases to be tested:\n')
testCases = parseTestCases(testingPath)
outcomes = tree.predictOutcome(testCases, attributes)
print (outcomes)