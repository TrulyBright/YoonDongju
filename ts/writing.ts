window.addEventListener("beforeunload", (event)=>{return true;});
const input = document.getElementsByName("content")[0];
const preview = document.querySelector(".preview");
// @ts-expect-error
preview.innerHTML = marked.parse(input.value);
input.addEventListener("input", (event)=>{
    // @ts-expect-error
    preview.innerHTML = marked.parse(input.value);
});