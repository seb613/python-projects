# Instrukcja

## Do UI używamy PyQt6

1. **Instalujemy UV - menedżer środowiska python**
    ```sh
    pip install uv
    ```

2. **Synchronizujemy pakiety**
    ```sh
    uv venv
    uv sync
    ```


3. **Odpalamy program**
    ```sh
    uv run main.py
    ```

## Inne

1. **Dodawanie pakietów**
    ```sh
    uv add <pakiet>
    ```

2. **Jak poprzednie nie działa (nie polecam)**
    ```sh
    uv pip install <pakiet>
    ```

3. **Odpalenie designera**
    ```sh
    uv run designer.py
    #muszą być zsynchronizowane pakiety
    ```

4. **Konwersja .ui na pythona**
    ```sh
    uv run  pyuic6 -x Design_Files/main.ui -o Windows/mainwindow.py 
    ```
