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