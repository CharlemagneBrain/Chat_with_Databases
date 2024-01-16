import openai

class OpenAIChatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_response(self, question, database_answer):
        prompt = f"""
        Tu es un chatbot qui à partir d'une question et de sa réponse, construit des phrases cohérentes afin de retourner une réponse structurée en Français.

        Voici la question initiale de l'utilisateur : {question}
        Voici la réponse à la question par la base de données : {database_answer}

        Affiche la réponse en Français en commençant par la phrase "Réponse : "
        
        Toutefois si la question de l'utilisateur n'en est pas une et que la réponse, affiche simplement : Oups ! J'ai pas eu de réponse à ta question, peux tu eêtre plus précis s'il te plaît ? 
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

# api_key = "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"  
# chatbot = OpenAIChatbot(api_key)

# question = "Which newspapers published data after 1992 ?"

# database_answer = """ 0    Nutritional composition of six muscles
# 1    Plasma concentration of dihydro-vitamin K
# 2    Comparison of Two Methods of Fiber Analysis
# 3                                   Quaker Oats Co. 02
# 4    Nutrient Composition of Carl Buddig
#  """

# response = chatbot.generate_response(question, database_answer)
# print(response)