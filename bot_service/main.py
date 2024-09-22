import os
import psycopg2
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = 'expensebot'
DB_HOST = 'db'

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

def test_db_connection():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()
                print("Conexión a la base de datos exitosa.")
                return True
    except Exception as e:
        print(f"Error al conectar con la base de datos: {str(e)}")
        return False

def test_llm_connection():
    try:
        llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
        prompt = PromptTemplate(
            input_variables=["product"],
            template="What is a good name for a company that makes {product}?"
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run("colorful socks")
        print(f"Conexión con LLM exitosa. Respuesta de ejemplo: {result}")
        return True
    except Exception as e:
        print(f"Error al conectar con LLM: {str(e)}")
        return False

if __name__ == "__main__":
    print("Iniciando pruebas de conexión...")
    db_success = test_db_connection()
    llm_success = test_llm_connection()

    if db_success and llm_success:
        print("Todas las conexiones fueron exitosas.")
    else:
        print("Hubo problemas con las conexiones. Revisa los mensajes anteriores.")
