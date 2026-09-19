class User():

    def __init__(self, username, password, db):
        self.username = username
        self.password = password
        self.database = db
        self.menu_choices = {1: self.get_my_data, 2: self.add_product, 3: self.rm_product, 4: self.logout}

    def show_options(self):
        print(f"Bienvenido {self.username}. ¿Qué deseas hacer?")
        print("1: Ver mis datos.\n2: Añadir un producto a mi lista.\n3: Eliminar un producto de mi lista.\n4: Cerrar sesión.")

    def get_user_choice(self):
        while user_choice not in {1, 2, 3, 4}:
            try:
                user_choice = int(input("Elige 1, 2, 3 o 4: "))
            except ValueError:
                continue
        return user_choice
        
    def execute_user_choice(self, user_choice):
        self.menu_choices[user_choice]()

    def init_user_action(self):
        self.show_options()
        user_choice = self.get_user_choice()
        self.execute_user_choice(user_choice)

    def get_my_data(self, db_to):
        datos = f"Usuario: {self.username}\nContraseña: {self.password}\n"
        datos += f"id: {db_to.data["id"]}\nLista de productos: {db_to.data["products"]}"
        print(datos)

    def add_product(self, db_to):
        producto = input("Producto a añadir: ")
        db_to.add_product_to_list(producto, self.username)

    def rm_product(self, db_to):
        producto = input("Producto a eliminar: ")
        if producto in db_to.data[self.username]["products"]:
            db_to.remove_product_from_list(producto, self.username)
            print("Producto eliminado con éxito. Volviendo al menú...")
        else:
            print("Parece que el producto no se encuentra en la lista. Volviendo al menú...")
        self.init_user_action()

    def logout(self, db_to):
        # Posible foco de problemas.
        db_to.anon_register_login_pipeline()

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
        self.data = {"admin":{"permissions":Admin, "password":"Admin123", "id":"1", "products":["BFG9000"]}}
        self.choice_menu = {
            1:self.register,
            2:self.login,
            3:self.exit
        }
        self.current_session = None
        self.user_clearance = {"admin":Admin, "user":User}
        self.user_counter = 1

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

        self.counter()
        new_user_data = {username:{"permissions":User, "password": password, "id":self.user_counter}}
        self.data.update(new_user_data)
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
                self.current_session = self.data[username]["permissions"](username, password, self)
                print("¡Sesión iniciada con éxito!")
                break
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
        
    def login_register_choice_menu(self):
        print("----Sistema de Autenticación----")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

    def obtain_anon_choice(self):
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

    def is_user(self, username, password):
        return self.data[username]["password"] == password

    def counter(self):
        self.user_counter += 1

    def anon_register_login_pipeline(self):
        """
        Pipeline completa del menú inicial del repo.
        """
        self.logoff()
        self.login_register_choice_menu()
        anon_choice = self.obtain_anon_choice()
        anon_choice()

    def add_product_to_list(self, product, user):
        self.data[user]["products"].append(product)

    def rm_product_from_list(self, product, user):
        self.data[user]["products"].remove(product)



if __name__ == "__main__":
    Database = DatabaseAccess()
    Database.anon_register_login_pipeline()