document.addEventListener("DOMContentLoaded", () => {
    const likeForm = document.querySelectorAll(".likeForm");
    likeForm.forEach(form => {
        form.addEventListener("submit", function(event) {
            event.preventDefault();
            const action = document.querySelector(`#btn-${form.id}`);
            const tweetID = document.querySelector(`#tweetID-${form.id}`).value;
            const csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
            const user = document.querySelector(`#userLiking-${form.id}`).value;
            const likesCount = document.querySelector(`#likes-count-${form.id}`);
            const baseUrl = "http://localhost:8000";

            fetch(`/tweets/${tweetID}/${action.value}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf_token,
                    "Content-Type": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    userLiking: user,
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                if (data.message === "Ok") {
                    if (action.value === "like"){

                        action.innerHTML = '<i class="liked bi bi-heart-fill"></i>';
                        action.value = "unlike";
                        const newValue = parseInt(likesCount.innerHTML) + 1;
                        likesCount.innerHTML = newValue;

                    } else if (action.value === "unlike") {

                        action.innerHTML = '<i class="like bi bi-heart"></i>';
                        action.value = "like";
                        const newValue = parseInt(likesCount.innerHTML) - 1;
                        likesCount.innerHTML = newValue;

                    }
                }
            })
        });
    })
});