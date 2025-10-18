import flet as ft

from frontend.grid_view import AnimeGrid
from frontend.main_page import MainPage


def main(page: ft.Page):
    page.title = "Anime Recommendation"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    anime_grid = AnimeGrid(page=page)
    main_page = MainPage(page=page, grid=anime_grid)

    page.add(
        ft.Container(
            content=main_page.build_page(),
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(
        target=main,
        host="192.168.3.17",
        port=8228,
        view=ft.WEB_BROWSER,
        use_color_emoji=True,
        assets_dir="assets",
    )