
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Configurar la ventana principal
Window.size = (500, 540)
Window.resizable = False

class HipotecaInversaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        pantalla = Screen()
        fondo = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            size_hint=(1, 1),
            md_bg_color=(0.93, 0.96, 1, 1)
        )

        tarjeta = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=("440dp", "480dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            padding=30,
            elevation=10,
            radius=[16],
            spacing=20,
        )

        titulo = MDLabel(
            text="Simulador de Hipoteca Inversa",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="40dp"
        )

        self.propiedad = MDTextField(
            hint_text="Valor de la propiedad",
            helper_text="Ejemplo: 200000",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )

        self.edad = MDTextField(
            hint_text="Edad del propietario",
            helper_text="Ejemplo: 70",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )

        self.tasa = MDTextField(
            hint_text="Tasa de interés anual (%)",
            helper_text="Ejemplo: 5",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )

        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, None),
            height="45dp",
            pos_hint={"center_x": 0.5}
        )

        boton_calcular = MDRaisedButton(
            text="Calcular",
            on_release=self.calcular,
            size_hint=(1, 1)
        )

        boton_limpiar = MDFlatButton(
            text="Limpiar",
            on_release=self.limpiar,
            size_hint=(1, 1)
        )

        botones.add_widget(boton_calcular)
        botones.add_widget(boton_limpiar)

        self.resultado = MDLabel(
            text="",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint=(1, None),
            height="60dp"
        )

        tarjeta.add_widget(titulo)
        tarjeta.add_widget(self.propiedad)
        tarjeta.add_widget(self.edad)
        tarjeta.add_widget(self.tasa)
        tarjeta.add_widget(botones)
        tarjeta.add_widget(self.resultado)

        fondo.add_widget(tarjeta)
        pantalla.add_widget(fondo)

        return pantalla

    def mostrar_error(self, mensaje):
        dialog = MDDialog(
            title="Error de entrada",
            text=mensaje,
            buttons=[
                MDFlatButton(
                    text="CERRAR",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def calcular(self, instance):
        errores = []

        try:
            valor = float(self.propiedad.text.strip())
        except ValueError:
            errores.append("El valor de la propiedad no es válido.")

        try:
            edad = int(self.edad.text.strip())
        except ValueError:
            errores.append("La edad debe ser un número entero.")

        try:
            tasa = float(self.tasa.text.strip()) / 100
        except ValueError:
            errores.append("La tasa debe ser un número.")

        if errores:
            self.mostrar_error("\n".join(errores))
            return

        # Cálculo simple teniendo en cuenta edad mínima
        factor_edad = max(0.3, (edad - 60) / 100)
        monto_mensual = (valor * factor_edad * tasa) / 12

        self.resultado.text = f"Monto mensual estimado:\n${monto_mensual:,.2f}"

    def limpiar(self, instance):
        self.propiedad.text = ""
        self.edad.text = ""
        self.tasa.text = ""
        self.resultado.text = ""


if __name__ == "__main__":
    HipotecaInversaApp().run()
