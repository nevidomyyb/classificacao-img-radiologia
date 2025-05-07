### Como iniciar o sistema

- Requer python >= 3.11

##### SETUP INICIAL 

- Na raiz do projeto usar o comando `poetry install`

- Criar o arquivo .env em `/classificacao_img_radiologia/.env`.
Com o conteúdo:
```
DATABASE = "classificacao_img_radiologia"
DB_USERNAME = ""
PASSWORD = ""
HOST = ""
PORT = "3306"
COOKIE_SALT = "ll2k4l1k!@3lsljkvlvcck2knMANNASm14444213"
```
> [!IMPORTANT]  
> SGBD MySQL

- Na raiz do projeto usar o comando `poetry run alembic upgrade head`
- Após isso é possível alterar qual a porta que a aplicação usará em `/.streamlit/config.toml` na propriedade **port**. Por padrão é usado a 8090
- Com tudo configurado, na raiz do projeto usar o comando `poetry run rst`

Com isso o sistema deverá ser iniciado na porta especificada.
