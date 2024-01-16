#database_manager.py
from database_scripts.db_connectors import PostgresConnector, SQLiteConnector, MysqlConnector
from database_scripts.prompt_formatters import SchemaFormatter
from transformers import AutoTokenizer, AutoModelForCausalLM
from Manager.chat import OpenAIChatbot


class DatabaseManager:
    def __init__(self, database, user, password, host, port, db_type, openai_api_key):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_type = db_type
        self.tables = []
        self.formatter = None
        self.tokenizer = AutoTokenizer.from_pretrained("NumbersStation/nsql-350M")
        self.model = AutoModelForCausalLM.from_pretrained("NumbersStation/nsql-350M")
        self.openai_chatbot = OpenAIChatbot(api_key="sk-********************")

    def connect_to_database(self):
        
        if self.db_type == "1":
            connector = PostgresConnector(
                user=self.user, password=self.password, dbname=self.database, host=self.host, port=self.port
            )
        elif self.db_type == "2":
            connector = SQLiteConnector(database_path=self.database)
        elif self.db_type == "3":
            connector = MysqlConnector(
                user=self.user, password=self.password, dbname=self.database, host=self.host, port=self.port
            )
        else:
            raise ValueError("Type de base de données non prise en charge")

        connector.connect()

        if len(self.tables) <= 0:
            self.tables.extend(connector.get_tables())

        print(f"Liste des Tables présentes dans la base de données: {self.tables}")

        db_schema = [connector.get_schema(table) for table in self.tables]
        self.formatter = SchemaFormatter(db_schema, db_type=self.db_type)

    def initialize_model(self):
        model_name = "NumbersStation/nsql-350M"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)


    def execute_query(self, query):
        if self.formatter is None:
            raise ValueError("Connexion avec la base de données non établie")

        
        if self.db_type == "1":
            connector = PostgresConnector(
                user=self.user, password=self.password, dbname=self.database, host=self.host, port=self.port
            )
        elif self.db_type == "2":
            connector = SQLiteConnector(database_path=self.database)
        elif self.db_type == "3":
            connector = MysqlConnector(
                user=self.user, password=self.password, dbname=self.database, host=self.host, port=self.port
            )
        else:
            raise ValueError("Type de base de données non prise en charge")

        connector.connect()
        results = connector.run_sql_as_df(query)
        return results

    def display_results(self, results):
        print("Résultats de l'exécution de la requête :")
        print(results)

    def run_query(self, prompt):
        if self.formatter is None:
            raise ValueError("Connexion avec la base de données non établie")

        # Formatez la requête de l'utilisateur
        formatted_prompt = self.formatter.format_prompt(prompt)

        # Générez la requête SQL
        input_ids = self.tokenizer(formatted_prompt, return_tensors="pt").input_ids
        generated_ids = self.model.generate(input_ids, max_length=4000)
        generated_query = 'SELECT' + self.tokenizer.decode(generated_ids[0], skip_special_tokens=True).split('SELECT')[-1]

        try:
            # Exécutez la requête dans la base de données
            results = self.execute_query(generated_query)

            # Affichez la requête générée
            print(f"Requête SQL générée: {generated_query}")

            # Affichez les résultats
            self.display_results(results)

            # Utilisez OpenAIChatbot pour générer une réponse en français
            french_response = self.openai_chatbot.generate_response(prompt, str(results))
            print(f"Réponse en Français générée: {french_response}")

            # Retournez les résultats
            return results
        except Exception as e:
            # Affichez l'erreur s'il y en a une
            print(f"Erreur lors de la génération ou de l'exécution de la requête : {e}")
            return str(e)





     
        
    


# Salesforce : CODE 
# Numberstation : NSQL: 350M, 6B, 3B 
# dates 
# 4000tokens

# LLama -> NSQL-Llama-7-2B

# RAG 

# Text-to-SQL LLamaIndex-BDD->GeneratedAnswer

# types de bases de données

# fenêtre contextuelle = 4000 tokens / 1280000 tokens for OpenAI

# PROMPT = SCHEMA + QUESTION + SELECT 
# +4000 TOKENS == ERREURS (SUPÉRIEURE)

# LATENCE = 2s, 

# Modèles : Explanations !

# NumberStations : Entreprise
# Solutions à l'analyse de données

# Text -> SQL : 
# Text -> Code (sql, java, c, python, etc) : CodeGEN
# NSQL : 3 tailles de modèles : 350M, 2B, 6B 

# Llama: Text -> SQL



