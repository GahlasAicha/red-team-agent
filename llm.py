import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODELE = "gemini-3.5-flash-lite"

def appeler_gemini(prompt, max_essais=4):
    """Appelle Gemini en réessayant si le serveur est surchargé (503)."""
    for essai in range(max_essais):
        try:
            reponse = client.models.generate_content(
                model=MODELE,
                contents=prompt,
            )
            return reponse.text
        except errors.ServerError:
            attente = 2 ** essai
            print(f"Serveur occupé (503), nouvel essai dans {attente}s...")
            time.sleep(attente)
        except errors.ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                print("Quota dépassé pour Gemini.attente de 60s.")
                time.sleep(60)
            else: 
                raise
    raise Exception("Gemini indisponible après plusieurs essais")