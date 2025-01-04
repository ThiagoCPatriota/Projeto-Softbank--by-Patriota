from database import db, User, Account
import flet as ft

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
                        size=20
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('LOGIN', color = ft.colors.WHITE),
                        bgcolor = "#0D47A1",
                        on_click = lambda e: Login(page)
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('CADASTRAR', color = ft.colors.WHITE),
                        bgcolor = "#0D47A1",
                        on_click = lambda e: Cadastro(page)
                    ),
                    ft.CupertinoButton(
                        content = ft.Text('SAIR', color = ft.colors.WHITE),
                        bgcolor = "#0D47A1",
                        on_click = lambda e: page.window_close()
                    ),
                    
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            alignment = ft.alignment.center,

        )
    )
    page.update()

#CPF VALIDO PARA TESTES:    64042544096
def validador_cpf(cpf):
    cpf_c = ''
    aux = 10
    result = 0
    for i in range(9):
        cpf_c += cpf[i]
    for i in range(9):
        result += int(cpf_c[i]) * aux
        aux -= 1
    result = (result*10)%11
    result = result if result < 10 else 0
    cpf_c += str(result)

    result = 0
    aux = 11
    for i in range(10):
        result += int(cpf_c[i]) * aux
        aux -= 1
    result = (result*10)%11
    result = result if result < 10 else 0
    cpf_c += str(result)
    if cpf_c == cpf:
        return True
    return False

def Login(page):
    email = ft.TextField(label='Digite seu email:')
    senha = ft.TextField(label='Digite sua senha:', password=True)
    cpf = ft.TextField(label='Digite seu cpf(apenas números):', max_length=11)
    mensagem = ft.Text(value='')

    def Confirma_login(e):
        mensagem.color='RED'
        if not email.value:
            mensagem.value = 'Porfavor, Insira um nome válido!'
        elif not email.value:
            mensagem.value = 'Porfavor, Insira um email válido!'
        elif not cpf.value:
            mensagem.value = 'Porfavor, Insira uma senha válida!'
        else:
            try:
                User.get(User.email == email.value and User.senha == senha.value and User.cpf == cpf.value)
                conta = Account.get(Account.usuario == email.value)
                mensagem.value = 'Login Realizado com Sucesso!'
                mensagem.color = 'green'
                Menu_Principal(page, conta)
                page.add(mensagem)
            except Exception as ex:
                mensagem.value = f'Erro ao Logar: {ex}'
                mensagem.color = 'red'
        page.update()

    page.controls.clear()
    page.controls.append(ft.Text('CADASTRO: '))
    page.add(
        email,
        senha,
        cpf,
        ft.Container(
            content = ft.Row(
                controls = [
                    ft.ElevatedButton(
                        content = ft.Text('Logar', color = ft.colors.WHITE),
                        bgcolor = "#0D47A1",
                        on_click=lambda e: Confirma_login(page)
                        ),
                    ft.ElevatedButton(
                        content = ft.Text('Voltar', color = ft.colors.WHITE), 
                        bgcolor = "#0D47A1",
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
                        bgcolor = "#0D47A1",
                        on_click=lambda e: Confirmar_Cadastro(page)
                        ),
                    ft.ElevatedButton(
                        content = ft.Text('Voltar', color = ft.colors.WHITE), 
                        bgcolor = "#0D47A1",
                        on_click=lambda e: CadastroOuLogin(page)
                        ),
                ],
            ), 
        ),  
        mensagem
    )
    page.update()
# 64042544096

def Nav(page):
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.ATTACH_MONEY_SHARP, label="Saque")
        ],
    )

def Menu_Principal(page, conta):
    page.controls.clear()
    Nav(page)
    page.update()
