import os
import requests
import ast
import subprocess

API_URL = "https://api.deepinfra.com/v1/inference/meta-llama/Meta-Llama-3.1-70B-Instruct"
API_TOKEN = "bcTuVyDUpz0vyRUbKvnSBTeNpeMFv3oh"


headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def est_python_valide(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print("Erreur de syntaxe détectée :", e)
        return False

def corriger_code(code_source: str, bug_description: str = "") -> str:
    prompt = {
        "input": f"""[INST] Tu es un expert Python. Un bug a été identifié dans le code suivant. Voici la description du bug : 

{bug_description}

Corrige ce bug dans le code suivant. Retourne uniquement le code corrigé, sans explication.

Code :
{code_source}
[/INST]"""
    }


    try:
        response = requests.post(API_URL, headers=headers, json=prompt)
        response.raise_for_status()
        
        result = response.json()
        print("Réponse API:", result)  # Pour le debug
        
        if "results" in result and len(result["results"]) > 0:
            # Nettoyage du code généré
            code = result["results"][0]["generated_text"]
            code = code.replace("[CODE]", "").replace("[/CODE]", "").replace("[/INST]", "").strip()
            return code
        return ""
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel API : {e}")
        return ""

def verifier_et_corriger(bug_description: str = ""):
     # Utiliser le chemin dans le dossier Clone
    fichier = os.path.join("C:\\Users\\timos\\Desktop\\Clone", "test_sample.py")
    
    # Vérifier si le fichier existe dans le dépôt cloné
    if not os.path.exists(fichier):
        print("❌ Fichier test_sample.py non trouvé dans le dépôt Git")
        return
        
    with open(fichier, "r", encoding="utf-8") as f:
        code_source = f.read()

    if not code_source.strip():
        print("Fichier vide. Rien à corriger.")
        return

    print("🔍 Code original :")
    print(code_source)

    print("\n⚙️ Envoi au modèle Meta-Llama-3...")  # Mise à jour du message
    code_corrige = corriger_code(code_source, bug_description)

    if not code_corrige:
        print("❌ Aucun code corrigé reçu.")
        return

    print("\n✅ Code corrigé :")
    print(code_corrige)

    if not est_python_valide(code_corrige):
        print("❌ Code généré invalide. Correction ignorée.")
        return

    with open("exemple_corrige.py", "w", encoding="utf-8") as f:
        f.write(code_corrige)

    # Modifier le chemin pour écrire dans le dossier Clone
    output_path = os.path.join("C:\\Users\\timos\\Desktop\\Clone", "exemple_corrige.py")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code_corrige)


    print("🧪 Exécution des tests...")
    result = subprocess.run(["pytest", "test_exemple.py"], capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print("❌ Les tests ont échoué.")
