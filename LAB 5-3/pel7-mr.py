from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        usuario, pelicula, calif, genero, fecha = line.split(',')
       
        yield (pelicula, genero),float(calif)

    def reducer(self, genpel, values):
        l = list(values)
        yield genpel, sum(l)/len(l)

    def mapper2(self, genpel, value):
        yield genpel[1], (value, genpel[0])

    def reducer2(self, genero, values):
        l = list(values)
        yield genero, ("Peor pelicula: ", min(l), "mejor pelicula: ", max(l))

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(mapper=self.mapper2, reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()