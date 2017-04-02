from A3.Data import get_random_data, get_real_data
import operator
import functools


# estimate unknown dependence tree
# 1. calculate individual probability for each feature in the current class
# 2. check probabilities of a feature when another feature is 1 or 0
def dependece_tree_estimator(test_data):
    pass


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
    accuracy = five_fold_validation(d)
    print(accuracy*100)
