import flet as ft

class AnimeGrid:
    """
    Виджет сетки, в котором находятся контейнеры с аниме контентом
    """
    def __init__(self, page:ft.Page):
        # Сетка в которой будут находиться контейнеры с контентом
        self.grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=200,
            spacing=10,
            run_spacing=10,
            controls=[]
        )

        self.page = page

    def get_anime_grid(self) -> ft.GridView:
        """
        Выдача сетки
        """
        return self.grid

    def add_anime(self, anime_data: list):
        """
        Добавление аниме в сетку
        """
        self.grid.controls.clear() # Перед тем как выдать рекомендации надо стереть старые
        if not isinstance(anime_data[0], str): # Если запрос прошел успешно и не вылезла ошибка
            for anime_dict in anime_data:
                title = anime_dict.get("title", "anime")
                image_url = anime_dict.get("image_url","")
                similarity = anime_dict.get("similarity", 0)
                genres = anime_dict.get("genres", "")
                themes = anime_dict.get("themes", "")
                score = anime_dict.get("score", 60)
                year = anime_dict.get("year", 9999)

                # добавляем рекомендацию в сетку
                self.grid.controls.append(
                    self._create_anime_card(
                        title=title,
                        image_url=image_url,
                        similarity=similarity,
                        genres=genres,
                        themes=themes,
                        score=score,
                        year=year
                    )
                )
            self.page.update()
        else:
            # При ошибке в выдаче рекомендаций, выводим всплывающее окно с ошибкой
            self._show_small_notification(anime_data[0])

    def _create_anime_card(
            self,
            title: str,
            image_url: str,
            similarity: float,
            genres: str,
            themes: str,
            score: float,
            year: int,

    ) -> ft.Container:
        """
        Создаем контейнер с аниме контентом
        Params:
            title: название аниме
            image_url: ссылка на фото самого аниме
            similarity: число - похожесть данного аниме (от 0 до 1)
            genres: жанры выводимой рекомендации
            themes: темы выводимой рекомендации
            score: оценка аниме
            year: год выхода аниме
        """
        # Укорачиваем название аниме
        anime_title = title
        if len(anime_title) > 16:
            anime_title = f"{anime_title[:14]}..."

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Изображение аниме
                    ft.Container(
                        content=ft.Image(
                            src=image_url,
                            fit=ft.ImageFit.COVER,
                            width=100,
                            height=120,
                            border_radius=5,
                        ),
                        alignment=ft.alignment.center,
                        on_click=lambda e: self._show_details(
                            e,
                            title=title,
                            image_url=image_url,
                            similarity=similarity,
                            genres=genres,
                            themes=themes,
                            score=score,
                            year=year
                        ) # вывод полной информации по аниме при нажатии на его картинку

                    ),
                    # Название аниме (укороченное из-за маленьких размеров контейнера)
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                anime_title,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                selectable=True
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=10,
                    )
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.BLACK,
            border_radius=10,
            padding=5,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.BLACK12,
                offset=ft.Offset(0, 2),
            ),
        )

    def _show_details(
            self,
            e,
            title: str,
            image_url: str,
            similarity: float,
            genres: str = "none",
            score: float = 0.0,
            themes: str = "",
            year: int = 9999

    ) -> None:
        """Показывает детали аниме при клике на картинку"""
        # Можем не показывать год выхода аниме, если он является выбросом (то есть больше 3000)
        year = ft.Text(f"Год: {int(year)}", size=12, text_align=ft.TextAlign.CENTER) if year < 3000 else ft.Text()

        # Объект окна для просмотра полной информации об аниме
        dialog = ft.AlertDialog(
            title=ft.Container(
                content=ft.Text(
                    title,
                    text_align=ft.TextAlign.CENTER,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    selectable=True
                ),
                width=250,
                alignment=ft.alignment.center,
            ),
            content=ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Image(
                            src=image_url,
                            width=180,
                            height=220,
                            fit=ft.ImageFit.COVER,
                            border_radius=4,
                        ),
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(bottom=5),
                    ),
                    ft.Text(f"Сходство: {similarity:.2f}", size=14, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Рейтинг: ⭐{score}", size=12, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Жанры: {genres}", size=12, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"Темы: {themes}", size=12, text_align=ft.TextAlign.CENTER),
                    year,

                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=5,
                height=400,
                width=250
            ),
            actions=[
                ft.Container(
                    content=ft.TextButton(
                        "Закрыть",
                        on_click=lambda _: self.page.close(dialog),
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.GREY_700,
                        )
                    ),
                    alignment=ft.alignment.center,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=ft.Colors.GREY_900,
            shape=ft.RoundedRectangleBorder(radius=5),

        )
        self.page.open(dialog)

    def _show_small_notification(self, message: str):
        """Маленькое уведомление внизу экрана для вывода ошибок"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message),
            duration=2000,
            bgcolor=ft.Colors.GREY_800,
        )
        self.page.snack_bar = snack_bar
        self.page.open(snack_bar)
        self.page.update()