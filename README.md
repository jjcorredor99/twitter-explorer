# TWITTER EXPLORER

Este es un paquete para explorar listas de tuits extraídas con las Apis Standard Search y Standard Stream de Twitter.

Un ejemplo de cómo extraer tuits usando Standard Search se encuentra [aquí](https://github.com/Obsdemocracia/twitter-explorer/blob/master/Extract%20tuits%20Standard%20Search.ipynb)
Los requerimientos del paquete son:

- Tweepy
- .....

Para instalar el paquete descargue este repo y en su código use este código:

```python
import sys  
sys.path.insert(0, [PATH TO REPO])
import twitter_explorer
```
Este paquete incluye funciones para:

1. Generar una gráfica de la cantidad de tuits por día.
2. Generar un contador de los hashtags usados e imprimir el Top n.
3. Generar un contador de los usuarios mencionados e imprimir el Top n.
4. Generar un contador de las urls usadas e imprimir el Top n.
5. Generar un contador de las dominios usados e imprimir el Top n.
6. Unificar el texto de los tuits en una única variable.
7. Generar una variable con el número total de tuits de un tuit (Suma de los retuits al tuit original y al retuiteado o citado).
8. Identificar los n tuits más retuiteados.
9. Buscar tuits por su ID.
10. Buscar tuits por palabra clave.
11. Generar una nube de palabras con las bios de los usuarios.
12. Generar una nube de palabras del texto
13. Generar una nube de palabras de los tuits que contengan palabras clave.

Un ejemplo de uso de las funciones se encuentra [aquí](https://github.com/Obsdemocracia/twitter-explorer/blob/master/Ejemplo%20funciones%20Twitter.ipynb)

La documentación completa se encuentra [aquí]
