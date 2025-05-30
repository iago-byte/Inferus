
import flet as ft
from training_tab import TrainingTab

TABS = ["Entrenamiento", "Inferencia", "Métricas", "Despliegue", "Configuración"]

def main(page: ft.Page):
    page.title = "Plataforma MLOps - Cliente"
    page.horizontal_alignment = "stretch"
    page.scroll = ft.ScrollMode.AUTO

    inferencia_tab = ft.Column([
        ft.Text("Inferencia sobre imágenes"),
        ft.Text("(Carga de imagen, visualización del resultado)"),
        ft.ElevatedButton("Seleccionar imagen"),
        ft.ElevatedButton("Inferir")
    ])

    metricas_tab = ft.Column([
        ft.Text("Comparativa de modelos y versiones"),
        ft.Text("(Gráficas, tabla comparativa, métricas clave)")
    ])

    despliegue_tab = ft.Column([
        ft.Text("Despliegue de modelos en Triton"),
        ft.Text("(Selector de modelo, exportación ONNX, botón desplegar)"),
        ft.ElevatedButton("Exportar"),
        ft.ElevatedButton("Generar config.pbtxt"),
        ft.ElevatedButton("Desplegar en Triton")
    ])

    configuracion_tab = ft.Column([
        ft.Text("Configuraciones generales del sistema"),
        ft.TextField(label="Dirección núcleo"),
        ft.TextField(label="Puerto Triton"),
        ft.Switch(label="Logs extendidos")
    ])

    tab_view = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Entrenamiento", content=TrainingTab()),
            ft.Tab(text="Inferencia", content=inferencia_tab),
            ft.Tab(text="Métricas", content=metricas_tab),
            ft.Tab(text="Despliegue", content=despliegue_tab),
            ft.Tab(text="Configuración", content=configuracion_tab),
        ]
    )

    page.add(tab_view)

ft.app(target=main)