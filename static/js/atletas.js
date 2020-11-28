"use strict";

const atletas = document.querySelectorAll(".atelta-clickable-photo");

const getLogros = async (playerId) => {
  const request_url = `/logros?player_id=${playerId}`
  const response = await fetch(request_url)
  const logros = await response.json();
  console.log(logros)
}

for (const atleta of atletas) {
  const playerId = atleta.dataset.player_id;
  atleta.addEventListener("click", () => getLogros(playerId))
}
