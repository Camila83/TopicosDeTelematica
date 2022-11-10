from mrjob.job import MRJob
from sympy import true

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        cp, precio, fecha = line.split(',')
        yield cp, float(precio)

    def reducer(self, cp, values):
        l = list(values)
        est = true
        valorPasado = l[0]
        for valor in l[1:]:
            if valor < valorPasado:
                est = False
            valorPasado = valor
        if est:
            yield cp, 'Estable'
        

if __name__ == '__main__':
    MRWordFrequencyCount.run()