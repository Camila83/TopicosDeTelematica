from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        usuario, pelicula, calif, genero, fecha= line.split(',')
        
        yield fecha , 1

    def reducer(self,fecha, values):
        yield None, (sum(values), fecha)

    def reducer2(self, _, values):
        yield 'Dia en que se vieron mas peliculas', max(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()