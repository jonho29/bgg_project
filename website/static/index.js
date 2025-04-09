function deleteGame(gameId) {
    fetch('/delete-game', {
        method: 'POST',
        body: JSON.stringify({ gameId: gameId }),
    }).then((_res) => {
        window.location.href = '/collection';
    });
}