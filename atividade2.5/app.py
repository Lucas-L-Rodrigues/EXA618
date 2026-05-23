# Esse 'url_for' foi recomendação de IA para gerar URLs de forma automática
from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import make_response, session


app = Flask(__name__)

app.secret_key = "chave"

# Usuários fixos
usuarios = {
    "Lucas": "123",
    "Joao": "456"
}


@app.route("/")
def index():

    # Pegando usuário da sessão
    # Se não existir login, usa "."
    usuario = session.get("usuario", ".")

    # Nome do cookie específico do usuário
    nome_cookie = f"visitas_{usuario}"

    # Pegando número de visitas
    visitas = request.cookies.get(nome_cookie)

    # Incrementa contador
    if visitas:
        visitas = int(visitas) + 1
    else:
        visitas = 1

    # Cria resposta HTTP
    resposta = make_response(
        render_template(
            "index.html",
            usuario=usuario,
            visitas=visitas
        )
    )

    # Atualiza cookie
    resposta.set_cookie(
        nome_cookie,
        str(visitas)
    )

    return resposta


@app.route("/login", methods=["GET", "POST"])
def login():

    # POST → tentativa de login
    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # Verifica credenciais
        if usuario in usuarios and usuarios[usuario] == senha:

            # Cria sessão
            session["usuario"] = usuario

            # Redireciona para página inicial
            return redirect(url_for("index"))

        else:

            erro = "Usuário ou senha inválidos."

            return render_template(
                "login.html",
                erro=erro
            )

    # GET → mostra formulário
    return render_template("login.html")



@app.route("/perfil")
def perfil():

    # Verifica se usuário está logado
    if "usuario" not in session:
        return redirect(url_for("login"))

    # Pega usuário da sessão
    usuario = session["usuario"]

    # Renderiza página de perfil
    return render_template(
        "perfil.html",
        usuario=usuario
    )


@app.route("/logout")
def logout():

    # Remove usuário da sessão
    session.pop("usuario", None)

    # Redireciona para página inicial
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)