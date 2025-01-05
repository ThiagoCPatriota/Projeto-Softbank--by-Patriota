from database import db, User, Account
import flet as ft
import requests
from utilitarios import *

db.connect()
db.create_tables([User, Account])

def CadastroOuLogin(page):
    page.controls.clear()
    page.add(
        ft.Container(
            content = ft.Column(
                controls=[
                    ft.Text(
                        'Bem-Vindo(a) ao SoftBank',
                        size=20,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('LOGIN', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click = lambda e: Login(page)
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('CADASTRAR', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click = lambda e: Cadastro(page)
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('SAIR', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click = lambda e: page.window_close()
                    ),
                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment = ft.alignment.center,

        )
    )
    page.update()

def Login(page):
    email = ft.TextField(label='Digite seu email:')
    senha = ft.TextField(label='Digite sua senha:', password=True)
    cpf = ft.TextField(label='Digite seu cpf(apenas números):', max_length=11)
    mensagem = ft.Text(value='')

    def Confirma_login(e):
        mensagem.color='RED'
        if not email.value:
            mensagem.value = 'Porfavor, Insira um email válido!'
        elif not senha.value:
            mensagem.value = 'Porfavor, Insira um senha válido!'
        elif not cpf.value:
            mensagem.value = 'Porfavor, Insira uma senha válida!'
        else:
            usuario = User.get_or_none(User.email == email.value & User.senha == senha.value & User.cpf == cpf.value)

            if usuario:
                conta = Account.get(Account.email == email.value)
                mensagem.value = 'Login Realizado com Sucesso!'
                mensagem.color = 'green'
                Menu_Principal(page, conta)
                page.add(mensagem)
            else:
                mensagem.value = 'Usuário ou senha inválidos!'
                mensagem.color = 'red'
        page.update()

    page.controls.clear()
    page.controls.append(ft.Text('LOGIN: '))
    page.add(
        email,
        senha,
        cpf,
        ft.Container(
            content = ft.Row(
                controls = [
                    ft.ElevatedButton(
                        content = ft.Text('Logar', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click=lambda e: Confirma_login(page)
                        ),
                    ft.ElevatedButton(
                        content = ft.Text('Voltar', color = ft.colors.WHITE), 
                        bgcolor = '#0D47A1',
                        on_click=lambda e: CadastroOuLogin(page)
                        ),
                ],
            ), 
        ),  
        mensagem
    )
    page.update()

def Cadastro(page):
    page.controls.clear()
    nome = ft.TextField(label='Digite seu nome:')
    email = ft.TextField(label='Digite seu email:')
    senha = ft.TextField(label='Digite sua senha:', password=True)
    cpf = ft.TextField(label='Digite seu cpf(apenas números):', max_length=11)
    mensagem = ft.Text(value='')

    def Confirmar_Cadastro(e):
        mensagem.color='RED'
        if not nome.value:
            mensagem.value = 'Porfavor, Insira um nome válido!'
        elif not email.value:
            mensagem.value = 'Porfavor, Insira um email válido!'
        elif not senha.value:
            mensagem.value = 'Porfavor, Insira uma senha válida!'
        elif not cpf.value:
            mensagem.value = 'Porfavor, Insira uma CPF válido!'
        else:
            try:
                if validador_cpf(cpf.value):
                    User.create(nome=nome.value, email=email.value, senha=senha.value, cpf=cpf.value)
                    Account.create(email=email.value, usuario=nome.value, saldo=0)
                    mensagem.value = 'Cadastro Realizado com Sucesso!'
                    mensagem.color = 'green'
                    CadastroOuLogin(page)
                    page.add(mensagem)
            except Exception as ex:
                mensagem.value = f'Erro ao cadastrar: {ex}'
                mensagem.color = 'red'
        page.update()

    page.controls.clear()
    page.controls.append(ft.Text('CADASTRO: '))
    page.add(
        nome,
        email,
        senha,
        cpf,
        ft.Container(
            content = ft.Row(
                controls = [
                    ft.ElevatedButton(
                        content = ft.Text('Cadastrar', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click=lambda e: Confirmar_Cadastro(page)
                        ),
                    ft.ElevatedButton(
                        content = ft.Text('Voltar', color = ft.colors.WHITE), 
                        bgcolor = '#0D47A1',
                        on_click=lambda e: CadastroOuLogin(page)
                        ),
                ],
            ), 
        ),  
        mensagem
    )
    page.update()
# 64042544096

def Nav(page, conta):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.PERSON, label='Perfil'),
            ft.NavigationDestination(icon=ft.icons.CURRENCY_BITCOIN_SHARP, label='Moeda'),
            ft.NavigationDestination(icon=ft.icons.ATTACH_MONEY_SHARP, label='Saque'),
            ft.NavigationDestination(icon=ft.icons.MOVE_TO_INBOX_ROUNDED, label='Deposito'),
        ],
        on_change=lambda e: hot_bar(e, page, conta),
    )

def hot_bar(e, page, conta):
    if e.control.selected_index == 0:
        Perfil(page, conta)
    elif e.control.selected_index == 1:
        ExibirCotacaoDolar(page)
    elif e.control.selected_index == 2:
        Saque(page, conta)
    elif e.control.selected_index == 3:
        Deposito(page, conta)
    page.update()
    

def Perfil(page, conta):
    page.controls.clear()
    page.controls.append(ft.Text('Informações da Conta: '))
    page.controls.append(ft.Text(f'''
    NOME: {conta.usuario}
    EMAIL: {conta.email}

    SALDO: {conta.saldo}

    ''', size=15))
    page.update()

def ExibirCotacaoDolar(page):
    page.controls.clear()
    cotacao = obter_cotacao_bitcoin()
    page.controls.append(ft.Text(f'A cotação do Bitcoin hoje é:'))
    page.controls.append(ft.Text(f'R$ {cotacao}', size=24, weight='bold'))  
    page.update()

def Saque(page, conta):
    saq = ft.TextField(label='Quanto deseja sacar: ')
    mensagem = ft.Text(value='')
    mensagem.color='RED'
    def confirmar_saque(e):
        valor_saque = float(saq.value)
        if valor_saque > conta.saldo:
            mensagem.value = 'Saque maior que o saldo da conta, tentativa negada!'
        elif not saq.value:
            mensagem.value = 'Valor inválido.'
        elif valor_saque > 10000:
            mensagem.value = 'Saque maior que R$10000, tentativa negada!'
        else:
            try:
                conta.saldo -= valor_saque
                conta.save()
                mensagem.color = 'green'
                mensagem.value = f'Foram depositados na conta {conta.usuario}, R${saq.value}'
                page.update()
            except ValueError:
                mensagem.value = 'Valor inválido. Por favor, insira um número.'
        page.update()
    page.controls.clear()
    page.add(
        saq,
        ft.Container(
            content = ft.Row(
                controls = [
                    ft.ElevatedButton(
                        content = ft.Text('Sacar', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click=lambda e: confirmar_saque(page)
                        ),
                ],
            ), 
        ), 
        mensagem,
    )
    page.update()

def Deposito(page, conta):
    dep = ft.TextField(label='Quanto deseja Depositar: ')
    mensagem = ft.Text(value='')
    mensagem.color='RED'
    def confirmar_deposito(e):
        valor_saque = float(dep.value)
        if not dep.value:
            mensagem.value = 'Valor inválido.'
        else:
            try:
                conta.saldo += valor_saque
                conta.save()
                mensagem.color = 'green'
                mensagem.value = f'Foram depositados na conta {conta.usuario}, R${dep.value}'
                page.update()
            except ValueError:
                mensagem.value = 'Valor inválido. Por favor, insira um número.'
        page.update()
    page.controls.clear()
    page.add(
        dep,
        ft.Container(
            content = ft.Row(
                controls = [
                    ft.ElevatedButton(
                        content = ft.Text('Depositar', color = ft.colors.WHITE),
                        bgcolor = '#0D47A1',
                        on_click=lambda e: confirmar_deposito(page)
                        ),
                ],
            ), 
        ), 
        mensagem,
    )
    page.update()

def Menu_Principal(page, conta):
    page.controls.clear()
    Perfil(page, conta)
    Nav(page, conta)
    page.update()
