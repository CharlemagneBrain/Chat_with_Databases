from db_connectors import PostgresConnector, SQLiteConnector, MysqlConnector
from prompt_formatters import RajkumarFormatter
from transformers import AutoTokenizer, AutoModelForCausalLM

class DatabaseManager:
    def __init__(self, database, user, password, host, port, db_type):
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
        self.formatter = RajkumarFormatter(db_schema, db_type=self.db_type)

    def initialize_model(self):
        model_name = "NumbersStation/nsql-350M"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def run_query(self, prompt):
        if self.formatter is None:
            raise ValueError("Connexion avec la base de données non établie")

        prompt = self.formatter.format_prompt(prompt)
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        generated_ids = self.model.generate(input_ids, max_length=1000)
        output = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        output = 'SELECT' + output.split('SELECT')[-1]

        print(output)


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



