function addRow (event) {
    //@ts-expect-error
    if (addRow.number !== undefined) {
        //@ts-expect-error
        addRow.number +=1
    } else {
        //@ts-expect-error
        addRow.number = 0;
    }
    const div = document.createElement("div");
    const typeInput = document.createElement("input");
    const authorInput = document.createElement("input");
    const titleInput = document.createElement("input");
    const languageInput = document.createElement("input");
    const removeThisLine = document.createElement("button");
    //@ts-expect-error
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
    div.appendChild(authorInput);
    div.appendChild(titleInput);
    div.appendChild(languageInput);
    div.appendChild(removeThisLine);
    document.querySelector("#published-content-list").appendChild(div);
    return typeInput;
}
addRow(null);