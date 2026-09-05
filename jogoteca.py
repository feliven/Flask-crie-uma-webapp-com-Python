# importa as rotas e inicia o servidor

from app import app

import views_game  # noqa: F401
import views_user  # noqa: F401

if __name__ == "__main__":
    app.run(debug=True, port=8000)  # inicia o servidor
