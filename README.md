# Bingo Game

A small implementation of the Bingo game with multiplayer support using FastAPI.

## Features

- Multiplayer support without use of websocket
- Player (add, ready, unready, crossed)
- Random number generation for Bingo

## Requirements

- Python 3.8+
- FastAPI
- PrettyTable
- Requests
- Colorama
- Pydantic

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/princesanjivy/bingo.git
    cd bingo
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Server

1. Navigate to the bingo directory:

    ``` bash
    cd bingo
    ```

2. Start the FastAPI server:

    ```bash
    cd server
    uvicorn main:app
    ```

3. Running the Game

    In a new terminal, navigate to the bingo directory:

    ```bash
    cd bingo
    ```

4. Start the game:

    ```bash
    python game.py
    ```

## Pull Requests
I welcome everyone to enchance this small project. Also feel free to throw some issues if you find one.

Cheers!
