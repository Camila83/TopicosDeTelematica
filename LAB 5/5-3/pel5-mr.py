from mrjob.job import MRJob, MRStep

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        usuario, pelicula, calif, genero, fecha= line.split(',')
        
        yield fecha , float(calif)

    def reducer(self,fecha, values):
        l = list(values)
        pro = sum(l)/len(l)
        yield None, (pro, fecha)

    def reducer2(self, _, values):
        yield 'Dia con peores calificaciones', min(values)

    def steps(self):
        return [
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordFrequencyCount.run()