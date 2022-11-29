# API e Admin para Gerenciamento de vendas e comissões

> A ideia do projeto é registrar vendas e calcular a comissão dos vendedores com base nas vendas feitas em dado período e nos percentuais de comissão cadastrados nos produtos vendidos.

## Prerequisitos

- Python 3.10.8

## Instalação

Passo a passo para rodar o projeto local

$ python3 -m venv /path/to/new/virtual/environment

- Ative o ambiente

$ pip install -r requirements.txt

- Crie a base de dados 'sales_management_db' e insira suas credenciais em sales_management > settings.py > DATABASES

$ python manage.py migrate

$ python manage.py createsuperuser

$ python manage.py runserver

Pronto. Agora você pode acessar seu localhost/admin e logar com as credenciais criadas.

## Tela

![1](https://raw.githubusercontent.com/rayanemsantos/proj-django-sales-management/screenshot.png)

## Funcionalidades

Via Django Admin

- Cadastrar produtos, clientes e vendedores.
- Configurar os dias da semana e os mínimos e máximos de comissão.

Via API

- CRUD de produtos, clientes, vendedores e vendas.
- Endpoint que permite obter a lista de vendedores com o valor total de comissões a ser pago a cada um pelas vendas de dado período.

## Rodar os testes

Com o env ativado, rode o seguinte comando:

$ python manage.py test

Para rodar por app, rode o seguinte o comando:

$ python manage.py test app

## Próximos passos

- Implementar autenticação via API para que vendedores consigam registrar as vendas e acompanhar suas comissões.
