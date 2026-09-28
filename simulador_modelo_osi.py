import tkinter as tk
from tkinter import ttk, messagebox
import base64


class SimuladorOSI:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador Interactivo del Modelo OSI")
        self.ventana.geometry("1200x700")
        self.ventana.resizable(True, True)

        self.mensaje = ""
        self.mensaje_codificado = ""
        self.procesando = False
        self.capa_actual = 0

        self.capas = [
            (7, "Aplicación"),
            (6, "Presentación"),
            (5, "Sesión"),
            (4, "Transporte"),
            (3, "Red"),
            (2, "Enlace de Datos"),
            (1, "Física")
        ]

        self.informacion_capas = {
            7: "Proporciona servicios de red a las aplicaciones.\nEjemplos: HTTP, FTP, DNS.",
            6: "Transforma, codifica, cifra o comprime los datos.\nEjemplos: UTF-8, TLS y Base64.",
            5: "Establece y administra sesiones de comunicación.",
            4: "Permite la comunicación extremo a extremo.\nEjemplos: TCP y UDP.",
            3: "Gestiona el direccionamiento lógico mediante IP.",
            2: "Utiliza tramas y direcciones MAC.\nEjemplo: Ethernet.",
            1: "Representa los bits mediante un medio físico."
        }

        self.crear_interfaz()

    # =========================================================
    # CREACIÓN DE LA INTERFAZ
    # =========================================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="SIMULADOR INTERACTIVO DEL MODELO OSI",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)

        marco_entrada = tk.Frame(self.ventana)
        marco_entrada.pack(pady=5)

        tk.Label(
            marco_entrada,
            text="Mensaje:",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=5)

        self.entrada = tk.Entry(
            marco_entrada,
            width=40,
            font=("Arial", 12)
        )
        self.entrada.insert(0, "Hola Red OSI")
        self.entrada.pack(side=tk.LEFT, padx=5)

        self.boton_encapsular = tk.Button(
            marco_entrada,
            text="📤 Encapsular",
            command=self.encapsular,
            width=15
        )
        self.boton_encapsular.pack(side=tk.LEFT, padx=5)

        self.boton_transmitir = tk.Button(
            marco_entrada,
            text="📡 Transmitir",
            command=self.transmitir,
            width=15,
            state=tk.DISABLED
        )
        self.boton_transmitir.pack(side=tk.LEFT, padx=5)

        self.boton_desencapsular = tk.Button(
            marco_entrada,
            text="📥 Desencapsular",
            command=self.desencapsular,
            width=15,
            state=tk.DISABLED
        )
        self.boton_desencapsular.pack(side=tk.LEFT, padx=5)

        self.boton_reiniciar = tk.Button(
            marco_entrada,
            text="🔄 Reiniciar",
            command=self.reiniciar,
            width=15
        )
        self.boton_reiniciar.pack(side=tk.LEFT, padx=5)

        self.estado = tk.Label(
            self.ventana,
            text="Estado: listo para comenzar",
            font=("Arial", 11, "bold")
        )
        self.estado.pack(pady=5)

        self.progreso = ttk.Progressbar(
            self.ventana,
            orient="horizontal",
            length=800,
            mode="determinate",
            maximum=7
        )
        self.progreso.pack(pady=5)

        marco_principal = tk.Frame(self.ventana)
        marco_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------------------------------------------------
        # PANEL DE CAPAS
        # ---------------------------------------------------------

        marco_capas = tk.LabelFrame(
            marco_principal,
            text="MODELO OSI",
            font=("Arial", 11, "bold")
        )
        marco_capas.pack(
            side=tk.LEFT,
            fill="y",
            padx=5
        )

        for numero, nombre in self.capas:
            boton = tk.Button(
                marco_capas,
                text=f"{numero}. {nombre}",
                width=20,
                command=lambda n=numero: self.mostrar_capa(n)
            )
            boton.pack(pady=5, padx=5)

        # ---------------------------------------------------------
        # PANEL EMISOR
        # ---------------------------------------------------------

        marco_emisor = tk.LabelFrame(
            marco_principal,
            text="📤 PC-A - ENCAPSULAMIENTO",
            font=("Arial", 11, "bold")
        )
        marco_emisor.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=5
        )

        self.texto_emisor = tk.Text(
            marco_emisor,
            width=40,
            height=25,
            font=("Consolas", 10)
        )
        self.texto_emisor.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # ---------------------------------------------------------
        # PANEL RECEPTOR
        # ---------------------------------------------------------

        marco_receptor = tk.LabelFrame(
            marco_principal,
            text="📥 PC-B - DESENCAPSULAMIENTO",
            font=("Arial", 11, "bold")
        )
        marco_receptor.pack(
            side=tk.LEFT,
            fill="both",
            expand=True,
            padx=5
        )

        self.texto_receptor = tk.Text(
            marco_receptor,
            width=40,
            height=25,
            font=("Consolas", 10)
        )
        self.texto_receptor.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    # =========================================================
    # MOSTRAR INFORMACIÓN DE LAS CAPAS
    # =========================================================

    def mostrar_capa(self, numero):
        informacion = self.informacion_capas[numero]

        ventana_info = tk.Toplevel(self.ventana)
        ventana_info.title(f"Capa {numero}")
        ventana_info.geometry("500x250")

        tk.Label(
            ventana_info,
            text=f"Capa {numero}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        tk.Label(
            ventana_info,
            text=informacion,
            font=("Arial", 12),
            justify="left"
        ).pack(padx=20, pady=10)

    # =========================================================
    # ESCRIBIR INFORMACIÓN
    # =========================================================

    def escribir(self, widget, texto):
        widget.insert(tk.END, texto + "\n")
        widget.see(tk.END)

    # =========================================================
    # ENCAPSULAMIENTO
    # =========================================================

    def encapsular(self):

        if self.procesando:
            return

        self.mensaje = self.entrada.get().strip()

        if not self.mensaje:
            messagebox.showwarning(
                "Advertencia",
                "Ingrese un mensaje antes de comenzar."
            )
            return

        self.procesando = True
        self.capa_actual = 0

        self.texto_emisor.delete("1.0", tk.END)
        self.texto_receptor.delete("1.0", tk.END)

        self.progreso["value"] = 0

        self.boton_encapsular.config(state=tk.DISABLED)
        self.boton_transmitir.config(state=tk.DISABLED)
        self.boton_desencapsular.config(state=tk.DISABLED)

        self.estado.config(
            text="Estado: realizando encapsulamiento..."
        )

        self.escribir(
            self.texto_emisor,
            "===== INICIO DEL ENCAPSULAMIENTO ====="
        )

        self.procesar_siguiente_capa()

    def procesar_siguiente_capa(self):

        if self.capa_actual >= len(self.capas):

            self.escribir(
                self.texto_emisor,
                ""
            )

            self.escribir(
                self.texto_emisor,
                "✔ ENCAPSULAMIENTO COMPLETADO"
            )

            self.escribir(
                self.texto_emisor,
                "El mensaje está listo para ser transmitido."
            )

            self.estado.config(
                text="Estado: encapsulamiento completado"
            )

            self.procesando = False

            self.boton_transmitir.config(
                state=tk.NORMAL
            )

            self.boton_reiniciar.config(
                state=tk.NORMAL
            )

            return

        numero, nombre = self.capas[self.capa_actual]

        self.progreso["value"] = self.capa_actual + 1

        self.escribir(
            self.texto_emisor,
            f"\n--- CAPA {numero}: {nombre.upper()} ---"
        )

        if numero == 7:

            self.escribir(
                self.texto_emisor,
                f"Mensaje original: {self.mensaje}"
            )

        elif numero == 6:

            self.mensaje_codificado = base64.b64encode(
                self.mensaje.encode("utf-8")
            ).decode("utf-8")

            self.escribir(
                self.texto_emisor,
                "Formato original: UTF-8"
            )

            self.escribir(
                self.texto_emisor,
                "Codificación Base64:"
            )

            self.escribir(
                self.texto_emisor,
                self.mensaje_codificado
            )

            self.escribir(
                self.texto_emisor,
                "Seguridad representada: TLS"
            )

        elif numero == 5:

            self.escribir(
                self.texto_emisor,
                "ID de sesión: #88392"
            )

            self.escribir(
                self.texto_emisor,
                "Se establece una sesión de comunicación."
            )

        elif numero == 4:

            self.escribir(
                self.texto_emisor,
                "Protocolo: TCP"
            )

            self.escribir(
                self.texto_emisor,
                "Puerto origen: 8080"
            )

            self.escribir(
                self.texto_emisor,
                "Puerto destino: 443"
            )

            self.escribir(
                self.texto_emisor,
                "Se crea el segmento."
            )

        elif numero == 3:

            self.escribir(
                self.texto_emisor,
                "Protocolo: IPv4"
            )

            self.escribir(
                self.texto_emisor,
                "IP origen: 192.168.1.15"
            )

            self.escribir(
                self.texto_emisor,
                "IP destino: 142.250.190.46"
            )

            self.escribir(
                self.texto_emisor,
                "Se crea el paquete."
            )

        elif numero == 2:

            self.escribir(
                self.texto_emisor,
                "Tecnología: Ethernet"
            )

            self.escribir(
                self.texto_emisor,
                "MAC origen: AA:11:BB:22:CC:33"
            )

            self.escribir(
                self.texto_emisor,
                "MAC destino: DD:44:EE:55:FF:66"
            )

            self.escribir(
                self.texto_emisor,
                "Se crea la trama."
            )

        elif numero == 1:

            datos = self.mensaje.encode("utf-8")

            bits = " ".join(
                format(byte, "08b")
                for byte in datos
            )

            self.escribir(
                self.texto_emisor,
                "Representación binaria:"
            )

            self.escribir(
                self.texto_emisor,
                bits
            )

            self.escribir(
                self.texto_emisor,
                "Medio físico: cable / Wi-Fi"
            )

        self.capa_actual += 1

        self.ventana.after(
            1000,
            self.procesar_siguiente_capa
        )

    # =========================================================
    # TRANSMISIÓN
    # =========================================================

    def transmitir(self):

        if self.procesando:
            return

        if not self.mensaje:
            messagebox.showwarning(
                "Advertencia",
                "Primero debe encapsular un mensaje."
            )
            return

        self.procesando = True

        self.estado.config(
            text="Estado: transmitiendo de PC-A a PC-B..."
        )

        self.escribir(
            self.texto_emisor,
            "\n===== TRANSMISIÓN PC-A → PC-B ====="
        )

        self.escribir(
            self.texto_emisor,
            "El mensaje encapsulado está siendo representado"
        )

        self.escribir(
            self.texto_emisor,
            "como enviado desde PC-A hacia PC-B."
        )

        self.ventana.after(
            1500,
            self.finalizar_transmision
        )

    def finalizar_transmision(self):

        self.escribir(
            self.texto_receptor,
            "===== MENSAJE RECIBIDO EN PC-B ====="
        )

        self.escribir(
            self.texto_receptor,
            "Los datos encapsulados fueron recibidos."
        )

        self.escribir(
            self.texto_receptor,
            "Listo para iniciar el desencapsulamiento."
        )

        self.estado.config(
            text="Estado: transmisión completada"
        )

        self.procesando = False

        self.boton_transmitir.config(
            state=tk.DISABLED
        )

        self.boton_desencapsular.config(
            state=tk.NORMAL
        )

    # =========================================================
    # DESENCAPSULAMIENTO
    # =========================================================

    def desencapsular(self):

        if self.procesando:
            return

        self.procesando = True

        self.capa_actual = len(self.capas) - 1

        self.boton_desencapsular.config(
            state=tk.DISABLED
        )

        self.estado.config(
            text="Estado: realizando desencapsulamiento..."
        )

        self.escribir(
            self.texto_receptor,
            "\n===== INICIO DEL DESENCAPSULAMIENTO ====="
        )

        self.procesar_desencapsulamiento()

    def procesar_desencapsulamiento(self):

        if self.capa_actual < 0:

            self.escribir(
                self.texto_receptor,
                ""
            )

            self.escribir(
                self.texto_receptor,
                "✔ DESENCAPSULAMIENTO COMPLETADO"
            )

            self.escribir(
                self.texto_receptor,
                f"Mensaje recibido: '{self.mensaje}'"
            )

            self.estado.config(
                text="Estado: mensaje recuperado correctamente en PC-B"
            )

            self.procesando = False

            self.boton_encapsular.config(
                state=tk.NORMAL
            )

            self.boton_reiniciar.config(
                state=tk.NORMAL
            )

            return

        numero, nombre = self.capas[self.capa_actual]

        self.escribir(
            self.texto_receptor,
            f"\n--- CAPA {numero}: {nombre.upper()} ---"
        )

        if numero == 1:

            self.escribir(
                self.texto_receptor,
                "Recibiendo bits mediante el medio físico."
            )

        elif numero == 2:

            self.escribir(
                self.texto_receptor,
                "Eliminando información de la trama Ethernet."
            )

        elif numero == 3:

            self.escribir(
                self.texto_receptor,
                "Eliminando información de direccionamiento IP."
            )

        elif numero == 4:

            self.escribir(
                self.texto_receptor,
                "Eliminando información de transporte TCP."
            )

        elif numero == 5:

            self.escribir(
                self.texto_receptor,
                "Finalizando la sesión de comunicación."
            )

        elif numero == 6:

            try:
                mensaje_decodificado = base64.b64decode(
                    self.mensaje_codificado
                ).decode("utf-8")

                self.escribir(
                    self.texto_receptor,
                    "Decodificando información Base64."
                )

                self.escribir(
                    self.texto_receptor,
                    f"Datos recuperados: {mensaje_decodificado}"
                )

            except Exception:
                self.escribir(
                    self.texto_receptor,
                    "Interpretando los datos en formato UTF-8."
                )

        elif numero == 7:

            self.escribir(
                self.texto_receptor,
                "Entregando los datos a la aplicación."
            )

        self.escribir(
            self.texto_receptor,
            "✔ Capa procesada correctamente."
        )

        self.capa_actual -= 1

        self.ventana.after(
            1000,
            self.procesar_desencapsulamiento
        )

    # =========================================================
    # REINICIAR
    # =========================================================

    def reiniciar(self):

        self.mensaje = ""
        self.mensaje_codificado = ""
        self.procesando = False
        self.capa_actual = 0

        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "Hola Red OSI")

        self.texto_emisor.delete(
            "1.0",
            tk.END
        )

        self.texto_receptor.delete(
            "1.0",
            tk.END
        )

        self.progreso["value"] = 0

        self.estado.config(
            text="Estado: listo para comenzar"
        )

        self.boton_encapsular.config(
            state=tk.NORMAL
        )

        self.boton_transmitir.config(
            state=tk.DISABLED
        )

        self.boton_desencapsular.config(
            state=tk.DISABLED
        )


# =============================================================
# EJECUCIÓN DEL PROGRAMA
# =============================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = SimuladorOSI(ventana)

    ventana.mainloop()