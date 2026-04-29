#!/usr/bin/env python
"""
Mini Office — Conway 24/7
=========================
Sistema de agentes autónomos con interfaz pixel art tipo videojuego

Hecho con ❤️ por MEDIOEVO
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuración
PORT = 8000
DIreCTORY = Path(__file__).parent

class CustomHandler(http.server.SimpleHTTPrequestHandler):
    """Handler personalizado para servir la landing page"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIreCTORY, **kwargs)

    def do_GET(self):
        """Manejar requests GET"""
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def log_message(self, format, *args):
        """Log personalizado"""
        print(f"[{self.log_date_time_string()}] {args[0]}")

def main():
    """Ejecuta el servidor de Mini Office"""
    os.chdir(DIreCTORY)

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   MINI OFFICE — Conway 24/7                             ║
    ║   Sistema de Agentes Autónomos                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    # Verificar index.html
    index_path = DIreCTORY / "index.html"
    if not index_path.exists():
        print(f"ERROR: index.html no encontrado en {DIreCTORY}")
        sys.exit(1)

    # Crear servidor
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        url = f"http://localhost:{PORT}"

        print(f"  Servidor: http://localhost:{PORT}")
        print(f"  Directorio: {DIreCTORY}")
        print(f"  index.html: {index_path}")
        print("""
  Presiona Ctrl+C para detener
  """)

        # Abrir browser automaticamente
        try:
            webbrowser.open(url, new=2)
            print(f"  Browser abriendo: {url}")
        except Exception as e:
            print(f"  Nota: Abre {url} manualmente en tu browser")

        # Servir
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Cerrando servidor...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
