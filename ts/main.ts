const joinModal = document.querySelector("#join-modal");
const loginModal = document.querySelector("#login-modal");
const registerModal = document.querySelector("#register-modal");
const desiredPassword = document.querySelector("#register-pw") as HTMLInputElement;
const deisredPasswordConfirm = document.querySelector("#register-pw-confirm") as HTMLInputElement;
const desiredNewPassword = document.querySelector("#new-password") as HTMLInputElement;
const desiredNewPasswordConfirm = document.querySelector("#new-password-confirm") as HTMLInputElement;
const findIDModal = document.querySelector("#find-id-modal");
const findPWModal = document.querySelector("#find-pw-modal");
const modalOverlay = document.querySelector("#overlay-on-modal-up");
const seeMore = document.querySelector("#see-more");

function validatePassword () {
    deisredPasswordConfirm.setCustomValidity(desiredPassword.value === deisredPasswordConfirm.value ? "":"비밀번호가 다릅니다.");
}

function validateNewPassword () {
    desiredNewPasswordConfirm.setCustomValidity(desiredNewPassword.value === desiredNewPasswordConfirm.value ? "":"비밀번호가 다릅니다.");
}

deisredPasswordConfirm.addEventListener("keyup", validatePassword);
desiredNewPasswordConfirm.addEventListener("keyup", validateNewPassword);
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
loginModal.querySelector("#forgot-id").addEventListener("click", (event)=>{
    const closeButton = loginModal.querySelector(".close-button") as HTMLButtonElement;
    closeButton.click();
    findIDModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});
loginModal.querySelector("#forgot-pw").addEventListener("click", (event)=>{
    const closeButton = loginModal.querySelector(".close-button") as HTMLButtonElement;
    closeButton.click();
    findPWModal.classList.toggle("hidden");
    modalOverlay.classList.toggle("hidden");
});
findIDModal.querySelector("form").addEventListener("submit", (event)=>{
    event.preventDefault();
    const formData = new FormData(findIDModal.querySelector("form"));
    fetch(location.origin+"/find-id", {
        method: "POST",
        body: formData
    })
        .then(response=>response.json())
        .then(data=>{
            findIDModal.querySelector("#result").textContent = `ID는 ${data["ID"]}입니다.` || data["error"];
        })
        .catch(error=>{
            alert(`알 수 없는 오류가 발생했습니다: ${error}`);
        });
});
// document.querySelector("#join-link").addEventListener("click", (event)=>{
//     joinModal.classList.toggle("hidden");
//     modalOverlay.classList.toggle("hidden");
// });