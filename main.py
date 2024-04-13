import flet as ft
from core_engine import CoreEngine

def main(page: ft.Page):
    engine = CoreEngine(page)
    engine.run()

if __name__ == "__main__":
    ft.app(target=main)
