# Script de autenticación simple con Python y diccionarios

Script de autenticación que usa una consulta o request de "base de datos" estilo JSON en un diccionario de Python.

2 tipos de clases: Los usuarios y el acceso a la base de datos.
Los usuarios base (User) tienen una subclase Admin. Ambos tienen permisos y menús diferentes.

## Los menús

Al iniciar el programa se muestra un menú con la posibilidad de registrar un usuario, iniciar sesión, o salir del sistema. Este es el menú principal de acceso al sistema, del que se puede salir, terminando la ejecución, al introducir el 3 (que corresponde a la salida del sistema). El registro inicia sesión automáticamente en la cuenta creada.

Una vez se ha efectuado el registro o el inicio de sesión, se genera una sesión. La sesión es una instancia de la clase que corresponde al usuario que inicia sesión (User o Admin). Esta instancia, al inicializarse con los parámetros del usuario, inicia el menú de opciones del usuario registrado. Las acciones tienen efectos persistentes, ya que modifican directamente el diccionario que contiene los datos de los usuarios, aunque sólo las sesiones de la clase Admin tienen la opción de modificar datos de otras personas.

Cuando se desee salir de la sesión, se puede cerrar sesión en el menú principal de la sesión, y se devolverá al usuario a la pantalla de Registro, Inicio de sesión o salida, donde puede volver a elegir según guste.

## Los usuarios

2 Clases: *User y Admin*.
* **User**: Clase base de los usuarios. Puede consultar sus datos, modificar sus propias credenciales, y modificar su propia lista.
* **Admin**: Clase que hereda de User, con permisos para consultar los datos de todos los usuarios, modificar credenciales de todos, crear y eliminar usuarios, y modificar listas de todos.
La única utilidad real implementada de momento para los usuarios es una lista de "productos" en la que pueden añadir o eliminar los productos que quieran.
Las entradas de usuarios Admin sólo pueden ser creadas por otro Admin, y el registro manual de usuario anónimo sólo permite crear usuarios base.

## El sistema

1 clase: **DatabaseAccess**.
DatabaseAccess inicializa el diccionario "data", que contiene los datos de todos los usuarios, y contiene además los métodos tanto de los menús de usuario "anónimo", como los que permiten modificar el diccionario.

## Posibles problemas y direcciones de mejora

- La implementación de un almacenamiento persistente como una base de datos es el siguiente paso natural.

- Es importante y necesaria la implementación de medidas de seguridad para evitar SQL Injections si se usa base de datos, y mejorar las verificaciones y medidas de seguridad en algunas partes concretas del código, aunque en general para su propósito está bastante bien.

- Dividir la clase DatabaseAccess en 2 clases: Una que contenga al usuario anónimo y los menús, y otra que contenga a los propios datos y los métodos para modificarlos.

- Crear funciones, ya que se repite muchísimo código. Varias ideas útiles son verificadores del input para las elecciones (Elige 1, 2 o 3...) o verificadores del input para los input de username o password, que es un código relativamente denso y muy repetido en todo el script.

- Probar a implementar el sistema en una base de datos real, con utilidades reales, sustituyendo la "lista" de productos simple que hay ahora mismo.

- Puede que hayan problemas de implementación de algunas funciones, como anidación de ejecución de funciones, aunque no lo he comprobado aún.

- Al eliminarse un usuario Admin a sí mismo y cerrar sesión, el programa se rompe y entra en un bucle de ejecución infinito. Por lógica, directamente no se permite que un usuario Admin se elimine a sí mismo, pues así se perdería la posibilidad de crear más usuarios Admin.