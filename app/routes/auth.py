from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from werkzeug.security import check_password_hash

from app.models.usuario import Usuario
from app.services.usuario_service import UsuarioService


auth_bp = Blueprint(
    "auth",
    __name__,
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard.dashboard")
        )

    if request.method == "POST":

        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        user = Usuario.query.filter_by(
            usuario=usuario,
            ativo=True,
        ).first()

        if user and check_password_hash(
            user.senha_hash,
            senha,
        ):

            login_user(user)

            return redirect(
                url_for("dashboard.dashboard")
            )

        flash(
            "Usuário ou senha inválidos.",
            "danger",
        )

    return render_template(
        "auth/login.html"
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sessão encerrada.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )


@auth_bp.route(
    "/alterar-senha",
    methods=["GET", "POST"],
)
@login_required
def alterar_senha():

    if request.method == "POST":

        senha_atual = request.form.get(
            "senha_atual"
        )

        nova_senha = request.form.get(
            "nova_senha"
        )

        confirmar = request.form.get(
            "confirmar"
        )

        if nova_senha != confirmar:

            flash(
                "As senhas não conferem.",
                "warning",
            )

            return redirect(
                url_for("auth.alterar_senha")
            )

        ok, mensagem = UsuarioService.alterar_senha(
            current_user,
            senha_atual,
            nova_senha,
        )

        flash(
            mensagem,
            "success" if ok else "danger",
        )

        if ok:

            return redirect(
                url_for("dashboard.dashboard")
            )

    return render_template(
        "auth/alterar_senha.html"
    )
