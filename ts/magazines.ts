document.querySelectorAll(".item").forEach((element)=>{
    const info = element.parentNode.querySelector(".content-info") as HTMLElement;
    element.querySelector("img").addEventListener("click", (event)=>{
        info.style.display = "block";
        element.classList.toggle("hidden");
    });
    element.parentNode.querySelector(".hide-content").addEventListener("click", (event)=>{
        info.style.removeProperty("display");
        element.classList.toggle("hidden");
    });
});