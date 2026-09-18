class User():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def menu(self):
        pass
    def get_my_data(self):
        pass

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
        self.data = {"admin":{"permissions":Admin, "password":"Admin123", "id":"001"}}
        self.choice_menu = {
            1:self.register,
            2:self.login,
            3:self.exit
        }
        self.user_clearance = {"admin":Admin, "user":User}
    def __repr__(self):
        return f"{self.users}"

    def register(self):
        pass
    def login(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if self.is_user(username, password):
                user = self.data[username]["permissions"]()
                # SEGUIR DESDE AQUÍ
        


    # Exit tiene toda la pinta de que va a ser temporal. Para hacer break en el loop.
    def exit(self):
        pass
    def login_register_choice_menu(self):
        print("----Sistema de Autenticación----")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

    def obtain_anon_choice(self):
        while True:
            anon_user_choice = int(input("Elija 1, 2 o 3: "))
            if anon_user_choice not in {1, 2, 3}:
                print("Opción fuera de las posibles.")
                continue
            break
        return self.choice_menu[anon_user_choice]()
    def is_user(self, username, password):
        return self.data[username]["password"] == password