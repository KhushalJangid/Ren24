const showModalDialog = (eventId) => {
  let modal = document.getElementById(`modal-${eventId}`);
  modal.style.display = 'block';
  modal.addEventListener('click', (e) => {
    let closeBtn = document.getElementById(`close-modal-btn-${eventId}`);
    if (e.target === modal || e.target === closeBtn) {
      modal.style.display = 'none';
    }
  });
}

const buyNow = (eventId, eventName) => {
  if (confirm(`Are you sure you want to buy a ticket for ${eventName}? 
          This will be used from your Ren pass.`) == true) {
    window.location = `/buy/${eventId}`;
  }
}
function getCurrentUrl() {
  return window.location.href;
}

function updateUrl(parameter, value) {
  // Get the current URL
  var currentUrl = getCurrentUrl();
  var paramIndex = currentUrl.lastIndexOf(parameter + '=');
  if (paramIndex === -1) {
    var separator = currentUrl.indexOf('?') !== -1 ? '&' : '?';
    var newUrl = currentUrl + separator + parameter + '=' + value;
    window.location.href = newUrl;
  } else {
    var paramStart = paramIndex + parameter.length + 1;
    var paramEnd = currentUrl.indexOf('&', paramStart);
    if (paramEnd === -1) {
      paramEnd = currentUrl.length;
    }
    var existingValue = currentUrl.substring(paramStart, paramEnd);
    var updatedUrl = currentUrl.replace(parameter + '=' + existingValue, parameter + '=' + value);
    window.location.href = updatedUrl;
  }
}