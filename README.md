# Paso_apaso

El link de este repositorio es el siguiente: [GitHub](https://github.com/joseluis031/Paso_apaso.git)


## Codigo en asincrono

```
#importo las librerias necesarias
import asyncio 
import aiohttp
from urllib.parse import urlparse
import sys
from os import sep
from sys import stderr
import functools
from bs4 import BeautifulSoup

from timeit import timeit


async def get_images_src_from_html(html_doc):      
    """Recupera todo el contenido de los atributos src de las etiquetas 
img"""   
    soup = BeautifulSoup(html_doc, "html.parser")  # Parsea el HTML    
    for img in soup.find_all('img'):    
        yield img.get('src')    
        await asyncio.sleep(0.001)  # Evita saturar el servidor

async def get_uri_from_images_src(base_uri, images_src): 
    """Devuelve una a una cada URI de la imagen a descargar"""    
    parsed_base = urlparse(base_uri)# Parsea la URI base
    async for src in images_src: # Recorre cada src de la imagen
        parsed = urlparse(src)# Parsea cada src de la imagen
        if parsed.netloc == '': # Si no tiene netloc, es relativa
            path = parsed.path    
            if parsed.query:    
                path += '?' + parsed.query    
            if path[0] != '/':    
                if parsed_base.path == '/':    
                    path = '/' + path    
                else:    
                    path = '/' + '/'.join(parsed_base.path.split('/')   [:-1]) + '/' + path    
            yield parsed_base.scheme + '://' + parsed_base.netloc + path  
        else:    
            yield parsed.geturl()# Si tiene netloc, es absoluta   
            await asyncio.sleep(0.001) # Evita saturar el servidor
            
async def get_images(session, page_uri):# Recibe la sesion y la URI de la pagina  
    html = await wget(session, page_uri)  # Descarga la pagina
    if not html:  # Si no se ha podido descargar, devuelve None
        print("Error: no se ha encontrado ninguna imagen", 
        sys.stderr)  
        return None  
    images_src_gen = get_images_src_from_html(html)# Recupera los src de las imagenes  
    images_uri_gen = get_uri_from_images_src(page_uri, # Recupera las URIs de las imagenes
        images_src_gen)  
    async for image_uri in images_uri_gen:  # Recorre cada URI de la imagen
        print('Descarga de %s' % image_uri)  
        await download(session, image_uri) # Descarga la imagen


async def wget(session, uri):    # Recibe la sesion y la URI a descargar
    """Descarga una URI y devuelve el contenido"""    
    async with session.get(uri) as response:    # Descarga la URI
        if response.status == 200:# Si la respuesta es correcta
            if response.content_type == 'text/html':   
                return await response.text() 
            else:    
                return await response.read()   
        else:    
            return None
        
async def download(session, uri):    
    """Descarga una URI y la guarda en el disco"""    
    async with session.get(uri) as response:    
        if response.status == 200:    
            if response.content_type == 'text/html':    
                return None    
            else:    
                filename = uri.split('/')[-1]    
                with open(filename, 'wb') as f:    
                    while True:    
                        chunk = await response.content.read(1024)    
                        if not chunk:    
                            break    
                        f.write(chunk)    
                return filename    
        else:    
            return None
        
async def main():
    async with aiohttp.ClientSession() as session:    
        await get_images(session, 'https://viajes.nationalgeographic.com.es/a/mejores-playas-espana_11759')
    
    
def write_in_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    
        
if __name__ == '__main__':
    time = timeit(main, number=1)# Tiempo de ejecucion
    write_in_file('time.txt', str(time))# Guarda el tiempo de ejecucion en un archivo
    asyncio.run(main())        # Ejecuta el programa
```
Con este codigo, conseguimos que, de manera asincrona, se descarguen todas las
imagenes de una pagina web y que se guarden en una carpeta, ademas de que se escriba
en un .txt el tiempo que ha tardado en descargar la imagen


## Ejecucion del codigo en asincrono

```
Descarga de https://viajes.nationalgeographic.com.es//a/image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 837"%3E%3C/svg%3E
Descarga de https://viajes.nationalgeographic.com.es/medio/2022/05/06/istock-611291102_b81f9871_1254x837.jpg
Descarga de https://viajes.nationalgeographic.com.es//a/image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 869"%3E%3C/svg%3E
Descarga de https://viajes.nationalgeographic.com.es/medio/2017/07/10/cala-pola-tossa-de-mar_4c9b3ec2.jpg
Descarga de https://viajes.nationalgeographic.com.es//a/image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 667"%3E%3C/svg%3E
Descarga de https://viajes.nationalgeographic.com.es/medio/2020/09/15/playa-de-poo-asturias_e5404338_1000x667.jpg
Descarga de https://viajes.nationalgeographic.com.es//a/image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 836"%3E%3C/svg%3E
Descarga de https://viajes.nationalgeographic.com.es/medio/2022/05/04/castro-de-barona_c1e9ced6_1254x836.jpg
```

![tiempo ejecucion asincrono](https://user-images.githubusercontent.com/91721888/230768517-13792021-cf1a-4b41-afff-e09fb09dea6e.png)

Y algunas de las imagenes que se han descargado, a las cuales se puede acceder a ellas mediante 
la carpeta 'imagenes' son las siguientes:
![cala del moro](https://user-images.githubusercontent.com/91721888/230768657-7dea928d-e5f1-4f61-b8cc-e63005ae1e15.png)

![image](https://user-images.githubusercontent.com/91721888/230768726-bd02c7bb-040a-4395-a7b9-80752139095c.png)


