import streamlit as st
from Manager.Database_Manager import DatabaseManager
from Manager.chat import OpenAIChatbot  # Ajout de l'importation d'OpenAIChatbot
import warnings
from googletrans import Translator

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text


warnings.filterwarnings("ignore")

st.title("Chattez avec vos Données 🚀")

st.markdown(
    """
    Bienvenue dans notre application de Chat ! 😊\n
    Connectez-vous à votre **base de données** et explorez vos données de manière interactive. 📊\n
    Cette application prend en charge les bases de données **Postgresql, SQLite et Mysql**. 
    Posez vos questions directement en **Français**. 🇫🇷\n
    Laissez votre curiosité guider la conversation ! 💬
    
    """
)


# Clé API OpenAI
openai_api_key = "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"  

# Initialize database manager
if "manager" not in st.session_state:
    st.session_state.manager = None

# Initialize OpenAIChatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = OpenAIChatbot(api_key=openai_api_key)

# Sidebar for entering database information
st.sidebar.title("Connexion à la base de données")

db_type_mapping = {"": "0", "Postgresql": "1", "SQLite": "2", "Mysql": '3'}
db_type = st.sidebar.selectbox("Sélectionnez le type de base de données", list(db_type_mapping.keys()))

database = st.sidebar.text_input("Nom de la base de données ou son chemin")

if db_type != "" and db_type not in db_type_mapping:
    st.error("Type de base de données non pris en charge.")
    st.stop()

if db_type_mapping[db_type] != "2":
    user = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    host = st.sidebar.text_input("Host")
    port = st.sidebar.number_input("Port", value=5432)

# Button to connect to the database
if st.sidebar.button("Connexion") and st.session_state.manager is None:
    try:
        if db_type_mapping[db_type] == "2":
            st.session_state.manager = DatabaseManager(database, "", "", "", "", db_type_mapping[db_type], openai_api_key)
        else:
            st.session_state.manager = DatabaseManager(database, user, password, host, port, db_type_mapping[db_type], openai_api_key)

        st.session_state.manager.connect_to_database()
        st.session_state.manager.initialize_model()

        st.success("Connecté à la base de données et initialisé le modèle.")
    except Exception as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")

if st.session_state.manager is not None:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.text_input("Posez une question :"):
        # Translate the user's question to English
        translated_prompt = translate_text(prompt, target_language='en')

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            try:
                # Pass the translated question to the model to generate SQL
                results = st.session_state.manager.run_query(translated_prompt)

                # Generate the response in French with OpenAIChatbot
                french_response = st.session_state.chatbot.generate_response(prompt, str(results))

                # Display the generated query and results in the interface
                message_placeholder.markdown(f"\n{french_response}")

                # Add the assistant's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": f"\n{french_response}"})
            except Exception as e:
                message_placeholder.markdown(f"Erreur lors de la génération ou de l'exécution de la requête : {e}")

                # Add an error message to the chat history
                st.session_state.messages.append({"role": "assistant", "content": f"Erreur lors de la génération ou de l'exécution de la requête : {e}"})