import random
random.seed()


class DataClass(object):
    """A dependence tree built out of a list of features"""
    def __init__(self):
        self.features = []  # List of features

    def add_feature(self, feature):
        self.features.append(feature)

    def generate_sample(self):
        sample = [x.get_value() for x in self.features]
        for x in self.features:
            x.value = None
        return sample


class DataFeature(object):
    def __init__(self, parent, p0, p1):
        self.parent = parent
        self.prob0ifparent0 = p0
        self.value = None
        if self.parent is None:
            self.prob0ifparent1 = self.prob0ifparent0
        else:
            self.prob0ifparent1 = p1

    def get_probablity(self, value):
        """Returns the probability of feature being given value"""
        if self.parent is None:
            prob = self.prob0ifparent0
        else:
            if self.parent.get_value() == 1:
                prob = self.prob0ifparent1
            else:
                prob = self.prob0ifparent0

        if value == 1:
            prob = 1 - prob

        return prob

    def get_value(self):
        if self.value is None:
            r = random.random()
            if r <= self.get_probablity(0):
                self.value = 0
            else:
                self.value = 1
        return self.value


def get_random_data():
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
    return data_list


def get_real_data():
    # thresholding, take the mean of the values in each feature, above is 1 below is 0
    data = []
    with open('wine.csv', 'r') as f:
        for line in f:
            data.append([float(x) for x in line.strip().split(',')])

    # calculate thresholds
    threshold = [0 for x in range(1, len(data[0]))]
    for item in data:
        for index, feature in enumerate(item):
            if index == 0:
                continue
            threshold[index-1] += feature
    threshold = [x/len(data) for x in threshold]

    # apply thresholds to data
    for item in data:
        item[0] = int(item[0])
        for index, thresh in enumerate(threshold):
            item[index+1] = 0 if item[index+1] < thresh else 1

    # sort data into classes
    data_classes = [[] for x in range(3)]
    for item in data:
        data_classes[item[0]-1].append(item[1:])
    return data_classes


if __name__ == "__main__":
    d = get_real_data()
    for c in d:
        print(c)