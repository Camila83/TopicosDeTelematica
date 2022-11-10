from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        cp, precio, fecha = line.split(',')
        yield cp,(precio, fecha)

    def reducer(self, cp, values):
        l = list(values)
        dMin= min(l)
        dMax= max(l)
        yield cp ,("Peor dia",dMin,"Mejor dia",dMax)

if __name__ == '__main__':
    MRWordFrequencyCount.run()