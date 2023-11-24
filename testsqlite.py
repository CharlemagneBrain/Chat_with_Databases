import sqlite3
import sqlalchemy

database_path = '/home/charlie/Documents/Chinook.db'
uri = f"sqlite:///{database_path}"
# ensure we can actually connect to this SQLite uri
engine = sqlalchemy.create_engine(uri)
conn = engine.connect()

print(uri)

# # Remplacez "ma_base_de_donnees.db" par le chemin de votre fichier de base de données SQLite
# 

# # Connexion à la base de données en utilisant l'URI
# conn = sqlite3.connect(database_uri)

# # Création d'un curseur pour exécuter des requêtes SQL
# cur = conn.cursor()


# # Récupération et affichage des données
# cur.execute("SELECT * FROM album")
# utilisateurs = cur.fetchall()

# for utilisateur in utilisateurs:
#     print(utilisateur)

# # Fermer la connexion à la base de données
# conn.close()


