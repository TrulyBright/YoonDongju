window.addEventListener("beforeunload", (event)=>{return true;});
const input = document.getElementsByName("content")[0];
const preview = document.querySelector(".preview");
// @ts-expect-error
preview.innerHTML = marked.parse(input.value);
input.addEventListener("input", (event)=>{
    // @ts-expect-error
    preview.innerHTML = marked.parse(input.value);
});
document.querySelector("#add-participant").addEventListener("click", (event)=>{
    const div = document.createElement("div");
    const newParticipant = document.createElement("input");
    const removeThisParticipant = document.createElement("button");
    newParticipant.type = "text";
    newParticipant.name = "participant"+String(document.querySelectorAll("#participants input").length+1);
    newParticipant.placeholder = "참여자";
    newParticipant.required = true;
    removeThisParticipant.type = "button";
    removeThisParticipant.textContent = "제거";
    removeThisParticipant.addEventListener("click", (event)=>{
        document.querySelector("#participants").removeChild(div);
    });
    div.appendChild(newParticipant);
    div.innerHTML+="\n";
    div.appendChild(removeThisParticipant);
    document.querySelector("#participants").appendChild(div);
});