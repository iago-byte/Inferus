import flet as ft

def TrainingTab():
    estado_entrenamiento = ft.Text("Estado: Idle")
    barra_progreso = ft.ProgressBar(width=400, value=0)

    # Campos básicos
    modelo_dropdown = ft.Dropdown(
        label="Modelo",
        options=[ft.dropdown.Option("Unet"), ft.dropdown.Option("BiRefNet")],
        value="Unet",
    )

    backbone_dropdown = ft.Dropdown(
        label="Backbone",
        options=[ft.dropdown.Option("resnet34"), ft.dropdown.Option("efficientnet-b0")],
        value="resnet34",
    )

    num_clases = ft.TextField(label="Número de clases", value="3", width=200)
    dataset_path = ft.TextField(label="Ruta del dataset", value="", width=400)
    tile_size = ft.TextField(label="Tile size", value="512", width=200)
    stride = ft.TextField(label="Stride", value="384", width=200)
    batch_size = ft.TextField(label="Batch size", value="8", width=200)
    epochs = ft.TextField(label="Épocas", value="50", width=200)

    # Acciones
    def config_recomendada(e):
        batch_size.value = "16"
        modelo_dropdown.value = "Unet"
        backbone_dropdown.value = "resnet34"
        estado_entrenamiento.value = "Valores recomendados aplicados"
        e.control.page.update()

    def lanzar_entrenamiento(e):
        estado_entrenamiento.value = "Entrenando..."
        barra_progreso.value = None  # carga indeterminada por ahora
        e.control.page.update()
        # Aquí deberías hacer POST al núcleo

    config_rec_button = ft.ElevatedButton("Config. recomendada", on_click=config_recomendada)
    entrenar_button = ft.ElevatedButton("Entrenar", on_click=lanzar_entrenamiento)

    return ft.Column([
        ft.Text("Entrenamiento de modelos", style=ft.TextThemeStyle.HEADLINE_SMALL),
        modelo_dropdown,
        backbone_dropdown,
        num_clases,
        dataset_path,
        tile_size,
        stride,
        batch_size,
        epochs,
        ft.Row([config_rec_button, entrenar_button]),
        estado_entrenamiento,
        barra_progreso,
        ft.Text("Aquí irá la gráfica de pérdida/precisión")
    ])