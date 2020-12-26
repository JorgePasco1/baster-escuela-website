const deleteButton = document.getElementById('deleteButton');
const confirmationContainer = document.querySelector('.delete-confirmation');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');
const personaId = deleteButton.dataset.personaId;
const type = deleteButton.dataset.type;

deleteButton.addEventListener('click', () => {
  confirmationContainer.classList.remove('hidden');
});

confirmButton.addEventListener('click', async () => {
  const url = `/${type}/${personaId}`;

  const response = await fetch(url, {
    method: 'DELETE',
  });

  const json = await response.json();
  console.log(json);

  window.location.replace(`${location.origin}${json.redirect_to}`);
});

cancelButton.addEventListener('click', () => {
  console.log('cancel button');
  confirmationContainer.classList.add('hidden');
});
