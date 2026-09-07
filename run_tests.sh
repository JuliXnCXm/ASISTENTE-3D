#!/bin/bash
# run_tests.sh
# Ejecuta las pruebas unitarias de la DSL usando Blender en modo headless.

echo "====================================="
echo "  Ejecutando pruebas de la DSL...    "
echo "====================================="

blender -b -P tests/test_dsl.py

if [ $? -eq 0 ]; then
    echo "====================================="
    echo "  Todas las pruebas pasaron."
    echo "====================================="
else
    echo "====================================="
    echo "  Algunas pruebas fallaron."
    echo "====================================="
    exit 1
fi
