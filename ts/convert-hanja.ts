export const convertToHanja = ()=> document.querySelectorAll(".convertable").forEach((element)=>{
    element.innerHTML = element.innerHTML.replaceAll(new RegExp("([\u3400-\u9FBF]+)", "g"), '<span class="hanja">$1</span>');
});
convertToHanja();