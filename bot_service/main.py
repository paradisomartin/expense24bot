import os
import psycopg2
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from flask import Flask, request, jsonify

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = 'expensebot'
DB_HOST = 'db'

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Conectar a la base de datos
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )

# Inicializar LangChain
llm = OpenAI(temperature=0, api_key=OPENAI_API_KEY)
prompt = PromptTemplate(
    input_variables=["expense"],
    template="Categorize this expense into one of the following categories: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, Other. Expense: {expense}"
)
chain = LLMChain(llm=llm, prompt=prompt)

def is_valid_user(telegram_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
            return cur.fetchone() is not None

def categorize_expense(expense_text):
    return chain.run(expense_text).strip()

def parse_expense(message):
    # Implementar lógica para extraer descripción y monto del mensaje
    # Por ejemplo: "Pizza 20 bucks" -> ("Pizza", 20)
    parts = message.split()
    amount = float(parts[-2])
    description = ' '.join(parts[:-2])
    return description, amount

def add_expense(user_id, description, amount, category):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO expenses (user_id, description, amount, category, added_at) VALUES (%s, %s, %s, %s, NOW())",
                (user_id, description, amount, category)
            )
        conn.commit()

def process_message(telegram_id, message):
    if not is_valid_user(telegram_id):
        return "Unauthorized user"

    try:
        description, amount = parse_expense(message)
        category = categorize_expense(description)
        user_id = get_user_id(telegram_id)
        add_expense(user_id, description, amount, category)
        return f"{category} expense added ✅"
    except Exception as e:
        return f"Error processing expense: {str(e)}"

def get_user_id(telegram_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
            result = cur.fetchone()
            return result[0] if result else None

app = Flask(__name__)

@app.route('/process_message', methods=['POST'])
def handle_message():
    data = request.json
    telegram_id = data['telegram_id']
    message = data['message']
    result = process_message(telegram_id, message)
    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
