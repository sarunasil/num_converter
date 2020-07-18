

function toggle_password_func(username) {
    var x = document.getElementById("password_"+username);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}
