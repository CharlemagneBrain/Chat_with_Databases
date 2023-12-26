import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline

class LlamaTextGenerator:
    def __init__(self, model_dir="./llama-2-7b-chat-hf"):
        self.model = LlamaForCausalLM.from_pretrained(model_dir)
        self.tokenizer = LlamaTokenizer.from_pretrained(model_dir)
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=torch.bfloat16,
            device_map="cuda",
        )

    def generate_response(self, question, answer, num_return_sequences=1, max_length=4000):
        prompt = f"""
        Tu es un chatbot qui à partir d'une question et de sa reponse, construit des phrases cohérentes afin de retourner une réponse structurée en Français.

        Voici la question initiale de l'utilisateur : {question}, 
        Voici la réponse à la question par la base de données  : {answer}

        Affiche la reponse en Français en commençant par la phrase "Réponse : "

                """

        sequences = self.pipeline(
            prompt,
            do_sample=True,
            top_k=1,
            num_return_sequences=num_return_sequences,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=max_length,
        )

        generated_responses = [seq["generated_text"].strip() for seq in sequences]
        return generated_responses

# Utilisation de la classe
generator = LlamaTextGenerator()


question = "Which newspapers published data after 1992 ?"

answer = """ 0    Nutritional composition of six muscles
1    Plasma concentration of dihydro-vitamin K 
2    Comparison of Two Methods of Fiber Analysis
3                                   Quaker Oats Co. 02
4    Nutrient Composition of Carl Buddig 
 """

responses = generator.generate_response(question, answer)

for response in responses:
    print(response)

