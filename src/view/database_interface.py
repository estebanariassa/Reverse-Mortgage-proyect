from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
import sys
import os
from datetime import date

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Secret_config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
from src.controller.py.clientes_controller import ClientesController
from src.controller.py.propiedades_controller import PropiedadesController
from src.controller.py.hipotecas_controller import HipotecasController
from src.controller.py.herederos_controller import HerederosController
from src.model.clientes import Clientess
from src.model.propiedad import Propiedad
from src.model.hipoteca import Hipoteca
from src.model.heredero import Heredero

# Configurar la ventana principal
Window.size = (800, 600)
Window.resizable = True

class DatabaseInterfaceApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        # Crear el administrador de pantallas
        self.screen_manager = ScreenManager()
        
        # Pantalla principal
        self.main_screen = self.create_main_screen()
        self.screen_manager.add_widget(self.main_screen)
        
        # Pantalla de clientes
        self.clientes_screen = self.create_clientes_screen()
        self.screen_manager.add_widget(self.clientes_screen)
        
        # Pantalla de propiedades
        self.propiedades_screen = self.create_propiedades_screen()
        self.screen_manager.add_widget(self.propiedades_screen)
        
        # Pantalla de hipotecas
        self.hipotecas_screen = self.create_hipotecas_screen()
        self.screen_manager.add_widget(self.hipotecas_screen)
        
        # Pantalla de herederos
        self.herederos_screen = self.create_herederos_screen()
        self.screen_manager.add_widget(self.herederos_screen)
        
        return self.screen_manager

    def create_main_screen(self):
        """Crear la pantalla principal con navegación"""
        screen = Screen(name="main")
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(0.93, 0.96, 1, 1)
        )
        
        # Barra superior
        toolbar = MDTopAppBar(
            title="Sistema de Hipoteca Inversa",
            elevation=2,
            md_bg_color=(0.2, 0.6, 0.9, 1)
        )
        main_layout.add_widget(toolbar)
        
        # Tarjeta de bienvenida
        welcome_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="200dp",
            padding=30,
            elevation=5,
            radius=[16],
            spacing=20
        )
        
        welcome_title = MDLabel(
            text="Bienvenido al Sistema de Hipoteca Inversa",
            halign="center",
            font_style="H4",
            size_hint=(1, None),
            height="40dp"
        )
        
        welcome_text = MDLabel(
            text="Seleccione una opción del menú para gestionar los datos:",
            halign="center",
            font_style="Subtitle1",
            size_hint=(1, None),
            height="30dp"
        )
        
        welcome_card.add_widget(welcome_title)
        welcome_card.add_widget(welcome_text)
        
        # Botones de navegación
        nav_layout = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint=(1, None),
            height="300dp"
        )
        
        btn_clientes = MDRaisedButton(
            text="Gestionar Clientes",
            on_release=lambda x: self.switch_screen("clientes"),
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_propiedades = MDRaisedButton(
            text="Gestionar Propiedades",
            on_release=lambda x: self.switch_screen("propiedades"),
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_hipotecas = MDRaisedButton(
            text="Gestionar Hipotecas",
            on_release=lambda x: self.switch_screen("hipotecas"),
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_herederos = MDRaisedButton(
            text="Gestionar Herederos",
            on_release=lambda x: self.switch_screen("herederos"),
            size_hint=(1, None),
            height="50dp"
        )
        
        nav_layout.add_widget(btn_clientes)
        nav_layout.add_widget(btn_propiedades)
        nav_layout.add_widget(btn_hipotecas)
        nav_layout.add_widget(btn_herederos)
        
        main_layout.add_widget(welcome_card)
        main_layout.add_widget(nav_layout)
        
        screen.add_widget(main_layout)
        return screen

    def create_clientes_screen(self):
        """Crear pantalla para gestionar clientes"""
        screen = Screen(name="clientes")
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(0.93, 0.96, 1, 1)
        )
        
        # Barra superior con botón de regreso
        toolbar = MDTopAppBar(
            title="Gestión de Clientes",
            elevation=2,
            md_bg_color=(0.2, 0.6, 0.9, 1),
            left_action_items=[["arrow-left", lambda x: self.switch_screen("main")]]
        )
        main_layout.add_widget(toolbar)
        
        # Formulario de cliente
        form_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="400dp",
            padding=20,
            elevation=5,
            radius=[16],
            spacing=15
        )
        
        form_title = MDLabel(
            text="Datos del Cliente",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="30dp"
        )
        
        # Campos del formulario
        self.cedula_field = MDTextField(
            hint_text="Cédula",
            helper_text="Ejemplo: 12345678",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.nombre_field = MDTextField(
            hint_text="Nombre completo",
            helper_text="Ejemplo: Juan Pérez",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.edad_field = MDTextField(
            hint_text="Edad (65-90 años)",
            helper_text="Ejemplo: 70",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.direccion_field = MDTextField(
            hint_text="Dirección",
            helper_text="Ejemplo: Calle 123 #45-67",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.telefono_field = MDTextField(
            hint_text="Teléfono",
            helper_text="Ejemplo: 3001234567",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.correo_field = MDTextField(
            hint_text="Correo electrónico",
            helper_text="Ejemplo: juan@email.com",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        # Botones de acción
        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_insertar = MDRaisedButton(
            text="Insertar",
            on_release=self.insertar_cliente,
            size_hint=(1, 1)
        )
        
        btn_buscar = MDRaisedButton(
            text="Buscar",
            on_release=self.buscar_cliente,
            size_hint=(1, 1)
        )
        
        btn_limpiar = MDFlatButton(
            text="Limpiar",
            on_release=self.limpiar_formulario_cliente,
            size_hint=(1, 1)
        )
        
        btn_layout.add_widget(btn_insertar)
        btn_layout.add_widget(btn_buscar)
        btn_layout.add_widget(btn_limpiar)
        
        # Agregar widgets al formulario
        form_card.add_widget(form_title)
        form_card.add_widget(self.cedula_field)
        form_card.add_widget(self.nombre_field)
        form_card.add_widget(self.edad_field)
        form_card.add_widget(self.direccion_field)
        form_card.add_widget(self.telefono_field)
        form_card.add_widget(self.correo_field)
        form_card.add_widget(btn_layout)
        
        main_layout.add_widget(form_card)
        
        # Área de resultados
        self.resultado_cliente = MDLabel(
            text="",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint=(1, None),
            height="100dp"
        )
        main_layout.add_widget(self.resultado_cliente)
        
        screen.add_widget(main_layout)
        return screen

    def create_propiedades_screen(self):
        """Crear pantalla para gestionar propiedades"""
        screen = Screen(name="propiedades")
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(0.93, 0.96, 1, 1)
        )
        
        # Barra superior
        toolbar = MDTopAppBar(
            title="Gestión de Propiedades",
            elevation=2,
            md_bg_color=(0.2, 0.6, 0.9, 1),
            left_action_items=[["arrow-left", lambda x: self.switch_screen("main")]]
        )
        main_layout.add_widget(toolbar)
        
        # Formulario de propiedad
        form_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="350dp",
            padding=20,
            elevation=5,
            radius=[16],
            spacing=15
        )
        
        form_title = MDLabel(
            text="Datos de la Propiedad",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="30dp"
        )
        
        # Campos del formulario
        self.codigo_prop_field = MDTextField(
            hint_text="Código de propiedad",
            helper_text="Ejemplo: 1",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.cedula_cliente_prop_field = MDTextField(
            hint_text="Cédula del cliente",
            helper_text="Ejemplo: 12345678",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.valor_prop_field = MDTextField(
            hint_text="Valor de la propiedad (COP)",
            helper_text="Ejemplo: 200000000",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.direccion_prop_field = MDTextField(
            hint_text="Dirección de la propiedad",
            helper_text="Ejemplo: Calle 123 #45-67",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.area_prop_field = MDTextField(
            hint_text="Área (m²)",
            helper_text="Ejemplo: 120.5",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.tipo_prop_field = MDTextField(
            hint_text="Tipo de propiedad",
            helper_text="Ejemplo: Casa, Apartamento, Finca",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        # Botones de acción
        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_insertar = MDRaisedButton(
            text="Insertar",
            on_release=self.insertar_propiedad,
            size_hint=(1, 1)
        )
        
        btn_buscar = MDRaisedButton(
            text="Buscar",
            on_release=self.buscar_propiedad,
            size_hint=(1, 1)
        )
        
        btn_limpiar = MDFlatButton(
            text="Limpiar",
            on_release=self.limpiar_formulario_propiedad,
            size_hint=(1, 1)
        )
        
        btn_layout.add_widget(btn_insertar)
        btn_layout.add_widget(btn_buscar)
        btn_layout.add_widget(btn_limpiar)
        
        # Agregar widgets al formulario
        form_card.add_widget(form_title)
        form_card.add_widget(self.codigo_prop_field)
        form_card.add_widget(self.cedula_cliente_prop_field)
        form_card.add_widget(self.valor_prop_field)
        form_card.add_widget(self.direccion_prop_field)
        form_card.add_widget(self.area_prop_field)
        form_card.add_widget(self.tipo_prop_field)
        form_card.add_widget(btn_layout)
        
        main_layout.add_widget(form_card)
        
        # Área de resultados
        self.resultado_propiedad = MDLabel(
            text="",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint=(1, None),
            height="100dp"
        )
        main_layout.add_widget(self.resultado_propiedad)
        
        screen.add_widget(main_layout)
        return screen

    def create_hipotecas_screen(self):
        """Crear pantalla para gestionar hipotecas"""
        screen = Screen(name="hipotecas")
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(0.93, 0.96, 1, 1)
        )
        
        # Barra superior
        toolbar = MDTopAppBar(
            title="Gestión de Hipotecas",
            elevation=2,
            md_bg_color=(0.2, 0.6, 0.9, 1),
            left_action_items=[["arrow-left", lambda x: self.switch_screen("main")]]
        )
        main_layout.add_widget(toolbar)
        
        # Formulario de hipoteca
        form_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="400dp",
            padding=20,
            elevation=5,
            radius=[16],
            spacing=15
        )
        
        form_title = MDLabel(
            text="Datos de la Hipoteca",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="30dp"
        )
        
        # Campos del formulario
        self.id_hipoteca_field = MDTextField(
            hint_text="ID de hipoteca",
            helper_text="Ejemplo: 1",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.codigo_prop_hip_field = MDTextField(
            hint_text="Código de propiedad",
            helper_text="Ejemplo: 1",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.porcentaje_field = MDTextField(
            hint_text="Porcentaje del préstamo (%)",
            helper_text="Ejemplo: 70",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.tasa_field = MDTextField(
            hint_text="Tasa de interés (%)",
            helper_text="Ejemplo: 10",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.plazo_field = MDTextField(
            hint_text="Plazo en años",
            helper_text="Ejemplo: 20",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.renta_field = MDTextField(
            hint_text="Renta mensual (COP)",
            helper_text="Ejemplo: 1500000",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.deuda_field = MDTextField(
            hint_text="Deuda final (COP)",
            helper_text="Ejemplo: 360000000",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.estado_field = MDTextField(
            hint_text="Estado",
            helper_text="Ejemplo: ACTIVA, FINALIZADA",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        # Botones de acción
        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_insertar = MDRaisedButton(
            text="Insertar",
            on_release=self.insertar_hipoteca,
            size_hint=(1, 1)
        )
        
        btn_buscar = MDRaisedButton(
            text="Buscar",
            on_release=self.buscar_hipoteca,
            size_hint=(1, 1)
        )
        
        btn_limpiar = MDFlatButton(
            text="Limpiar",
            on_release=self.limpiar_formulario_hipoteca,
            size_hint=(1, 1)
        )
        
        btn_layout.add_widget(btn_insertar)
        btn_layout.add_widget(btn_buscar)
        btn_layout.add_widget(btn_limpiar)
        
        # Agregar widgets al formulario
        form_card.add_widget(form_title)
        form_card.add_widget(self.id_hipoteca_field)
        form_card.add_widget(self.codigo_prop_hip_field)
        form_card.add_widget(self.porcentaje_field)
        form_card.add_widget(self.tasa_field)
        form_card.add_widget(self.plazo_field)
        form_card.add_widget(self.renta_field)
        form_card.add_widget(self.deuda_field)
        form_card.add_widget(self.estado_field)
        form_card.add_widget(btn_layout)
        
        main_layout.add_widget(form_card)
        
        # Área de resultados
        self.resultado_hipoteca = MDLabel(
            text="",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint=(1, None),
            height="100dp"
        )
        main_layout.add_widget(self.resultado_hipoteca)
        
        screen.add_widget(main_layout)
        return screen

    def create_herederos_screen(self):
        """Crear pantalla para gestionar herederos"""
        screen = Screen(name="herederos")
        
        # Layout principal
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
            md_bg_color=(0.93, 0.96, 1, 1)
        )
        
        # Barra superior
        toolbar = MDTopAppBar(
            title="Gestión de Herederos",
            elevation=2,
            md_bg_color=(0.2, 0.6, 0.9, 1),
            left_action_items=[["arrow-left", lambda x: self.switch_screen("main")]]
        )
        main_layout.add_widget(toolbar)
        
        # Formulario de heredero
        form_card = MDCard(
            orientation="vertical",
            size_hint=(1, None),
            height="350dp",
            padding=20,
            elevation=5,
            radius=[16],
            spacing=15
        )
        
        form_title = MDLabel(
            text="Datos del Heredero",
            halign="center",
            font_style="H5",
            size_hint=(1, None),
            height="30dp"
        )
        
        # Campos del formulario
        self.id_heredero_field = MDTextField(
            hint_text="ID del heredero",
            helper_text="Ejemplo: 1",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.cedula_cliente_her_field = MDTextField(
            hint_text="Cédula del cliente",
            helper_text="Ejemplo: 12345678",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.nombre_her_field = MDTextField(
            hint_text="Nombre del heredero",
            helper_text="Ejemplo: Pedro Pérez",
            helper_text_mode="on_focus",
            mode="rectangle",
            required=True,
            size_hint_y=None,
            height="60dp"
        )
        
        self.relacion_field = MDTextField(
            hint_text="Relación",
            helper_text="Ejemplo: Hijo, Hija, Cónyuge",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.telefono_her_field = MDTextField(
            hint_text="Teléfono",
            helper_text="Ejemplo: 3009876543",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        self.correo_her_field = MDTextField(
            hint_text="Correo electrónico",
            helper_text="Ejemplo: pedro@email.com",
            helper_text_mode="on_focus",
            mode="rectangle",
            size_hint_y=None,
            height="60dp"
        )
        
        # Botones de acción
        btn_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, None),
            height="50dp"
        )
        
        btn_insertar = MDRaisedButton(
            text="Insertar",
            on_release=self.insertar_heredero,
            size_hint=(1, 1)
        )
        
        btn_buscar = MDRaisedButton(
            text="Buscar",
            on_release=self.buscar_heredero,
            size_hint=(1, 1)
        )
        
        btn_limpiar = MDFlatButton(
            text="Limpiar",
            on_release=self.limpiar_formulario_heredero,
            size_hint=(1, 1)
        )
        
        btn_layout.add_widget(btn_insertar)
        btn_layout.add_widget(btn_buscar)
        btn_layout.add_widget(btn_limpiar)
        
        # Agregar widgets al formulario
        form_card.add_widget(form_title)
        form_card.add_widget(self.id_heredero_field)
        form_card.add_widget(self.cedula_cliente_her_field)
        form_card.add_widget(self.nombre_her_field)
        form_card.add_widget(self.relacion_field)
        form_card.add_widget(self.telefono_her_field)
        form_card.add_widget(self.correo_her_field)
        form_card.add_widget(btn_layout)
        
        main_layout.add_widget(form_card)
        
        # Área de resultados
        self.resultado_heredero = MDLabel(
            text="",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint=(1, None),
            height="100dp"
        )
        main_layout.add_widget(self.resultado_heredero)
        
        screen.add_widget(main_layout)
        return screen

    def switch_screen(self, screen_name):
        """Cambiar a una pantalla específica"""
        self.screen_manager.current = screen_name

    def mostrar_error(self, mensaje):
        """Mostrar un diálogo de error"""
        dialog = MDDialog(
            title="Error",
            text=mensaje,
            buttons=[
                MDFlatButton(
                    text="CERRAR",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    def mostrar_exito(self, mensaje):
        """Mostrar un diálogo de éxito"""
        dialog = MDDialog(
            title="Éxito",
            text=mensaje,
            buttons=[
                MDFlatButton(
                    text="CERRAR",
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

    # Métodos para clientes
    def insertar_cliente(self, instance):
        """Insertar un nuevo cliente"""
        try:
            # Validar campos requeridos
            if not self.cedula_field.text.strip():
                self.mostrar_error("La cédula es requerida")
                return
            
            if not self.nombre_field.text.strip():
                self.mostrar_error("El nombre es requerido")
                return
            
            if not self.edad_field.text.strip():
                self.mostrar_error("La edad es requerida")
                return
            
            # Validar edad
            try:
                edad = int(self.edad_field.text.strip())
                if edad < 65 or edad > 90:
                    self.mostrar_error("La edad debe estar entre 65 y 90 años")
                    return
            except ValueError:
                self.mostrar_error("La edad debe ser un número válido")
                return
            
            # Crear objeto cliente
            cliente = Clientess(
                cedula=self.cedula_field.text.strip(),
                nombre=self.nombre_field.text.strip(),
                edad=edad,
                direccion=self.direccion_field.text.strip() or None,
                telefono=self.telefono_field.text.strip() or None,
                correo=self.correo_field.text.strip() or None
            )
            
            # Insertar en base de datos
            resultado = ClientesController.insertar(cliente)
            
            if resultado:
                self.mostrar_exito("Cliente insertado exitosamente")
                self.resultado_cliente.text = f"Cliente insertado: {cliente.nombre} (Cédula: {cliente.cedula})"
            else:
                self.mostrar_error("Error al insertar el cliente")
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def buscar_cliente(self, instance):
        """Buscar un cliente por cédula"""
        try:
            if not self.cedula_field.text.strip():
                self.mostrar_error("Ingrese la cédula para buscar")
                return
            
            cliente = ClientesController.buscar(self.cedula_field.text.strip())
            
            if cliente:
                # Llenar el formulario con los datos encontrados
                self.nombre_field.text = cliente.nombre
                self.edad_field.text = str(cliente.edad)
                self.direccion_field.text = cliente.direccion or ""
                self.telefono_field.text = cliente.telefono or ""
                self.correo_field.text = cliente.correo or ""
                
                self.resultado_cliente.text = f"Cliente encontrado: {cliente.nombre}"
            else:
                self.mostrar_error("Cliente no encontrado")
                self.resultado_cliente.text = "Cliente no encontrado"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def limpiar_formulario_cliente(self, instance):
        """Limpiar el formulario de cliente"""
        self.cedula_field.text = ""
        self.nombre_field.text = ""
        self.edad_field.text = ""
        self.direccion_field.text = ""
        self.telefono_field.text = ""
        self.correo_field.text = ""
        self.resultado_cliente.text = ""

    # Métodos para propiedades
    def insertar_propiedad(self, instance):
        """Insertar una nueva propiedad"""
        try:
            # Validar campos requeridos
            if not self.codigo_prop_field.text.strip():
                self.mostrar_error("El código de propiedad es requerido")
                return
            
            if not self.cedula_cliente_prop_field.text.strip():
                self.mostrar_error("La cédula del cliente es requerida")
                return
            
            if not self.valor_prop_field.text.strip():
                self.mostrar_error("El valor de la propiedad es requerido")
                return
            
            # Validar valores numéricos
            try:
                codigo = int(self.codigo_prop_field.text.strip())
                valor = float(self.valor_prop_field.text.strip())
                area = float(self.area_prop_field.text.strip()) if self.area_prop_field.text.strip() else None
            except ValueError:
                self.mostrar_error("Los valores numéricos deben ser válidos")
                return
            
            # Crear objeto propiedad
            propiedad = Propiedad(
                codigo_propiedad=codigo,
                cedula_cliente=self.cedula_cliente_prop_field.text.strip(),
                valor_propiedad=valor,
                direccion=self.direccion_prop_field.text.strip() or None,
                area=area,
                tipo=self.tipo_prop_field.text.strip() or None
            )
            
            # Insertar en base de datos
            PropiedadesController.insertar(propiedad)
            self.mostrar_exito("Propiedad insertada exitosamente")
            self.resultado_propiedad.text = f"Propiedad insertada: Código {codigo}"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def buscar_propiedad(self, instance):
        """Buscar una propiedad por código"""
        try:
            if not self.codigo_prop_field.text.strip():
                self.mostrar_error("Ingrese el código de propiedad para buscar")
                return
            
            codigo = int(self.codigo_prop_field.text.strip())
            propiedad = PropiedadesController.buscar(codigo)
            
            if propiedad:
                # Llenar el formulario con los datos encontrados
                self.cedula_cliente_prop_field.text = propiedad[1]
                self.valor_prop_field.text = str(propiedad[2])
                self.direccion_prop_field.text = propiedad[3] or ""
                self.area_prop_field.text = str(propiedad[4]) if propiedad[4] else ""
                self.tipo_prop_field.text = propiedad[5] or ""
                
                self.resultado_propiedad.text = f"Propiedad encontrada: Código {codigo}"
            else:
                self.mostrar_error("Propiedad no encontrada")
                self.resultado_propiedad.text = "Propiedad no encontrada"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def limpiar_formulario_propiedad(self, instance):
        """Limpiar el formulario de propiedad"""
        self.codigo_prop_field.text = ""
        self.cedula_cliente_prop_field.text = ""
        self.valor_prop_field.text = ""
        self.direccion_prop_field.text = ""
        self.area_prop_field.text = ""
        self.tipo_prop_field.text = ""
        self.resultado_propiedad.text = ""

    # Métodos para hipotecas
    def insertar_hipoteca(self, instance):
        """Insertar una nueva hipoteca"""
        try:
            # Validar campos requeridos
            campos_requeridos = [
                (self.id_hipoteca_field, "ID de hipoteca"),
                (self.codigo_prop_hip_field, "Código de propiedad"),
                (self.porcentaje_field, "Porcentaje del préstamo"),
                (self.tasa_field, "Tasa de interés"),
                (self.plazo_field, "Plazo en años"),
                (self.renta_field, "Renta mensual"),
                (self.deuda_field, "Deuda final"),
                (self.estado_field, "Estado")
            ]
            
            for campo, nombre in campos_requeridos:
                if not campo.text.strip():
                    self.mostrar_error(f"{nombre} es requerido")
                    return
            
            # Validar valores numéricos
            try:
                id_hipoteca = int(self.id_hipoteca_field.text.strip())
                porcentaje = float(self.porcentaje_field.text.strip())
                tasa = float(self.tasa_field.text.strip())
                plazo = int(self.plazo_field.text.strip())
                renta = float(self.renta_field.text.strip())
                deuda = float(self.deuda_field.text.strip())
            except ValueError:
                self.mostrar_error("Los valores numéricos deben ser válidos")
                return
            
            # Crear objeto hipoteca
            hipoteca = Hipoteca(
                id_hipoteca=id_hipoteca,
                codigo_propiedad=self.codigo_prop_hip_field.text.strip(),
                porcentaje_prestamo=porcentaje,
                tasa_interes=tasa,
                plazo_anios=plazo,
                renta_mensual=renta,
                deuda_final=deuda,
                fecha_inicio=date.today(),
                fecha_fin=None,
                estado=self.estado_field.text.strip()
            )
            
            # Insertar en base de datos
            resultado = HipotecasController.insertar(hipoteca)
            
            if resultado:
                self.mostrar_exito("Hipoteca insertada exitosamente")
                self.resultado_hipoteca.text = f"Hipoteca insertada: ID {id_hipoteca}"
            else:
                self.mostrar_error("Error al insertar la hipoteca")
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def buscar_hipoteca(self, instance):
        """Buscar una hipoteca por ID"""
        try:
            if not self.id_hipoteca_field.text.strip():
                self.mostrar_error("Ingrese el ID de hipoteca para buscar")
                return
            
            id_hipoteca = int(self.id_hipoteca_field.text.strip())
            hipoteca = HipotecasController.buscar(id_hipoteca)
            
            if hipoteca:
                # Llenar el formulario con los datos encontrados
                self.codigo_prop_hip_field.text = hipoteca.codigo_propiedad
                self.porcentaje_field.text = str(hipoteca.porcentaje_prestamo)
                self.tasa_field.text = str(hipoteca.tasa_interes)
                self.plazo_field.text = str(hipoteca.plazo_anios)
                self.renta_field.text = str(hipoteca.renta_mensual)
                self.deuda_field.text = str(hipoteca.deuda_final)
                self.estado_field.text = hipoteca.estado
                
                self.resultado_hipoteca.text = f"Hipoteca encontrada: ID {id_hipoteca}"
            else:
                self.mostrar_error("Hipoteca no encontrada")
                self.resultado_hipoteca.text = "Hipoteca no encontrada"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def limpiar_formulario_hipoteca(self, instance):
        """Limpiar el formulario de hipoteca"""
        self.id_hipoteca_field.text = ""
        self.codigo_prop_hip_field.text = ""
        self.porcentaje_field.text = ""
        self.tasa_field.text = ""
        self.plazo_field.text = ""
        self.renta_field.text = ""
        self.deuda_field.text = ""
        self.estado_field.text = ""
        self.resultado_hipoteca.text = ""

    # Métodos para herederos
    def insertar_heredero(self, instance):
        """Insertar un nuevo heredero"""
        try:
            # Validar campos requeridos
            if not self.id_heredero_field.text.strip():
                self.mostrar_error("El ID del heredero es requerido")
                return
            
            if not self.cedula_cliente_her_field.text.strip():
                self.mostrar_error("La cédula del cliente es requerida")
                return
            
            if not self.nombre_her_field.text.strip():
                self.mostrar_error("El nombre del heredero es requerido")
                return
            
            # Validar ID
            try:
                id_heredero = int(self.id_heredero_field.text.strip())
            except ValueError:
                self.mostrar_error("El ID del heredero debe ser un número válido")
                return
            
            # Crear objeto heredero
            heredero = Heredero(
                id_heredero=id_heredero,
                cedula_cliente=self.cedula_cliente_her_field.text.strip(),
                nombre=self.nombre_her_field.text.strip(),
                relacion=self.relacion_field.text.strip() or None,
                telefono=self.telefono_her_field.text.strip() or None,
                correo=self.correo_her_field.text.strip() or None
            )
            
            # Insertar en base de datos
            HerederosController.insertar(heredero)
            self.mostrar_exito("Heredero insertado exitosamente")
            self.resultado_heredero.text = f"Heredero insertado: {heredero.nombre}"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def buscar_heredero(self, instance):
        """Buscar un heredero por ID"""
        try:
            if not self.id_heredero_field.text.strip():
                self.mostrar_error("Ingrese el ID del heredero para buscar")
                return
            
            id_heredero = int(self.id_heredero_field.text.strip())
            heredero = HerederosController.buscar(id_heredero)
            
            if heredero:
                # Llenar el formulario con los datos encontrados
                self.cedula_cliente_her_field.text = heredero[1]
                self.nombre_her_field.text = heredero[2]
                self.relacion_field.text = heredero[3] or ""
                self.telefono_her_field.text = heredero[4] or ""
                self.correo_her_field.text = heredero[5] or ""
                
                self.resultado_heredero.text = f"Heredero encontrado: {heredero[2]}"
            else:
                self.mostrar_error("Heredero no encontrado")
                self.resultado_heredero.text = "Heredero no encontrado"
                
        except Exception as e:
            self.mostrar_error(f"Error: {str(e)}")

    def limpiar_formulario_heredero(self, instance):
        """Limpiar el formulario de heredero"""
        self.id_heredero_field.text = ""
        self.cedula_cliente_her_field.text = ""
        self.nombre_her_field.text = ""
        self.relacion_field.text = ""
        self.telefono_her_field.text = ""
        self.correo_her_field.text = ""
        self.resultado_heredero.text = ""

if __name__ == "__main__":
    DatabaseInterfaceApp().run()
