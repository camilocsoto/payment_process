The directory payment_service was the reestructuration of solid_principles on the files ater.py

There's a problem with solid principles: there're so many code lines in one olly file, which means it's not maintainable

How to reestructure the project?
1. Revisa todas las clases de bajo nivel y asignales una categoría: a partir de los contextos y funcionalidades.
2. Crea una carpeta a cada contexto.
3. Crea los archivos y su nombre debe ser de acuerdo a su funcionalidad.

separation criteria:
- Los servicios o clase principal que integra el funcionamiento de todos los módulos no va en una carpeta, va en la raíz
- Las clases que tienen distintos constructores: va en la carpeta "commons", para cada tipo de datos hay un archivo
- Cada directorio necesita un archivo __init__.py para poder hacer accesibles sus archivos (from directoryName import fileName)
- Cada protocolo debe tener su propio archivo .py

characteristics:
- the directories loggers, validators and  doesn't depend from a protocol. By other hand, processors, notifiers, depend from protocols
- The directory processors has a lot of complexity because has 3 protocols and 3 payment procesors
