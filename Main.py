from Database_Manager import DatabaseManager
import warnings

warnings.filterwarnings("ignore")

def get_database_manager():

    print("========= Bienvenue dans notre Application Text-to-SQL =========\n")

    print("Voici les types de Bases de données prises en charge : \n")
    print(" 1. Postgresql")
    print(" 2. SQLite")
    print(" 3. Mysql")

    db_type = ""
    while db_type not in ["1", "2", "3"]:
        db_type = input("Veuillez entrer le type de Base de Données en spécifiant le numéro correspondant : ")

    try:
        if db_type == "2":
            database = input("Saisissez le chemin de votre base de données : ")
            return DatabaseManager(database, "", "", "", "", db_type)
        else:
            database = input("Saisissez le nom de votre base de données : ")
            user = input("Saisissez le nom d'utilisateur : ")
            password = input("Faites entrer le mot de passe : ")
            host = input("Saisissez le host : ")
            port = int(input("Saisissez le port : "))
            return DatabaseManager(database, user, password, host, port, db_type, "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")

    except ValueError as ve:
        print(f"Erreur : {ve}")
        return None

if __name__ == "__main__":
    
    manager = get_database_manager()

    if manager is not None:
        try:
            manager.connect_to_database()
            manager.initialize_model()

            while True:
                prompt = input("Saisissez votre question (tapez 'exit' pour sortir de l'application) : ")

                if prompt.lower() == 'exit':
                    print("À bientôt")
                    break

                try:
                    manager.run_query(prompt)
                except Exception as e:
                    print(f"Erreur lors de la génération de la requête : {e}")
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")



# from Database_Manager import DatabaseManager

# if __name__ == "__main__":

#     DB_TYPE = input("Enter database type (Postgresql, SQLite, Mysql): ")
#     PORT = int(input("Enter port: "))
#     DATABASE = input("Enter database: ")
#     USER = input("Enter user: ")
#     PASSWORD = input("Enter password: ")
#     HOST = input("Enter host: ")
    

#     manager = DatabaseManager(DATABASE, USER, PASSWORD, HOST, PORT, PROMPT, DB_TYPE)
#     manager.connect_to_database()

#     while True:

#         PROMPT = input("Enter prompt: ")

#         if PROMPT == "exit":
#             break
#         manager.run_query()



# Which newspapers published data after 1992?  
# List of customers who have made a payment since 2004



# 1. TEXT -> 2. SQL REQUEST -> 3. INFERENCE -> 4. RESULT 
                                            # -> 5. Llama-2-chat : Giving the question and the result, build a correct answer 
                                            # -> 6. Print the generated answer




