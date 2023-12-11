document.addEventListener("DOMContentLoaded", () => {
    const editForms = document.querySelectorAll(".editForm");
    editForms.forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            const tweetPK = this.id;
            const newTweetContent = document.querySelector(`#editTextarea-${tweetPK}`).value;
            const tweetOwnerPK = document.querySelector(`#tweetOwnerPK-${tweetPK}`).value;
            const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").value;

            const tweetContent = document.querySelector(`.tweetContent-${tweetPK}`);

            fetch(`/tweets/${tweetPK}/edit`, {
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    tweet_pk: parseInt(tweetPK),
                    tweet_owner: parseInt(tweetOwnerPK),
                    new_tweet_content: newTweetContent,
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                if (data.message == "Ok") {
                    tweetContent.innerText = newTweetContent;

                }
            })
        })

    })
})