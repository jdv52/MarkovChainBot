import copy


class Loader:

    def __init__(self, order):
        self.frequency_table = {}
        self.probability_table = {}
        self.order = order
        self.txt = ''

    def load_data(self, file_name):
        f = open(file_name, "r")
        self.txt = f.read()
        return self.txt

    def generate_table(self, data):
        order = self.order
        T = {}
        for i in range(len(data) - order):
            gram = data[i:i + order]
            next_gram = data[i + order]
            if gram not in T:
                T[gram] = {}
                T[gram][next_gram] = 1
            elif next_gram not in T[gram]:
                T[gram][next_gram] = 1
            else:
                T[gram][next_gram] += 1
        self.frequency_table = T
        return T

    def frequency_to_prob(self, table):
        T = copy.deepcopy(table)
        for kx in T:
            s = float(sum(T[kx].values()))
            for k in T[kx].keys():
                T[kx][k] = T[kx][k] / s
        self.probability_table = T
        return T

