@chcp 65001
@echo off
title NXT.
echo Проверка виртуального окружения.
IF EXIST ".\venv" (
    echo Виртуальное окружение существует, активация окружения.
    call ".\venv\Scripts\activate"
) ELSE (
    echo Создание виртуального окружения. Подождите.
    call python -m venv venv
    echo Активация окружения.
    call ".\venv\Scripts\activate"
    echo Установка библиотек. Подождите.
    call python -m pip install --upgrade pip
    call pip install -r ".\req.txt"
)
echo Выберите программу для запуска.
echo "1) Программа для Xcos-модели (Задание 1)"
echo "2) Программа для Xcos-модели (Задание 2)"
echo "3) Программа для вычисления угловой скорости"

:m
set /p var=Введите номер:
if %var% equ 1 (
    call python nxt.py
) else if %var% equ 2 (
    call python nxt2.py
) else if %var% equ 3 (
    echo "Выберите параметры запуска или оставьте поле пустым (-h для справки)"
    :new
    set /p params=Параметры:
    if "%params%" equ "-h" (
        goto h
    ) else if "%params%" equ "--help" (
        goto h
    ) else (
        goto eh
    )
    :h
    call python test_data.py -h
    goto new
    :eh
    call python test_data.py %params%
    goto e
) else (
    echo Неправильный ввод
    goto m
)
:e

call ".\venv\Scripts\deactivate"
pause