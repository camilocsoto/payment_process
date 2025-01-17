¡Hola!  
Para que no te pierdas en esta clase, te dejo un tutorial de cómo correr el proyecto:  
disclaimer: you need python >= 3.11.1  
1. Descarga el .zip de los recursos de clase y crea una carpeta en donde instanciar el proyecto.  
2. Crea tu entorno virtual, en mi caso mi S.O es wsl2, es decir un Linux dentro de Windows y yo lo creo con estos comandos, asegúrate de tener los comandos para tu S.O:  
´´´bash
python3 -m venv env
# activa tu entorno con el siguiente comando:
source env/bin/activate
´´´
3. Descarga las librerías:  
´´´bash
pip install pydantic numpy matplotlib typing python-dotenv stripe
´´´
4. Crea tu cuenta en Stripe: dirígete al siguiente link y crea una cuenta. Yo vivo en Colombia pero le puse México.  

5. Obtén tu API key: dirígete al siguiente link para obtener tu API key. Debes elegir tu llave secreta y copiarla. [link de api secret key](https://dashboard.stripe.com/test/apikeys)   

6. En la raíz de tu directorio/carpeta, crea un archivo y ponle de nombre .env. Allí debes pegar la API key secreta que copiaste del paso anterior.  

7. Ejecuta el proyecto :D  

¡Dirigite a src para ver la estructura del proyectoy ver como se aplícan estos principios!  
