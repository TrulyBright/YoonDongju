const joinModal = document.querySelector("#join-modal");
const modalOverlay = document.querySelector("#overlay-on-modal-up");

document.querySelector("#join-link").addEventListener("click", (event)=>{
    joinModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});
document.querySelectorAll(".close-button").forEach((button)=>{
    button.addEventListener("click", (event)=>{
        (button.parentNode as HTMLElement).classList.toggle("hidden");
        modalOverlay.classList.toggle("hidden");
    });
});