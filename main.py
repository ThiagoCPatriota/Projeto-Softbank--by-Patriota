import flet as ft
from defs import *

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 800
    page.alignment = ft.alignment.center 

    page.appbar = ft.AppBar(
        leading = ft.Icon(ft.Icons.ACCOUNT_BALANCE_SHARP),
        title = ft.Text('SoftBank'),
        center_title = True,
        bgcolor = ft.colors.RED,
    )

    CadastroOuLogin(page)
    page.update()

ft.app(main) 