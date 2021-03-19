class test {

    text_1() {

        i++;
        document.getElementById("texto").innerHTML = i;
    }
}
window.addEventListener("load", (event) => {
    var i = 0;
    document.getElementById("btn_id").addEventListener("click", function () {
        i++;
        document.getElementById("texto").innerHTML = i;
    });
});












