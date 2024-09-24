#!/bin/bash

# Función para ejecutar comandos de Django
run_django_command() {
    docker-compose run --rm web python manage.py $@
}

manage_whitelist() {
    echo "Gestión de la lista blanca:"
    echo "1) Agregar usuario"
    echo "2) Eliminar usuario"
    echo "3) Listar usuarios"
    echo "4) Volver al menú principal"

    read -p "Seleccione una opción: " whitelist_option

    case $whitelist_option in
        1)
            read -p "Ingrese el Telegram ID del usuario a agregar: " telegram_id
            run_django_command shell -c "from bot.models import TelegramUser; TelegramUser.objects.get_or_create(telegram_id='$telegram_id')"
            echo "Usuario agregado a la lista blanca."
            ;;
        2)
            read -p "Ingrese el Telegram ID del usuario a eliminar: " telegram_id
            run_django_command shell -c "from bot.models import TelegramUser; TelegramUser.objects.filter(telegram_id='$telegram_id').delete()"
            echo "Usuario eliminado de la lista blanca."
            ;;
        3)
            echo "Usuarios en la lista blanca:"
            run_django_command shell -c "from bot.models import TelegramUser; print('\n'.join([user.telegram_id for user in TelegramUser.objects.all()]))"
            ;;
        4)
            return
            ;;
        *)
            echo "Opción no válida"
            ;;
    esac

    manage_whitelist
}

# Función para mostrar el menú
show_menu() {
    echo "Selecciona una opción:"
    echo "1) Crear superusuario"
    echo "2) Hacer migraciones"
    echo "3) Aplicar migraciones"
    echo "4) Shell de Django"
    echo "5) Ejecutar comando personalizado"
    echo "6) Gestionar lista blanca"
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
        6)
            manage_whitelist
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
