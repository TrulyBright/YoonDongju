let potentialRole = "user";

function setPotentialRole(role) {
    potentialRole = role;
}
function changeRole(id) {
    fetch(location.origin+`/users/${id}/modify?role=${potentialRole}`)
    .then(()=>{location.reload()})
    .catch(alert);
    hide(id);
}
function show(id) {
    const popup = document.querySelector(`#change-role-popup-${id}`) as HTMLElement;
    popup.style.display = "block";
}
function hide(id) {
    const popup = document.querySelector(`#change-role-popup${id}`) as HTMLElement;
    popup.style.removeProperty("display");
}

document.querySelectorAll("#navigator div h3").forEach((element)=>{
    element.addEventListener("click", (event)=>{
        document.querySelectorAll("#workspace > div").forEach((element)=>{
            element.classList.remove("working");
        });
        document.querySelector(`#workspace .${element.className}`).classList.toggle("working");
    });
});