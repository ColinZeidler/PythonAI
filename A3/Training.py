from A3.Data import DataClass, DataFeature
import operator
import functools


def get_all_data():
    data_classes = [DataClass()]

    f1 = DataFeature(None, 0.27, 0.27)
    data_classes[-1].add_feature(f1)
    f2 = DataFeature(f1, 0.58, 0.84)
    data_classes[-1].add_feature(f2)
    f3 = DataFeature(f1, 0.67, 0.27)
    data_classes[-1].add_feature(f3)
    f4 = DataFeature(f1, 0.40, 0.76)
    data_classes[-1].add_feature(f4)
    f5 = DataFeature(f2, 0.48, 0.83)
    data_classes[-1].add_feature(f5)
    f6 = DataFeature(f3, 0.84, 0.94)
    data_classes[-1].add_feature(f6)
    f7 = DataFeature(f4, 0.32, 0.48)
    data_classes[-1].add_feature(f7)
    f8 = DataFeature(f4, 0.83, 0.28)
    data_classes[-1].add_feature(f8)
    f9 = DataFeature(f6, 0.66, 0.04)
    data_classes[-1].add_feature(f9)
    f0 = DataFeature(f6, 0.98, 0.85)
    data_classes[-1].add_feature(f0)

    data_classes.append(DataClass())
    f1 = DataFeature(None, 0.56, 0.56)
    data_classes[-1].add_feature(f1)
    f2 = DataFeature(f1, 0.50, 0.17)
    data_classes[-1].add_feature(f2)
    f3 = DataFeature(f1, 0.97, 0.70)
    data_classes[-1].add_feature(f3)
    f4 = DataFeature(f1, 0.38, 0.81)
    data_classes[-1].add_feature(f4)
    f5 = DataFeature(f2, 0.02, 0.24)
    data_classes[-1].add_feature(f5)
    f6 = DataFeature(f3, 0.07, 0.95)
    data_classes[-1].add_feature(f6)
    f7 = DataFeature(f4, 0.79, 0.11)
    data_classes[-1].add_feature(f7)
    f8 = DataFeature(f4, 0.55, 0.05)
    data_classes[-1].add_feature(f8)
    f9 = DataFeature(f6, 0.66, 0.97)
    data_classes[-1].add_feature(f9)
    f0 = DataFeature(f6, 0.81, 0.63)
    data_classes[-1].add_feature(f0)

    data_classes.append(DataClass())
    f1 = DataFeature(None, 0.88, 0.88)
    data_classes[-1].add_feature(f1)
    f2 = DataFeature(f1, 0.68, 0.69)
    data_classes[-1].add_feature(f2)
    f3 = DataFeature(f1, 0.66, 0.19)
    data_classes[-1].add_feature(f3)
    f4 = DataFeature(f1, 0.55, 0.53)
    data_classes[-1].add_feature(f4)
    f5 = DataFeature(f2, 0.60, 0.46)
    data_classes[-1].add_feature(f5)
    f6 = DataFeature(f3, 0.76, 0.39)
    data_classes[-1].add_feature(f6)
    f7 = DataFeature(f4, 0.86, 0.31)
    data_classes[-1].add_feature(f7)
    f8 = DataFeature(f4, 0.29, 0.05)
    data_classes[-1].add_feature(f8)
    f9 = DataFeature(f6, 0.88, 0.57)
    data_classes[-1].add_feature(f9)
    f0 = DataFeature(f6, 0.14, 0.42)
    data_classes[-1].add_feature(f0)

    data_classes.append(DataClass())
    f1 = DataFeature(None, 0.01, 0.01)
    data_classes[-1].add_feature(f1)
    f2 = DataFeature(f1, 0.94, 0.60)
    data_classes[-1].add_feature(f2)
    f3 = DataFeature(f1, 0.44, 0.38)
    data_classes[-1].add_feature(f3)
    f4 = DataFeature(f1, 0.28, 0.40)
    data_classes[-1].add_feature(f4)
    f5 = DataFeature(f2, 0.43, 0.40)
    data_classes[-1].add_feature(f5)
    f6 = DataFeature(f3, 0.43, 0.58)
    data_classes[-1].add_feature(f6)
    f7 = DataFeature(f4, 0.15, 0.91)
    data_classes[-1].add_feature(f7)
    f8 = DataFeature(f4, 0.63, 0.36)
    data_classes[-1].add_feature(f8)
    f9 = DataFeature(f6, 0.43, 0.86)
    data_classes[-1].add_feature(f9)
    f0 = DataFeature(f6, 0.15, 0.69)
    data_classes[-1].add_feature(f0)

    data_list = []
    for c in data_classes:
        data_list.append([c.generate_sample() for x in range(2000)])
    print("Class Count:", len(data_list))
    print("Item Count:", [len(x) for x in data_list])
    return data_list

# estimate unknown dependence tree
# 1. calculate individual probability for each feature in the current class
# 2. check probabilities of a feature when another feature is 1 or 0
def dependece_tree_estimator(test_data):
    pass


def bayesian_independent_trainer(training_data):
    """training data is a single class of data entries with 10 values each
    :returns """

    trainer = [0 for x in range(10)]
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


def confidence_classifier(data_confidences, test_data):
    winner = 0
    result = []
    for d, td in zip(data_confidences, test_data):
        for i in range(1, len(d)):
            if d[i] > d[winner]:
                winner = i
        result.append((td, winner))
    return result


if __name__ == "__main__":
    d = get_all_data()

    # TODO split data into 5 groups, 4 to train 1 to test
    trainers = [bayesian_independent_trainer(x) for x in d]

    test = d[0][-1]
    train = d[0][:-1]
    r = bayesian_independent_tester(trainers, [test])
    print(confidence_classifier(r, [test]))
