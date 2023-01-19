import pandas as pd
from fastapi import FastAPI
import uvicorn

app = FastAPI()

df = pd.read_csv('Datasets/out.csv')
identificador = {'amazon':'a','disney':'d','hulu':'h','netflix':'n'}

@app.get("/")
async def root():
    return {"message": "Hello World"}

#Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma
@app.get("/keyword/{plataforma}/{keyword}")
async def get_word_count(plataforma,keyword):
    count = 0
    for index,serie in df.iterrows():
        if str(keyword) in serie[2] and identificador[str(plataforma).lower()] in serie[0]:
            count += 1
    return count

#Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año
@app.get("/cantidad/{plataforma}/{score}/{anio}")
async def get_score_count(plataforma,score,anio):
    count = 0
    for index,serie in df.iterrows():
        if identificador[str(plataforma).lower()] in serie[0] and serie[11] > int(score) and serie[7] == int(anio):
            count += 1
    return count

#La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.
segunda_película = df.sort_values('title')
@app.get("/segunda_película/{plataforma}")
async def get_second_score(plataforma):
    count = 0
    for index,serie in segunda_película.iterrows():
        if identificador[str(plataforma).lower()] in serie[0] and serie[1] == 'movie' and serie[11] >= 100:
            count += 1
            if count == 2:
                return serie[2],' ',serie[11]
                break

#Película que más duró según año, plataforma y tipo de duración
@app.get("/pelicula_larga/{plataforma}/{tipo}/{anio}")
async def get_longest(plataforma,tipo,anio):
    count = {}
    for index,serie in df.iterrows():
        if serie[7] == int(anio) and identificador[str(plataforma).lower()] in serie[0] and serie[13] == str(tipo).lower():
            count[serie[12]] = serie[2]
    try:
        return count[sorted(count.keys()).pop()],' ',sorted(count.keys()).pop()
    except:
        return []


#Cantidad de series y películas por rating
@app.get("/series_peliculas_rating/{rating}")
async def get_rating_count(rating):
    count = 0
    for index,serie in df.iterrows():
        if rating in serie[8]:
            count += 1
    return count

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=64423)
