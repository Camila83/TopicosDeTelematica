from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        usuario,pelicula,calif,genero,fecha = line.split(',')
        yield pelicula, (usuario ,float(calif))

    def reducer(self, pelicula, values):
        l = list(values)
        pro = sum([x[1] for x in l])/len(l)
        yield pelicula, ("calificacion promedio",pro,"numero de usuarios que vieron",len(l))

if __name__ == '__main__':
    MRWordFrequencyCount.run()