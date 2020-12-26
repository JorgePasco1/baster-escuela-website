const deleteButton = document.getElementById("deleteButton");
const alumnoId = deleteButton.dataset.alumnoId;

deleteButton.addEventListener("click", async () => {
  const url = `/alumnos/${alumnoId}`;

  const response = await fetch(url, {
    method: "DELETE",
  });

  const json = await response.json()
  console.log(json)

  window.location.replace(`${location.origin}${json.redirect_to}`);
});
