from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        usuario,pelicula,calif,genero,fecha = line.split(',')
        yield usuario, float(calif)

    def reducer(self, usuario, values):
        l = list(values)
        pro = sum(l) / len(l)
        yield usuario, ("calificacion promedio",pro,"peliculas vistas",len(l))

if __name__ == '__main__':
    MRWordFrequencyCount.run()