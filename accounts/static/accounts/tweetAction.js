document.addEventListener("DOMContentLoaded", () => {
    const editTweetForms = document.querySelectorAll(".editTweetForm");
    editTweetForms.forEach(form => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            const tweetPK = form.id;
            const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").value;
            const absolutePath = document.querySelector(`path-${tweetPK}`);
            const editTweetDiv = document.querySelector(`.editTweetDiv-${tweetPK}`);
            const oldTweetContentElement = document.querySelector(`.tweetContent-${tweetPK}`);
            const tweetCard = document.querySelector(`#tweetCard-${tweetPK}`);
            const profileTweets = document.querySelector(".profile-tweets");

            fetch(`/tweets/${tweetPK}/delete`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    tweet_pk: tweetPK,
                    request_user: requestUserPK
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Ok") {
                    tweetCard.remove();
                    let newValue = parseInt(profileTweets.innerHTML) - 1;
                    profileTweets.innerHTML = newValue;
                }
            })
        })
    })
})