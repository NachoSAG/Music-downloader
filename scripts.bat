@echo off

:: Comprobar si el entorno virtual ya existe
if not exist mi_entorno (
    echo Creando entorno virtual...
    python -m venv mi_entorno
    if errorlevel 1 (
        echo Error al crear el entorno virtual.
        pause
        exit /b 1
    )
)

:: Activar el entorno virtual
echo Activando entorno virtual...
call mi_entorno\Scripts\activate
if errorlevel 1 (
    echo Error al activar el entorno virtual.
    pause
    exit /b 1
)

echo Entorno virtual activado correctamente.