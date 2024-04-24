#!/bin/bash

# DjAdmin v1.0.20240424
# https://github.com/kanmain/djadmin

# chmod +x runserver.sh
# ./runserver.sh local

# Update your venv path: sample in ,venv/bin/activate
venv_path=.venv/bin/activate

# Check if a virtual environment is active
is_venv_active() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Virtual environment is active: $VIRTUAL_ENV"
    else
        echo "No virtual environment is active."
        return 1  # Return failure status code (non-zero)
    fi
}

# Function to activate virtual environment
activate_virtualenv() {
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        # Try activate from variable venv_path
        source $venv_path
        is_venv_active
    fi
}

# Function to set environment variables
set_env_vars() {
    export DJANGO_SETTINGS_MODULE="config.settings.$1"
}

# Main function
main() {
    
    case "$1" in
        "local")
            activate_virtualenv
            set_env_vars "local"
            ;;
        "dev")
            activate_virtualenv
            set_env_vars "dev"
            run_server
            ;;
        "staging")
            activate_virtualenv
            set_env_vars "staging"
            ;;
        "production")
            # Ensure that the necessary configurations are set for production
            # For example, collect static files, set up the database, etc.
            activate_virtualenv
            set_env_vars "production"
            ;;
        *)
            echo "Usage: $0 {local|dev|staging|production} {runserver|makemigrations|migrate}"
            exit 1
            ;;
    esac

    case "$2" in
        "makemigrations")
            python manage.py makemigrations
            ;;
        "migrate")
            python manage.py migrate
            ;;
         *)
            python manage.py runserver
            ;;
    esac
}

main "$@"
