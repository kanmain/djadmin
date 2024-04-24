#!/bin/bash

# DjAdmin v1.0
# 20240424 - bukanmainapp@gmail.com

# chmod +x runserver.sh
# ./runserver.sh local

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
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        is_venv_active
        # echo "Virtual environment not found. Please create a virtual environment."
        # exit 1
    fi
}

# Function to set environment variables
set_env_vars() {
    export DJANGO_SETTINGS_MODULE="config.settings.$1"
    # Add other environment variables if needed
}

# Function to run Django server
run_server() {
    python manage.py runserver
}

# Main function
main() {
    case "$1" in
        "local")
            activate_virtualenv
            set_env_vars "local"
            run_server
            ;;
        "dev")
            activate_virtualenv
            set_env_vars "dev"
            run_server
            ;;
        "staging")
            activate_virtualenv
            set_env_vars "staging"
            run_server
            ;;
        "production")
            # Ensure that the necessary configurations are set for production
            # For example, collect static files, set up the database, etc.
            activate_virtualenv
            set_env_vars "production"
            run_server
            ;;
        *)
            echo "Usage: $0 {local|dev|staging|production}"
            exit 1
            ;;
    esac
}

main "$@"
