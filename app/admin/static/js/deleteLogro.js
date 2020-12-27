const listItems = document.querySelectorAll('.logro-li');
const atletaId = document.querySelector('.logros-title').dataset.atletaId;

for (const item of listItems) {
  const deleteButton = item.querySelector('.delete-button');
  const confirmationContainer = item.querySelector('.delete-confirmation');
  const confirmButton = confirmationContainer.querySelector('.confirmButton');
  const cancelButton = confirmationContainer.querySelector('.cancelButton');

  const itemId = item.dataset.logroId;

  deleteButton.addEventListener('click', () => {
    confirmationContainer.classList.remove('hidden');
  });

  confirmButton.addEventListener('click', async () => {
    const url = `/atletas/${atletaId}/logros/${itemId}`;

    const response = await fetch(url, {
      method: 'DELETE',
    });
    const json = await response.json();
    window.location.replace(`${location.origin}${json.redirect_to}`);
  });

  cancelButton.addEventListener('click', () => {
    confirmationContainer.classList.add('hidden');
  });
}
