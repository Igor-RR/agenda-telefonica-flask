import json
import os
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)
ARQUIVO_DADOS = "contatos.json"

# Template Jinja2 embutido diretamente como string no código Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Monolito Flask + JSON (Arquivo Único)</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
        form { margin-bottom: 20px; display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 8px; }
        button { padding: 8px 16px; background: #007BFF; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        ul { padding-left: 20px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <h1>Agênda telefônica</h1>
    
    <form action="/adicionar" method="POST">
        <input type="text" name="nome" placeholder="Nome do contato..." required>
        <input type="text" name="telefone" placeholder="Telefone..." required>
        <button type="submit">Salvar</button>
    </form>

    <h2>Lista de Contatos</h2>
    <ul>
        {% if contatos %}
            {% for contato in contatos %}
                <li><strong>{{ contato.nome }}</strong> - {{ contato.telefone }}</li>
            {% endfor %}
        {% else %}
            <p>Nenhum contato cadastrado ainda.</p>
        {% endif %}
    </ul>
</body>
</html>
"""


def carregar_dados():
  """Lê os dados do arquivo JSON em disco."""
  if not os.path.exists(ARQUIVO_DADOS):
    return []
  with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return []


def salvar_dados(dados):
  """Grava os dados de volta no arquivo JSON em disco."""
  with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)


@app.route("/")
def index():
  contatos = carregar_dados()
  # Renderiza o Jinja2 direto da string embutida
  return render_template_string(HTML_TEMPLATE, contatos=contatos)


@app.route("/adicionar", methods=["POST"])
def adicionar():
  nome = request.form.get("nome")
  telefone = request.form.get("telefone")

  if nome and telefone:
    contatos = carregar_dados()
    contatos.append({"nome": nome, "telefone": telefone})
    salvar_dados(contatos)

  return redirect("/")


if __name__ == "__main__":
  app.run(debug=True)