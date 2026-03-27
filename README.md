# Dashboard de Microservicios - Arquitectura UCB 🚀

Un moderno panel de control de monitoreo de microservicios desarrollado en **Python (Flask)**. Este sistema permite verificar en tiempo real el estado, disponibilidad (2.0s de timeout) y la respuesta/payload de una variedad de APIs implementadas en la arquitectura de red local (UCB).

![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black)

---

## ✨ Características

- **Interfaz Moderna Tabular:** Construida con `Tailwind CSS`, presenta los servicios igual que una aplicación de escritorio nativa orientada a datos.
- **Gráficos en Tiempo Real:** Integración con `Chart.js` para un gráfico de anillo (Doughnut) de disponibilidad de red (Activos vs Caídos).
- **Múltiples Métodos HTTP:** Soporta solicitudes `GET` y `POST`.
- **Inyección de Parámetros:** Capacidad de enviar `Query Params` (?a=10&b=5), cabeceras HTTP (`Headers` como los de *Authorization*) y `JSON Payloads` (útil para autenticación).
- **Parseo de Payload:** Desempaquetado dinámico de respuestas JSON (verde si es un 200 OK, rojo si es un timeout/error HTTP).

---

## 🛠️ Instalación y Uso

### 1. Requisitos
Asegúrate de tener instalado Python 3.9 o superior.

### 2. Instalar dependencias
Abre tu terminal (PowerShell o CMD) y ejecuta:
```bash
pip install flask requests
```

### 3. Ejecutar el Servidor
Inicia la herramienta de monitoreo:
```bash
python dashboard.py
```

### 4. Abrir en el navegador
Visita el enlace local que arroja la terminal:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## ⚠️ Solución de Problemas Frecuentes (Troubleshooting)

### Error: `ERROR: Socket Blocked (Network Boost / Firewall)` / `WinError 10013`
Este es un error común ocasionado cuando un software de red interno prohíbe a Python comunicarse con las IPs locales del segmento (`10.80.x.x` o `10.10.x.x`). 

**Solución si tienes Lenovo Vantage:**
1. Abre **Lenovo Vantage** en tu computadora.
2. Ve a la sección **Red** (Network) o configuración de Juegos.
3. Desactiva la función de **Celeridad de Red / Network Boost**.

**Solución si es el Firewall de Windows:**
1. Escribe en inicio `Permitir una aplicación a través de Firewall de Windows`.
2. Busca `python.exe`.
3. Activa las casillas tanto de redes **Privadas** como **Públicas**.
4. Haz clic en Aceptar.

---

## 🔗 Microservicios Monitoreados

Actualmente, el dashboard testea las siguientes categorías orientadas a micro-frontends y backends:

- **Estructuras de Datos:** Árboles Binarios, Colas, Listas enlazadas, Matrices.
- **Operaciones Matemáticas:** Suma, Resta, Multiplicación, División, Potencia.
- **Seguridad (Auth):** Registro, Login, Verificación de sesión de usuario y Refresco de Tokens Temporales.
- **Minijuegos:** Ahorcado, Buscaminas, Tres en Raya.