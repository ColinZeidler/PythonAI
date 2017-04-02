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


if __name__ == "__main__":
    data_class_1 = DataClass()
    f1 = DataFeature(None, 0.3, 0.3)
    data_class_1.add_feature(f1)
    f2 = DataFeature(f1, 0.25, 0.67)
    data_class_1.add_feature(f2)
    f3 = DataFeature(f1, 0.55, 0.23)
    data_class_1.add_feature(f3)
    f4 = DataFeature(f1, 0.93, 0.76)
    data_class_1.add_feature(f4)
    f5 = DataFeature(f2, 0.4, 0.44)
    data_class_1.add_feature(f5)
    f6 = DataFeature(f3, 0.65, 0.32)
    data_class_1.add_feature(f6)
    f7 = DataFeature(f4, 0.11, 0.35)
    data_class_1.add_feature(f7)
    f8 = DataFeature(f4, 0.8, 0.22)
    data_class_1.add_feature(f8)
    f9 = DataFeature(f6, 0.76, 0.78)
    data_class_1.add_feature(f9)
    f0 = DataFeature(f6, 0.56, 0.43)
    data_class_1.add_feature(f0)

    d = [data_class_1.generate_sample() for x in range(2000)]
    for x in d:
        print(x)
