const convertToHanja = ()=> document.querySelectorAll(".convertable").forEach((element)=>{
    element.innerHTML = element.innerHTML.replaceAll(new RegExp("([\u3400-\u9FBF]+)", "g"), '<span class="hanja">$1</span>');
});
const input = document.getElementsByName("content")[0];
const preview = document.querySelector(".preview");
// @ts-expect-error
marked.setOptions({
    headerIds: false,
})
// @ts-expect-error
preview.innerHTML = marked.parse(input.value);
input.addEventListener("input", (event)=>{
    // @ts-expect-error
    preview.innerHTML = marked.parse(input.value);
    convertToHanja();
});
function addParticipant (event) {
    //@ts-expect-error
    if (addParticipant.number !== undefined) {
        //@ts-expect-error
        addParticipant.number +=1
    } else {
        //@ts-expect-error
        addParticipant.number = 0;
    }
    const div = document.createElement("div");
    const newParticipant = document.createElement("input");
    const removeThisParticipant = document.createElement("button");
    newParticipant.type = "text";
    //@ts-expect-error
    newParticipant.name = "participant"+String(addParticipant.number);
    newParticipant.placeholder = "참여자";
    newParticipant.required = true;
    // newParticipant.addEventListener("keydown", (event)=>{
    //     // BUG: keydown 이벤트가 첫 번째 input 이후로는 작동을 안 함.
    //     if (event.key === "Tab") {
    //         if (newParticipant === document.querySelectorAll("#participants input")[document.querySelectorAll("#participants input").length-1]) {
    //             event.preventDefault();
    //             addParticipant(null).focus();
    //         }
    //     }
    // });
    div.appendChild(newParticipant);
    removeThisParticipant.type = "button";
    removeThisParticipant.textContent = "제거";
    removeThisParticipant.addEventListener("click", (event)=>{
        document.querySelector("#participants").removeChild(div);
    });
    div.innerHTML+="\n";
    div.appendChild(removeThisParticipant);
    document.querySelector("#participants").appendChild(div);
    return newParticipant;
}
addParticipant(null);