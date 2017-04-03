from A3.Data import get_random_data, get_real_data
import operator
import functools
import itertools
import math


class Vertex(object):
    """This is a feature"""

    def __init__(self, feature_id):
        self.fid = feature_id
        self.p0 = None
        self.p1 = None

    def calc_p(self, data_set):
        my_sum = 0
        for d in data_set:
            my_sum = my_sum + 1 if d[self.fid] == 0 else my_sum
        self.p0 = my_sum / len(data_set)
        self.p1 = 1 - self.p0

    def __hash__(self):
        return self.fid

    def __str__(self):
        return str(self.fid)


class Edge(object):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.p00 = None
        self.p11 = None
        self.p10 = None
        self.p01 = None
        self.weight = None

    def calc_ps(self, data_set):
        s00 = 0
        s11 = 0
        s10 = 0
        s01 = 0
        for d in data_set:
            if d[self.v1.fid] == 1:
                if d[self.v2.fid] == 1:
                    s11 += 1
                else:
                    s10 += 1
            else:
                if d[self.v2.fid] == 1:
                    s01 += 1
                else:
                    s00 += 1
        self.p00 = s00 / len(data_set)
        self.p11 = s11 / len(data_set)
        self.p01 = s01 / len(data_set)
        self.p10 = s10 / len(data_set)

    def __str__(self):
        return str(self.v1) + "-" + str(self.weight) + "->" + str(self.v2)


# estimate unknown dependence tree
# 2. check probabilities of a feature when another feature is 1 or 0
def dependence_tree_estimator(test_data):

    # combine data from each class into single list
    combined_data = []
    for c in test_data:
        combined_data.extend(c)

    print(len(combined_data))
    # calculate indiviual probabilities for each feature
    vertexs = [Vertex(i) for i in range(len(combined_data[0]))]
    for v in vertexs:
        v.calc_p(combined_data)
    edges = itertools.combinations(vertexs, 2)
    edges = [Edge(x[0], x[1]) for x in edges]
    for edge in edges:
        # calculate probabilities for feature pairs to be each value
        edge.calc_ps(combined_data)
        # use EMIM function to calculate weights,
        # i=0, j=0
        weight = edge.p00*math.log2(edge.p00/(edge.v1.p0 * edge.v2.p0))
        # i=1, j=0
        weight += edge.p00*math.log2(edge.p10/(edge.v1.p1 * edge.v2.p0))
        # i=0, j=1
        weight += edge.p00*math.log2(edge.p01/(edge.v1.p0 * edge.v2.p1))
        # i=1, j=1
        weight += edge.p11*math.log2(edge.p11/(edge.v1.p1 * edge.v2.p1))

        # print(weight)
        edge.weight = weight

    edges = sorted(edges, key=lambda x: x.weight, reverse=True)

    # tree time!
    graph_vs = set()
    graph_es = []
    for edge in edges:
        if edge.v1 in graph_vs and edge.v2 in graph_vs:
            continue
        graph_vs.add(edge.v1)
        graph_vs.add(edge.v2)

        graph_es.append(edge)

    for e in graph_es:
        print(e)



def bayesian_independent_trainer(training_data):
    """training data is a single class of data entries
    :returns list of probabilities that each feature is 0"""

    trainer = [0 for x in range(len(training_data))]
    for d in training_data:
        trainer = [x+1 if y == 0 else x for x, y in zip(trainer, d)]
    trainer = [x/len(training_data) for x in trainer]

    return trainer


def bayesian_independent_tester(classes, test_data):
    """input a list of bayesian_independent_trainers, and test data
    :returns confidence for each test data on each trainer"""

    result = []

    for d in test_data:
        # compare against each class_trainer
        test = []
        for c in classes:
            confidence = [abs(di - ci) for di, ci in zip(d, c)]
            confidence = functools.reduce(operator.mul, confidence, 1)
            test.append(confidence)
        result.append(test)
    return result


def confidence_classifier(data_confidences, test_data, class_only=False):
    winner = 0
    result = []
    for d, td in zip(data_confidences, test_data):
        for i in range(1, len(d)):
            if d[i] > d[winner]:
                winner = i
        if class_only:
            result.append(winner)
        else:
            result.append((td, winner))
    return result


def five_fold_validation(input_data_set, trainer=bayesian_independent_trainer,
                         tester=bayesian_independent_tester, classifier=confidence_classifier):
    # split data into 5 equal groups
    splits = []
    start = 0
    end = 400
    for i in range(5):
        splits.append([x[start:end] for x in input_data_set])
        start += 400
        end += 400
    # for each group combine the other 4 to train, then test with remaining one
    correct = 0
    total = 0
    for i, test_data in enumerate(splits):
        training_data = [[] for x in range(len(test_data))]
        for x, data in enumerate(splits):
            if i == x:
                continue
            for a, b in enumerate(training_data):
                training_data[a].extend(data[a])

        trainers = [trainer(x) for x in training_data]
        for cid, test_data_class in enumerate(test_data):
            r = tester(trainers, test_data_class)
            class_result = classifier(r, test_data_class, class_only=True)
            for cr in class_result:
                if cr == cid:
                    correct += 1
                total += 1

    print(total, correct)
    return correct/total


if __name__ == "__main__":
    d = get_random_data()
    dependence_tree_estimator(d)
    # accuracy = five_fold_validation(d)
    # print(accuracy*100)
