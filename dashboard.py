from flask import Flask, render_template_string, request, jsonify
import requests
import json
import threading
from datetime import datetime

app = Flask(__name__)

# Configuracion de Firebase (Extraida de tu proyecto)
FIREBASE_URL = "https://arqu-8f89c-default-rtdb.firebaseio.com"
FIREBASE_SECRET = "jSQbMFQ6Cvex22J6xlJhCg7iJ1sO4oWRVHOhQnaE"

def guardar_en_firebase(snapshot_data):
    """Sube un log de la métrica a Firebase en segundo plano para no demorar la web."""
    try:
        url = f"{FIREBASE_URL}/monitoreo/historial.json?auth={FIREBASE_SECRET}"
        requests.post(url, json=snapshot_data, timeout=3.0)
        
        # También actualizamos un nodo "estado_actual" 
        url_actual = f"{FIREBASE_URL}/monitoreo/estado_actual.json?auth={FIREBASE_SECRET}"
        requests.put(url_actual, json=snapshot_data, timeout=3.0)
    except Exception as e:
        print(f"Error al subir a Firebase: {e}")

# 1. Lista exhaustiva basada en la nueva lista del chat
SERVICIOS = [
    {"nombre": "Docs / Lista Enlazada", "url": "http://10.80.114.103:8000/docs", "params": ""},
    {"nombre": "Arbol Binario", "url": "http://10.80.114.115:5000/arbolbinario", "params": "count=99"},
    {"nombre": "Sumar", "url": "http://10.80.114.112:5001/sumar", "params": "a=75&b=25"},
    {"nombre": "Historial Suma", "url": "http://10.80.114.112:5001/historial", "params": ""},
    {"nombre": "Multiplicar", "url": "http://10.80.114.123:5001/multiplicar", "params": "a=2&b=3"},
    {"nombre": "Division", "url": "http://10.80.114.121:8080/division", "params": "a=10&b=2"},
    {"nombre": "Potencia", "url": "http://10.80.114.128:8080/potencia", "params": "base=2&exp=3"},
    {"nombre": "Restar", "url": "http://10.80.114.126:5001/restar", "params": "a=10&b=5"},
    {"nombre": "Ahorcado", "url": "http://10.80.114.114:5240/swagger", "params": ""},
    {"nombre": "Buscamina", "url": "http://10.80.114.122:5144/swagger", "params": ""},
    {"nombre": "Tres en Raya", "url": "http://10.80.114.101:62679/index.html", "params": ""},
    {"nombre": "Cola / Docs", "url": "http://10.80.114.113:8000/docs", "params": ""},
    {"nombre": "Creador de Matrices", "url": "http://10.80.114.130:8000", "params": ""},
    
    # Endpoints de Autenticación
    {"nombre": "Auth - Registro", "url": "http://10.10.22.84:7776/register", "params": "", "method": "POST", "json": {"email":"test@test.com","password":"mipass123"}},
    {"nombre": "Auth - Login", "url": "http://10.10.22.84:7776/login", "params": "", "method": "POST", "json": {"email":"test@test.com","password":"mipass123"}},
    {"nombre": "Auth - Me", "url": "http://10.10.22.84:7776/me", "params": "", "method": "GET", "headers": {"Authorization": "Bearer TOKEN_AQUI"}},
    {"nombre": "Auth - Refresh", "url": "http://10.10.22.84:7776/refresh", "params": "", "method": "POST", "json": {"refreshToken": "REFRESH_TOKEN_AQUI"}},
    {"nombre": "Auth - Logout", "url": "http://10.10.22.84:7776/logout", "params": "", "method": "POST", "headers": {"Authorization": "Bearer TOKEN_AQUI"}}
]

# 2. Plantilla UI Moderna (Estilo Dashboard Proyectado pero estético)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard de Microservicios</title>
    <!-- Tailwind CSS para diseño moderno rápido -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <style>
        body { background-color: #f3f4f6; }
        .glass-panel { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        .table-row-hover:hover { background-color: #f8fafc; }
        .success-bg { background-color: #d1fae5; color: #065f46; }
        .error-bg { background-color: #fee2e2; color: #991b1b; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    </style>
</head>
<body class="text-gray-800 font-sans h-screen flex flex-col p-6">

    <!-- Encabezado -->
    <header class="flex justify-between items-center mb-6 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div class="flex items-center gap-3">
            <div class="p-3 bg-blue-600 rounded-lg text-white">
                <i class="fas fa-network-wired text-xl"></i>
            </div>
            <div>
                <h1 class="text-2xl font-bold text-gray-800">System Dashboard</h1>
                <p class="text-sm text-gray-500">Monitor de estado en tiempo real (Arquitectura UCB)</p>
            </div>
        </div>
        <div class="text-right">
            <p class="text-sm text-gray-500">Última actualización</p>
            <p class="font-mono font-bold">{{ timestamp }}</p>
            <button onclick="window.location.reload()" class="mt-2 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-1 rounded shadow-sm text-sm transition-colors">
                <i class="fas fa-sync-alt mr-1"></i> Actualizar
            </button>
        </div>
    </header>

    <div class="flex gap-6 h-full min-h-0">
        
        <!-- Sidebar: Gráficos y Resumen -->
        <div class="w-1/3 flex flex-col gap-6">
            <!-- KPIs Generales -->
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Servicios Activos</p>
                    <p class="text-4xl font-black text-green-500 mt-2">{{ total_activos }}</p>
                </div>
                <div class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
                    <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Caídos / Timeout</p>
                    <p class="text-4xl font-black text-red-500 mt-2">{{ total_caidos }}</p>
                </div>
            </div>

            <!-- Gráfico Donut de Disponibilidad -->
            <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex-1">
                <h2 class="text-lg font-semibold border-b pb-2 mb-4"><i class="fas fa-chart-pie mr-2 text-indigo-500"></i>Disponibilidad de Red</h2>
                <div class="h-64 relative flex justify-center">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Main Content: La Tabla (Como en el proyector pero moderna) -->
        <div class="w-2/3 max-h-full bg-white rounded-xl shadow-sm border border-gray-100 flex flex-col overflow-hidden">
            <div class="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center z-10">
                <h2 class="text-lg font-semibold"><i class="fas fa-list-ul mr-2 text-indigo-500"></i>Registro de Peticiones (Requests)</h2>
                <span class="text-xs font-bold px-2 py-1 rounded bg-indigo-100 text-indigo-800">{{ resultados|length }} endpoints</span>
            </div>
            
            <div class="overflow-auto flex-1 p-0">
                <table class="w-full text-left border-collapse font-mono text-sm whitespace-nowrap">
                    <thead class="bg-gray-100 sticky top-0 shadow-sm z-10">
                        <tr>
                            <th class="p-3 border-b font-semibold text-gray-600">Servicio</th>
                            <th class="p-3 border-b font-semibold text-gray-600">Método / URL Destino</th>
                            <th class="p-3 border-b font-semibold text-gray-600">Params / Payload</th>
                            <th class="p-3 border-b font-semibold text-gray-600">Estado Network</th>
                            <th class="p-3 border-b font-semibold text-gray-600">Respuesta (Payload)</th>
                            <th class="p-3 border-b font-semibold text-gray-600">Probar</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in resultados %}
                        <tr class="table-row-hover border-b border-gray-50 {{ 'border-l-4 border-l-green-500' if row.estado == 'ACTIVO' else 'border-l-4 border-l-red-500' }}">
                            <td class="p-3 font-semibold font-sans">{{ row.nombre }}</td>
                            <td class="p-3 text-blue-600 truncate max-w-[200px]" title="{{ row.url }}">
                                <span class="bg-gray-200 text-gray-700 px-1 py-0.5 rounded text-xs font-bold mr-1">{{ row.method }}</span>
                                <a href="{{ row.url }}{% if row.params %}?{{ row.params }}{% endif %}" target="_blank" class="hover:underline">{{ row.url }}</a>
                            </td>
                            <td class="p-3 text-gray-500 text-xs">
                                {% if row.params is not none %}
                                    <div class="flex items-center gap-2 mb-1">
                                        <span class="text-blue-500 font-bold min-w-[20px]">Q:</span> 
                                        <input type="text" id="params_{{ loop.index }}" value="{{ row.params }}" class="border rounded px-2 py-1 w-full bg-white text-gray-700" placeholder="Ej: a=10&b=2">
                                    </div>
                                {% endif %}
                                {% if row.json is not none %}
                                    <div class="flex items-center gap-2">
                                        <span class="text-purple-500 font-bold min-w-[20px]">B:</span> 
                                        <input type="text" id="body_{{ loop.index }}" value="{{ row.json | tojson }}" class="border rounded px-2 py-1 w-full bg-white text-gray-700 font-mono text-[10px]" placeholder='Ej: {"a":1}'>
                                    </div>
                                {% endif %}
                            </td>
                            <td class="p-3">
                                {% if row.estado == 'ACTIVO' %}
                                    <span class="px-2 py-1 bg-green-100 text-green-700 rounded-md font-bold text-xs"><i class="fas fa-check-circle mr-1"></i> ACTIVO</span>
                                {% else %}
                                    <span class="px-2 py-1 bg-red-100 text-red-700 rounded-md font-bold text-xs"><i class="fas fa-times-circle mr-1"></i> ERROR</span>
                                {% endif %}
                            </td>
                            <td class="p-3 max-w-[300px]">
                                <div class="truncate {{ 'text-green-800' if row.estado == 'ACTIVO' else 'text-red-600' }}" title="{{ row.respuesta }}">
                                    {{ row.respuesta }}
                                </div>
                            </td>
                            <td class="p-3">
                                <button onclick='ejecutarFila("{{ row.url }}", "{{ row.method }}", {{ loop.index }})' class="bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-1 rounded text-xs shadow transition">
                                    <i class="fas fa-play"></i> Run
                                </button>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            <div class="p-3 bg-gray-50 border-t border-gray-100 text-center">
                <p class="text-xs text-gray-400">Desarrollado para validación de ecosistema. Latencia de prueba: 2.0s máx.</p>
            </div>
        </div>

    </div>

    <!-- Inicializar Chart.js -->
    <script>
        const ctx = document.getElementById('statusChart').getContext('2d');
        const statusChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Activos', 'Con Error / Time out'],
                datasets: [{
                    data: [{{ total_activos }}, {{ total_caidos }}],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#ffffff',
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        async function ejecutarFila(url, method, index) {
            // Obtener valores actuales de los inputs
            const paramsInput = document.getElementById(`params_${index}`);
            const bodyInput = document.getElementById(`body_${index}`);
            
            const currentParams = paramsInput ? paramsInput.value : "";
            let currentBodyStr = bodyInput ? bodyInput.value : "";
            
            let payload = null;
            if (currentBodyStr) {
                try { 
                    payload = JSON.parse(currentBodyStr); 
                } catch (e) {
                    Swal.fire({
                        icon: 'warning',
                        title: 'JSON Inválido',
                        text: 'El JSON del Body no es válido. Asegúrate de usar comillas dobles {"clave":"valor"}.'
                    });
                    return;
                }
            }
            
            let urlCompleta = url;
            if (currentParams) urlCompleta += "?" + currentParams;
            
            // 🤖 Pop-up visual animado de carga (Cargando peticion...)
            Swal.fire({
                title: 'Llamando al microservicio...',
                html: `Método: <b>${method}</b><br><span class="text-sm text-blue-500 font-mono">${urlCompleta}</span>`,
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });
            
            try {
                const response = await fetch('/test_api', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        url: url,
                        method: method,
                        params: currentParams,
                        json: payload
                    })
                });
                
                const data = await response.json();
                
                // Cerrar el popup de carga y mostrar el resultado real:
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: `¡Conectado! (HTTP ${data.status_code})`,
                        html: `El microservicio respondió:<br>
                               <pre class="bg-gray-100 p-3 rounded mt-3 text-left text-xs max-h-48 overflow-auto">${JSON.stringify(data.data, null, 2)}</pre>`
                    });
                } else {
                    let errorMessage = "El servidor respondió con error o no es alcanzable.";
                    
                    // Si el error de Python dice que hay TimeOut o WinError, deducimos que está apagado:
                    if(typeof data.data === 'string' && (data.data.includes("WinError 10013") || data.data.includes("timeout") || data.data.includes("ConnectTimeout"))) {
                        errorMessage = "<b>No está conectado</b><br>El microservicio está apagado, su computadora está sin internet, o el Firewall de él/ella lo bloqueó.";
                    } else {
                        errorMessage = `Mensaje: <br><span class="text-red-500 text-sm font-mono">${typeof data.data === 'object' ? JSON.stringify(data.data) : data.data}</span>`;
                    }

                    Swal.fire({
                        icon: 'error',
                        title: `Error en la llamada (HTTP ${data.status_code})`,
                        html: errorMessage
                    });
                }
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error Interno del Dashboard',
                    text: error.toString()
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    resultados_ui = []
    activos = 0
    caidos = 0
    
    for s in SERVICIOS:
        url_completa = f"{s['url']}?{s['params']}" if s['params'] else s['url']
        estado = "ERROR"
        respuesta_texto = "ERROR: Connect timed out / Socket Blocked"
        
        method = s.get('method', 'GET')
        headers = s.get('headers', {})
        json_data = s.get('json', None)

        try:
            # Hacemos la peticion a cada URL
            if method == 'POST':
                r = requests.post(url_completa, headers=headers, json=json_data, timeout=2.0)
            else:
                r = requests.get(url_completa, headers=headers, timeout=2.0)
                
            if r.status_code >= 200 and r.status_code < 400:
                estado = "ACTIVO"
                activos += 1
                try:
                    respuesta_texto = json.dumps(r.json(), ensure_ascii=False)
                except:
                    respuesta_texto = f"[HTML/Texto] {len(r.text)} bytes devueltos"
            else:
                caidos += 1
                respuesta_texto = f"ERROR: HTTP {r.status_code} - {r.text[:50]}"
                
        except Exception as e:
            caidos += 1
            if 'WinError 10013' in str(e):
                respuesta_texto = "ERROR: Socket Blocked (Network Boost / Firewall)"
            elif 'Read timed out' in str(e) or 'ConnectTimeout' in str(e):
                respuesta_texto = "ERROR: Connect timed out"
            else:
                respuesta_texto = f"ERROR: {str(e)[:40]}..."

        resultados_ui.append({
            "nombre": s['nombre'],
            "url": s['url'],
            "method": method,
            "params": s['params'],
            "json": json_data,
            "estado": estado,
            "respuesta": respuesta_texto
        })

    # ========= PREPARAR SNAPSHOT Y ENVIAR A FIREBASE =========
    snapshot = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estadisticas": {
            "activos": activos,
            "caidos": caidos,
            "total": len(SERVICIOS)
        },
        "detalles": resultados_ui
    }
    
    # Lanzar a firebase en un hilo para no bloquear la carga de la página
    threading.Thread(target=guardar_en_firebase, args=(snapshot,)).start()

    return render_template_string(
        HTML_TEMPLATE,
        resultados=resultados_ui,
        total_activos=activos,
        total_caidos=caidos,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route('/test_api', methods=['POST'])
def test_api():
    """Endpoint proxy para probar URLs manualmente desde el dashboard."""
    req_data = request.json
    url = req_data.get('url', '')
    method = req_data.get('method', 'GET')
    params = req_data.get('params', '')
    payload = req_data.get('json', None)
    headers = req_data.get('headers', {})

    url_completa = f"{url}?{params}" if params else url
    
    try:
        if method.upper() == 'POST':
            # Si el payload es un string (desde el textarea), intentar parsearlo a dict
            if isinstance(payload, str) and payload.strip():
                try:
                    payload = json.loads(payload)
                except:
                    pass # Se enviará como texto
            res = requests.post(url_completa, headers=headers, json=payload, timeout=3.0)
        else:
            res = requests.get(url_completa, headers=headers, timeout=3.0)
            
        try:
            resp_data = res.json()
        except:
            resp_data = res.text

        return jsonify({
            "status_code": res.status_code,
            "success": 200 <= res.status_code < 400,
            "data": resp_data
        })
    except Exception as e:
        return jsonify({"success": False, "status_code": 500, "data": str(e)})

if __name__ == '__main__':
    # Usar puerto 8000 para servir
    print("🚀 Iniciando Dashboard de Microservicios Avanzado...")
    print("Ve a: http://127.0.0.1:8000")
    app.run(port=8000, debug=True)