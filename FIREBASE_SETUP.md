# Conexion de tu sistema a Firebase (sin Supabase)

## 1) Crear proyecto Firebase
1. Entra a https://console.firebase.google.com
2. Crea un proyecto nuevo.
3. Activa Realtime Database en modo bloqueado (recomendado).

## 2) Obtener URL de Realtime Database
En Firebase Console -> Realtime Database, copia la URL base, por ejemplo:
https://tu-proyecto-default-rtdb.firebaseio.com

## 3) Crear secreto para backend
Opciones recomendadas:
- Opcion A (rapida): usar un token de autenticacion de servicio para backend.
- Opcion B (simple para pruebas): reglas temporales con acceso autenticado de backend.

Para este ejemplo usaremos una clave de backend por variable de entorno:
- FIREBASE_DB_URL
- FIREBASE_DB_SECRET

## 4) Variables de entorno en PHP
Define en tu servidor:
- FIREBASE_DB_URL=https://tu-proyecto-default-rtdb.firebaseio.com
- FIREBASE_DB_SECRET=TU_SECRETO_BACKEND

## 5) Probar conexion
1. Ejecuta servidor PHP:
   php -S localhost:8000
2. Abre:
   http://localhost:8000/firebase_connection_example.php

Si funciona, veras JSON con:
- conexion = ok
- write_test
- microservicios_snapshot

## 6) Integracion en tu panel
El archivo webb.php ya puede guardar un snapshot del estado de microservicios en Firebase cuando las variables existen.
Si faltan variables, la web no se cae y solo muestra aviso de no configurado.

## 7) Estructura sugerida en Firebase
- /sistemaMicroservicios/colaDatos/{autoId}
- /sistemaMicroservicios/historialVerificaciones/{autoId}
- /sistemaMicroservicios/usuariosVerificacion/{codigo}
- /sistemaMicroservicios/operaciones/suma/{autoId}
- /sistemaMicroservicios/operaciones/multiplicacion/{autoId}
- /sistemaMicroservicios/operaciones/division/{autoId}
- /sistemaMicroservicios/operaciones/potencia/{autoId}
- /sistemaMicroservicios/juegos/ahorcado/{autoId}
- /sistemaMicroservicios/juegos/ticTacToe/{idPartida}
- /sistemaMicroservicios/juegos/buscaminas/{autoId}
