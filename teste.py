import flet as ft
def main(page: ft.Page):
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home")
        ],
    )
        
    page.add(nav_bar)
    page.update()

ft.app(main) 