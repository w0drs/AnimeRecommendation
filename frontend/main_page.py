import flet as ft

from config.config_file import SERVER_ADDRESS, MICROSERVICE_PORT
from grid_view import AnimeGrid
import requests

class MainPage:
    """
    Главная страница со всеми виджетами
    """
    def __init__(self, page: ft.Page, grid: AnimeGrid) -> None:
        self.page = page
        self.grid = grid # Объект класса сетки в которой находятся контейнеры с аниме контентом

        self._initialize_all_widgets()

    def _initialize_all_widgets(self):
        """
        Инициализация всех виджетов
        """
        # Текстовое поле для названия аниме
        self.AnimeTitleTextField = ft.TextField(
            label="Название аниме",
            width=300,
            height=60
        )
        # Текстовое поле для описания аниме
        self.AnimeSynopsisTextField = ft.TextField(
            label="Описание аниме",
            width=300,
            multiline=True,
            min_lines=3,
            height=120
        )
        # Кнопка получить рекомендации
        self.GetRecommendationButton = ft.ElevatedButton(
            "Найти рекомендации",
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            elevation=2,
            on_click=lambda e: self._get_recommendation(e),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=1),
                padding=5,
            )
        )

        # Контейнер со всеми виджетами
        self.all_page = ft.ListView(
            controls=[
                ft.Stack(
                    controls=[
                        # Картинка для аниме
                        ft.Container(
                            content=ft.Image(
                                src="background2.png",
                                fit=ft.ImageFit.COVER,
                                width=self.page.width,
                                height=self.page.height,
                                opacity=1,
                                error_content=ft.Text("Image does load correctly!"),
                                expand=True
                            ),
                            expand=True
                        ),
                        # Функциональные виджеты
                        ft.Container(
                            content=self._build_functional_widgets(),
                            alignment=ft.alignment.center,
                            expand=True
                        ),
                    ],
                ),
            ]
        )

    def _build_functional_widgets(self) -> ft.Column:
        """
        Создает контейнер со всеми функциональными виджетами
        """
        return ft.Column(
            controls=[
                ft.Container(height=300),  # Отступ сверху
                ft.Row(
                    controls=[
                        ft.Container(width=80, expand=True),  # Левый отступ
                        ft.Column(
                            controls=[
                                self.AnimeTitleTextField,
                                ft.Text("или"),
                                self.AnimeSynopsisTextField,
                                self.GetRecommendationButton
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Container(width=80, expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Container(
                    content=ft.Column(controls=[
                        self.grid.get_anime_grid(),
                    ]),
                    alignment=ft.alignment.center
                ),

                ft.Container(height=100, expand=True), # Отступ снизу
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def build_page(self) -> ft.ListView:
        """
        Возвращает все виджеты для страницы
        """
        return self.all_page

    def _get_recommendation(self, e) -> None:
        """
        Запрос на сервис по выдаче аниме рекомендаций
        """
        request = {
            "title":self.AnimeTitleTextField.value,
            "synopsis": self.AnimeSynopsisTextField.value,
            "k": 16
        }

        # Запрос на сервис
        data = requests.post(f"http://{SERVER_ADDRESS}:{MICROSERVICE_PORT}/recommend", json=request)
        json_data = data.json()
        # Обновление сетки с аниме
        self.grid.add_anime(json_data.get("recommendation"))