#!/bin/bash

# Dominio a escanear
DOMAIN=""

# Clonar testssl.sh si no está aún
if [ ! -d "testssl.sh" ]; then
  git clone --depth 1 https://github.com/drwetter/testssl.sh.git
fi

# Ejecutar testssl.sh y generar reporte JSON
./testssl.sh/testssl.sh --jsonfile resultado.json "$DOMAIN"

# Esperar que termine
wait

# Procesar el JSON con jq para verificar versiones TLS soportadas
# Ejemplo: verificar si TLS 1.2 y TLS 1.3 están soportados
tls_versions=$(jq -r '.["test results"][] | select(.tls != null) | .tls' resultado.json | grep -o "TLS [0-9.]*" | sort -u)

echo "Versiones TLS soportadas:"
echo "$tls_versions"

# Verificar si TLS 1.2 y 1.3 están soportados
if echo "$tls_versions" | grep -q "TLS 1.2" && echo "$tls_versions" | grep -q "TLS 1.3"; then
  echo "TLS 1.2 y TLS 1.3 soportadas correctamente."
else
  echo "Advertencia: TLS 1.2 o TLS 1.3 no están soportadas correctamente."
fi

# Aquí puedes agregar más procesamiento: cifrados débiles, certificados vencidos, etc.
# Ejemplo: detectar cifrados débiles
weak_ciphers=$(jq -r '.["test results"][] | select(.cipher != null) | .cipher' resultado.json | grep -i "weak" )

if [ -n "$weak_ciphers" ]; then
  echo "Cifrados débiles detectados:"
  echo "$weak_ciphers"
else
  echo "No se detectaron cifrados débiles."
fi