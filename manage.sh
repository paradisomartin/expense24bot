#!/bin/bash

# Función para ejecutar comandos de Django
run_django_command() {
    docker-compose run --rm web python manage.py $@
}

# Función para mostrar el menú
show_menu() {
    echo "Selecciona una opción:"
    echo "1) Crear superusuario"
    echo "2) Hacer migraciones"
    echo "3) Aplicar migraciones"
    echo "4) Shell de Django"
    echo "5) Ejecutar comando personalizado"
    echo "q) Salir"
}

# Bucle principal
while true; do
    show_menu
    read -p "Opción: " choice

    case $choice in
        1)
            run_django_command createsuperuser
            ;;
        2)
            run_django_command makemigrations
            ;;
        3)
            run_django_command migrate
            ;;
        4)
            run_django_command shell
            ;;
        5)
            read -p "Ingresa el comando de Django: " custom_command
            run_django_command $custom_command
            ;;
        q)
            echo "Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida"
            ;;
    esac

    echo
done