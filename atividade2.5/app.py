# Esse 'url_for' foi recomendação de IA para gerar URLs de forma automática
from flask import Flask, render_template, request, redirect, url_for, make_response, session


app = Flask(__name__)
app.secret_key = "chave"

# Só criei 2 usuários mesmo, já que não precisa ter opção de cadastro deixei simples
usuarios = {
    "Lucas": "123",
    "Joao": "456"
}


@app.route("/")
def index():

    # pegando o nome do usuário
    usuario = session.get("usuario", ".")

    # pegando o nome do cookie específico para o usuário
    nome_cookie = f"visitas_{usuario}"

    # pegando o número de visitas a partir do cookie
    visitas = request.cookies.get(nome_cookie)

    # contador simples para registrar o número de visitas
    if visitas:
        visitas = int(visitas) + 1
    else:
        visitas = 1

    # Criando resposta para renderizar a página com as informações do usuário e número de visitas
    # OBS: como tem o 'render_template' as páginas 'index.html' e 'login.html' precisam estar na pasta 'templates'
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

# aqui é a rota de login, só tem o POST para mandar as informações pra login (e o GET para acessar a página de login)
@app.route("/login", methods=["GET", "POST"])
def login():

    # POST para logar
    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        # Verifica credenciais
        if usuario in usuarios and usuarios[usuario] == senha:

            session["usuario"] = usuario

            return redirect(url_for("index"))

        else:

            erro = "Usuário ou senha inválidos."

            return render_template(
                "login.html",
                erro=erro
            )

    return render_template("login.html")

# Rota de logout, só remove o usuário da sessão e redireciona para a página inicial
@app.route("/logout")
def logout():

    session.pop("usuario", None)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)