const showModalDialog = (eventId) =>{
  let modal = document.getElementById(`modal-${eventId}`);
  modal.style.display = 'block';
  modal.addEventListener('click',(e)=>{
    let closeBtn = document.getElementById(`close-modal-btn-${eventId}`);
    if(e.target === modal || e.target === closeBtn){
      modal.style.display = 'none';
    }
  });
}

const buyNow = (eventId,eventName)=>{
  if(confirm(`Are you sure you want to buy a ticket for ${eventName}? 
          This will be used from your Ren pass.`) == true){
            window.location = `/buy/${eventId}`;
          }
}