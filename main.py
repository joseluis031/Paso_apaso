from asincrono import *       # Importa el modulo asincrono
if __name__ == '__main__':
    time = timeit(main, number=1)# Tiempo de ejecucion
    write_in_file('time.txt', str(time))# Guarda el tiempo de ejecucion en un archivo
    asyncio.run(main())        # Ejecuta el programa