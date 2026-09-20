class User():

    def __init__(self, username, password, db, id):
        self.username = username
        self.password = password
        self.database = db
        self.id = id
        self.user = self.database.data[self.username]
        self.menu_choices = {1: self.get_my_data, 2: self.add_or_remove, 3: self.credential_mod_options, 4: self.logout}
        self.init_user_action()

    def show_options(self):
        """
        Imprime las opciones del usuario.
        """
        print(f"\nBienvenido {self.username}. ¿Qué deseas hacer?")
        print("1: Ver mi perfil.\n2: Añadir o eliminar un producto de mi lista.\n3: Modificar mis credenciales.\n4: Cerrar sesión.")

    def get_user_choice(self):
        """
        Obtiene y devuelve la elección del usuario sobre el menú inicial.
        """
        user_choice = 0
        while user_choice not in {1, 2, 3, 4}:
            try:
                user_choice = int(input("Elige 1, 2, 3 o 4: "))
            except ValueError:
                print("Valor incorrecto.")
                continue
        return user_choice
        
    def execute_user_choice(self, user_choice):
        self.menu_choices[user_choice]()

    def init_user_action(self):
        self.show_options()
        user_choice = self.get_user_choice()
        self.execute_user_choice(user_choice)

    def get_my_data(self):
        datos = f"\nUsuario: {self.username}\nContraseña: {self.password}\n"
        datos += f"id: {self.id}\nLista de productos: {self.user["products"]}"
        print(datos)
        self.init_user_action()

    def credential_mod_options(self):
        print("\n1: Modificar mi usuario.\n2: Modificar mi contraseña.\n3: Volver al menú.")
        user_choice_options = {1:self.set_username, 2:self.set_password}
        while True:
            try: user_choice = int(input("Por favor, seleccione una opción: "))
            except ValueError:
                print("Valor incorrecto.") 
                continue
            if user_choice not in {1, 2, 3}:
                print("Valor incorrecto.")
                continue
            elif user_choice == 3:
                break
            else:
                user_choice_options[user_choice]()
                return None
        self.init_user_action()

    def set_username(self):
        while True:
            new_username = input("Nuevo usuario o 'exit': ")
            verify_password = input("Contraseña antigua: ") == self.password
            if len(new_username) > 20 or len(new_username) < 4 or not verify_password:
                print("Nombre de usuario o contraseña no válido/a.")
                continue
            elif new_username == 'exit':
                break
            else:
                self.database.modify_username(self.username, new_username, self.password)
                self.username = new_username
                break

        self.init_user_action()

    def set_password(self):
        while True:
            new_password = input("Nueva contraseña o 'exit': ")
            verify_password = input("Contraseña antigua: ") == self.password
            if len(new_password) > 20 or len(new_password) < 4 or not verify_password:
                print("Alguna de las dos contraseñas es incorrecta. Vuelve a intentarlo.")
                continue
            elif new_password == "exit":
                break
            else:
                self.database.modify_password(self.username, self.password, new_password)
                self.password = new_password
                break

        self.init_user_action()

    def add_or_remove(self):
        print("\n1: Añadir un producto a mi lista.\n2: Eliminar un producto de mi lista.\n3: Volver al menú.")
        ADD_REMOVE_OPTIONS = {1: self.add_product, 2: self.rm_product}

        while True:
            try: user_choice = int(input("Por favor, seleccione una opción: "))
            except ValueError:
                print("Valor incorrecto.") 
                continue
            if user_choice not in {1, 2, 3}:
                print("Valor incorrecto.")
                continue
            elif user_choice == 3:
                break
            else:
                ADD_REMOVE_OPTIONS[user_choice]()
                return None
        self.init_user_action()

    def add_product(self):
        producto = input("Producto a añadir (o escribe 'exit'): ")
        if producto != "exit":
            self.database.add_product_to_data(self.username, producto)
            print("Producto añadido con éxito. Volviendo al menú...")
        self.init_user_action()

    def rm_product(self):
        print("Especifique un producto o escriba 'exit' para continuar.")
        while True:
            producto = input("Producto a eliminar: ")
            if producto == "exit":
                break
            elif producto in self.user["products"]:
                self.database.rm_product_from_data(self.username, producto)
                print("Producto eliminado con éxito. Volviendo al menú...")
                break
            else:
                print("Parece que el producto no se encuentra en la lista. Por favor, repita.")
        self.init_user_action()

    def logout(self):
        # Posible foco de problemas.
        print("\nCerrando sesión...\n")
        self.database.anon_register_login_pipeline()

class Admin(User):

    def menu(self):
        """
        Permite obtener datos de la base de datos y modificarlos.
        """
    def add_entry(self):
        pass
    def remove_entry(self):
        pass
    def modify_entry(self):
        pass
    def get_database(self):
        pass
    def get_entry(self):
        pass

class DatabaseAccess():

    def __init__(self):
        self.data = {"test":{"permissions":User, "password":"test_user", "id":0, "products":[]},
                     "admin":{"permissions":Admin, "password":"Admin123", "id":1, "products":["BFG9000"]}
                     }
        self.choice_menu = {
            1:self.register,
            2:self.login,
            3:self.exit
        }
        self.current_session = None
        self.user_clearance = {"admin":Admin, "user":User}
        self.user_counter = 1

    # Añadir, eliminar o modificar usuarios.

    def add_new_user(self, username,  password,  permissions = User):
        """
        Usado para añadir un usuario a la base de datos. Usuario base por defecto.
        """
        self._counter()
        new_user_data = {username:{"permissions":permissions, "password": password, "id":self.user_counter}}
        self.data.update(new_user_data)

    def delete_user(self, username):
        self.data.pop(username)

    def modify_username(self, old, new, password):
            self.data[new] = self.data[old]
            self.delete_user(old)
            print("Nombre de usuario modificado con éxito.")

    def modify_password(self, username, old, new):
            self.data[username][old] = new
            print("Contraseña modificada con éxito.")

    def add_product_to_data(self, username, product):
        self.data[username]["products"].append(product)
    def rm_product_from_data(self, username, product):
        self.data[username]["products"].remove(product)

    # Registrar, hacer login, o cerrar sesión.

    def register(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if username == "exit" or password == "exit":
                self.anon_register_login_pipeline()
                break
            elif self.data.get(username, False):
                print("Usuario ya registrado.")
                continue
            elif len(username) > 20 or len(password) > 30 or len(username) < 4 or len(password) < 4:
                print("Usuario y/o contraseña demasiado largo.")
                continue
            break
        self.add_new_user(username, password, User)
        self.login(username, password)

    def login(self, uname = None, passw = None):
        """
        Si recibe parámetros inicia sesión en esos parámetros (esto es por register).
        Si no los recibe, itera una vez, no hace nada, y entonces pide input de username y password.
        Reitera hasta que encuentra una combinación válida, y loggea.
        MUY susceptible a bruteforcing. No pensado para escenarios auténticos.
        Es la única función que crea User(), Register bebe de ella y hace login cuando registra usuario.
        """
        username = uname
        password = passw
        is_user = False

        print("Inicio de sesión...")
        
        while True:
            try:
                is_user = self.is_user(username, password)
            except KeyError:
                print("Por favor, introduzca un usuario y clave correctos.")
            if username != None and password != None and is_user:
                print("¡Sesión iniciada con éxito!")
                self.current_session = self.data[username]["permissions"](username, password, self, self.data[username]["id"])
                break
            elif username != None and password != None and not is_user:
                print("Usuario o contraseña incorrectos.")
                continue
            elif (not uname) and (not passw):
                username = input("Username: ")
                password = input("Password: ")

            if username == "exit" or password == "exit":
                break
        if username == "exit" or password == "exit":
            self.anon_register_login_pipeline()

    def logoff(self):
        self.current_session = None

    def exit(self):
        print("Saliendo del menú...")

    # Menú de usuario anónimo (antes de iniciar sesión).
        
    def _login_register_choice_menu(self):
        print("\n----Sistema de Autenticación----")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

    def _obtain_anon_choice(self):
        while True:
            try:
                anon_user_choice = int(input("Elija 1, 2 o 3: "))
            except ValueError:
                print("Valor no numérico.")
                continue
            if anon_user_choice not in {1, 2, 3}:
                print("Opción fuera de las posibles.")
                continue
            break
        return self.choice_menu[anon_user_choice]

    def anon_register_login_pipeline(self):
        """
        Pipeline completa del menú inicial del repo.
        """
        self.logoff()
        self._login_register_choice_menu()
        anon_choice = self._obtain_anon_choice()
        anon_choice()

    # Herramientas misceláneas.

    def is_user(self, username, password):
        """
        Comprueba que existe el usuario Y luego comprueba que la contraseña coincide.
        Si cualquiera de las dos falla, devuelve False. Si ambas son verdaderas, devuelve True (and).
        """
        if self.data.get(username, False):
            result = self.data[username]["password"] == password
        else:
            result = False
        return result

    def _counter(self):
        """
        Utilizado para las id de self.data, que incrementan en 1 por cada usuario nuevo. Se usa en Register.
        """
        self.user_counter += 1

if __name__ == "__main__":
    Database = DatabaseAccess()
    Database.anon_register_login_pipeline()