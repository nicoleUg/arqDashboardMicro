<?php
/**
 * Ejemplo minimo de conexion PHP -> Firebase Realtime Database (REST).
 *
 * Variables requeridas:
 * FIREBASE_DB_URL
 * FIREBASE_DB_SECRET
 */

$dbUrl = 'https://arqu-8f89c-default-rtdb.firebaseio.com';
$dbSecret = 'jSQbMFQ6Cvex22J6xlJhCg7iJ1sO4oWRVHOhQnaE';

if ($dbUrl === '' || $dbSecret === '') {
    http_response_code(500);
    echo 'Faltan variables de entorno de Firebase.';
    exit;
}

function firebaseRequest(string $method, string $url, ?array $payload = null): array
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 6);

    $headers = ['Content-Type: application/json'];
    if ($payload !== null) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload, JSON_UNESCAPED_UNICODE));
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $body = curl_exec($ch);
    $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    return [
        'ok' => $body !== false && $httpCode >= 200 && $httpCode < 300,
        'status' => $httpCode,
        'error' => $error,
        'body' => $body,
    ];
}

$testData = [
    'codigo_consultado' => 'USR-001',
    'usuario_encontrado' => true,
    'fecha_consulta' => gmdate('c'),
];

$write = firebaseRequest(
    'POST',
    $dbUrl . '/sistemaMicroservicios/historialVerificaciones.json?auth=' . urlencode($dbSecret),
    $testData
);

$read = firebaseRequest(
    'GET',
    $dbUrl . '/sistemaMicroservicios.json?auth=' . urlencode($dbSecret)
);

header('Content-Type: application/json; charset=utf-8');
echo json_encode([
    'conexion' => ($write['ok'] && $read['ok']) ? 'ok' : 'error',
    'write_test' => $write,
    'microservicios_snapshot' => $read['ok'] ? json_decode((string)$read['body'], true) : null,
], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
