let slideIndex = 1;
    let timeout;

    let plusDivs = (n) => showDivs(slideIndex += n);

    let showDivs = (n) => {
        clearTimeout(timeout);
        let i;
        let x = document.getElementsByClassName("slide");
        console.log(x)
        if (n > x.length) {
            slideIndex = 1
        }
        if (n < 1) {
            slideIndex = x.length
        }
        for (i = 0; i < x.length; i++) {
            x[i].classList.remove("active");
            x[i].classList.add("hidden");
        }
        x[slideIndex - 1].classList.remove("hidden");
        x[slideIndex - 1].classList.add("active");
        timeout = setTimeout(() => plusDivs(1), 5000);
    }

    window.onload = () => {
        timeout = setTimeout(() => showDivs(slideIndex), 5000);
    }