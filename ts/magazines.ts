document.querySelectorAll(".item").forEach((element)=>{
    const info = element.parentNode.querySelector(".content-info") as HTMLElement;
    element.addEventListener("click", (event)=>{
        info.style.display = "block";
        element.classList.toggle("hidden");
    });
});