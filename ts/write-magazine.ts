function removeLineNumber (no) {
    document
    .querySelector("#published-content-list")
    .removeChild(document.querySelector(`#existing-content-${no}`));
}
function addRow (event) {
    if (addRow.number !== undefined) {
        addRow.number +=1
    } else {
        addRow.number = 0;
    }
    const div = document.createElement("div");
    const typeInput = document.createElement("input");
    const authorInput = document.createElement("input");
    const titleInput = document.createElement("input");
    const languageInput = document.createElement("input");
    const removeThisLine = document.createElement("button");
    const number = String(addRow.number);
    typeInput.name = number + "-type";
    authorInput.name = number + "-author";
    titleInput.name = number + "-title";
    languageInput.name = number + "-language";
    typeInput.placeholder = "시, 소설, 희곡, 수필, ···";
    authorInput.placeholder = "작가";
    titleInput.placeholder = "제목";
    languageInput.placeholder = "언어";
    typeInput.required = true;
    authorInput.required = true;
    titleInput.required = true;
    languageInput.required = true;
    typeInput.spellcheck = false;
    authorInput.spellcheck = false;
    titleInput.spellcheck = false;
    languageInput.spellcheck = false;
    div.classList.add("published-content");
    removeThisLine.type = "button";
    removeThisLine.textContent = "제거";
    removeThisLine.addEventListener("click", (event)=>{
        document.querySelector("#published-content-list").removeChild(div);
    });
    languageInput.addEventListener("keydown", (event)=>{
        if (event.key === "Tab") {
            if (languageInput.parentElement === document.querySelectorAll("#published-content-list > div")[document.querySelectorAll("#published-content-list > div").length-1]) {
                event.preventDefault();
                addRow(null).focus();
            }
        }
    });
    div.appendChild(typeInput);
    div.appendChild(titleInput);
    div.appendChild(authorInput);
    div.appendChild(languageInput);
    div.appendChild(removeThisLine);
    document.querySelector("#published-content-list").appendChild(div);
    return typeInput;
}
addRow.number = document.querySelectorAll(".published-content").length;
addRow(null);