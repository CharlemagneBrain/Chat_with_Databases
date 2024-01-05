<p align="center">
  <a href="" rel="noopener">
 <img src="toybizapp.png" alt="Project logo"></a>
</p>
<h3 align="center">Talk tO Your BusIness PROJECT - TOYBIZ</h3>

<div align="center">

<!-- [![Chat](https://img.shields.io/badge/hackathon-name-orange.svg)](http://hackathon.url.com)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.md) -->

</div>

---

<p align="center"> Chat with your own Mysql, Postgresql and SQLite Databases in French
    <br> 
</p>

## 📝 Table of Contents

- [AIM](#problem_statement)
- [Workflow](#idea)
- [Limitations](#limitations)
- [Future Scope](#future_scope)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## 🧐 AIM <a name = "problem_statement"></a>

TOYBIZ's main objective is to create an AI assistant that will enable decision-makers to obtain quick and accurate answers to their business-related questions, whether in text or audio form. The aim is to simplify the decision-making process and increase the efficiency of decision-makers.

- IDEAL: Supporting both text and audio inputs, TOYBIZ allows users to interact with the AI assistant in a way that suits their preferences and requirements. TOYBIZ seamlessly integrates with different database systems, including MongoDB, PostgreSQL, SQLite, and MySQL, providing versatility to users with diverse data infrastructure.
- REALITY: TOYBIZ's current implementation includes functionalities for text-based interactions with its AI assistant. Users can pose questions related to their databases in natural language, and TOYBIZ will generate SQL queries using a language model. The system supports various database systems such as PostgreSQL, SQLite, and MySQL, enhancing flexibility and compatibility.

- CONSEQUENCES: TOYBIZ accelerates the decision-making process by providing quick and accurate responses to business-related queries. The integration of a language model streamlines the interaction, enabling decision-makers to obtain insights rapidly. The current implementation focuses on text-based interactions, allowing users to articulate questions in natural language. TOYBIZ utilizes a language model to generate SQL queries, facilitating a user-friendly experience for those familiar with standard language queries. TOYBIZ's adaptability extends to supporting different database systems, including PostgreSQL, SQLite, and MySQL. This flexibility enhances compatibility with various databases commonly used in business environments.


## 💡 Workflow <a name = "idea"></a>
                   +------------------------------------+
                   |                                    |
                   |           Application               |
                   |                                    |
                   +------------------------------------+
                                |
                                v
                   +------------------------------------+
                   |                                    |
                   |              User Input             |
                   |              (Text Prompt)          |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |   Open-source Finetuned LLM          |
                   |   (NumbersStation/nsql-350M)         |
                   |                                    |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |        SQL Request Generation        |
                   |         (Text to SQL Conversion)     |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |       Database Connection            |
                   |       (Postgres, SQLite, Mysql)       |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |         Execute SQL Query            |
                   |                                    |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |         Query Results                |
                   |       (Data from Database)           |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |    GPT-3 Language Model Inference   |
                   |         (Question + Result)          |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |      Constructed Answer              |
                   |    (Generated by GPT-3)              |
                   +------------------+-----------------+
                                      |
                                      v
                   +------------------+-----------------+
                   |                                    |
                   |        Print Generated Answer        |
                   |                                    |
                   +------------------------------------+

- **`db_connectors.py`:**
   - Contains connectors for PostgreSQL, SQLite and MySQL, allowing connection and execution of SQL queries.

- **`prompt_formatters.py`:**
   - Contains the `RajkumarFormatter` class which formats database schemas for SQL queries.

- **`Database_Manager.py`:**
   - Implements the `DatabaseManager` class which manages the connection to the database, the initialization of the language model, the execution of SQL queries, and the display of results.

- **`Main.py`:**
   - Main file allowing the user to specify the database type, provide login information and interact with the database by asking questions.

- **`nsql_streamlit.py`:**
   - File intended for use with Streamlit to create an interactive user interface for the Text-to-SQL application. The interface will make it easy to connect to the database, enter queries and view results.


## ⛓️ Limitations <a name = "limitations"></a>

- Limit of the model for some complex questions
- Latency of each inference questions


## 🚀 Future Scope <a name = "future_scope"></a>

- Select a better model for Text to SQL task
- Go futher for Speech to Text

## 🏁 Getting Started <a name = "getting_started"></a>

To run the application, follow this instructions

### Prerequisites

Version of Python : 3.8.18
Version of PIP : 23.3.1 <br/>
After cloning this project, run :

```
pip install -r requirements.txt
```

### Installing

Put your openai key in Database_Manager.py file

```
sk-********************************
```

Then download the different models by running :

```python

model_nsllama = "NumbersStation/nsql-llama-2-7B"
tokenizer = AutoTokenizer.from_pretrained(model_nsllama)
model = AutoModelForCausalLM.from_pretrained(model_nsllama, torch_dtype=torch.bfloat16)

```

## 🎈 Usage <a name="usage"></a>

After configure your database, run : 

```
streamlit run nsql_streamlit.py
```

<!-- ## ⛏️ Built With <a name = "tech_stack"></a>

- [MongoDB](https://www.mongodb.com/) - Database
- [Express](https://expressjs.com/) - Server Framework
- [VueJs](https://vuejs.org/) - Web Framework
- [NodeJs](https://nodejs.org/en/) - Server Environment -->

## ✍️ Authors <a name = "authors"></a>

- [@CharlemagneBrain](https://github.com/CharlemagneBrain) 
- [@SomaDjakiss](https://github.com/SomaDjakiss)



## 🎉 Acknowledgments <a name = "acknowledgments"></a>

- https://github.com/NumbersStationAI/NSQL
- 
