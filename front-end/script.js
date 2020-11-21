$(".input").focusin(function () {
    $(this).find("span").animate({ opacity: "0" }, 200);
});

$(".input").focusout(function () {
    $(this).find("span").animate({ opacity: "1" }, 300);
});

$(".login").submit(function () {
    $(this)
        .find(".submit i")
        .removeAttr("class")
        .addClass("fa fa-check")
        .css({ color: "#fff" });
    const userNameField = document.getElementById("user-input");
    const userNameValue = userNameField.value;

    const passwordField = document.getElementById("password-input");
    const passwordValue = passwordField.value;

    if (userNameValue !== "" && passwordValue !== "") {
        $(".user-input");
        $(".submit").css({ background: "#2ecc71", "border-color": "#2ecc71" });
        $(".feedback").show().animate({ opacity: "1", bottom: "-80px" }, 400);
        $("input").css({ "border-color": "#2ecc71" });

        localStorage.setItem("user", userNameValue);

        setTimeout(function(){
            location.href = "Chat/chat.html"
        }, 1300)
    } else {
        alert("Insira um usuario e senha");
    }

    return false;
});
