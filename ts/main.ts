const joinModal = document.querySelector("#join-modal");
const loginModal = document.querySelector("#login-modal");
const registerModal = document.querySelector("#register-modal");
const modalOverlay = document.querySelector("#overlay-on-modal-up");
const seeMore = document.querySelector("#see-more");

document.querySelector("#register").addEventListener("click", (event)=>{
    registerModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});
document.querySelectorAll(".close-button").forEach((button)=>{
    button.addEventListener("click", (event)=>{
        (button.parentNode as HTMLElement).classList.toggle("hidden");
        modalOverlay.classList.toggle("hidden");
    });
});
seeMore.addEventListener("click", (event)=>{
    document.querySelector("#header-menu").classList.toggle("open");
});
document.querySelector("#login").addEventListener("click", (event)=>{
    loginModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});
document.querySelector("#join-link").addEventListener("click", (event)=>{
    joinModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});