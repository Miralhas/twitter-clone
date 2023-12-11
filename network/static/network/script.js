document.addEventListener("DOMContentLoaded", () => {
    const editBtn = document.querySelector("#editBtn")
    if (editBtn) {
        editBtn.addEventListener('click', function() {
            this.remove();
            const csrfToken = document.querySelector("[name='csrfmiddlewaretoken']").value;
            const editBtnDiv = document.querySelector("#editBtnDiv");
            const tweetContentDiv = document.querySelector("#tweetContentDiv");
            const tweetContentElement = document.querySelector("#tweetContent");
            const tweetContent = tweetContentElement.innerText;
            tweetContentElement.remove();
    
            const tweetTextarea = document.createElement("textarea");
            tweetTextarea.name = "newTweetContent";
            tweetTextarea.id = "newTweetContentID";
            tweetTextarea.className = "form-input border border-info form-control mb-2";
            tweetTextarea.rows = 5;
            tweetTextarea.value = tweetContent;
            tweetTextarea.focus();
    
            const submitBtn = document.createElement("button");
            submitBtn.setAttribute("type", "submit");
            submitBtn.className = "btn btn-outline-primary my-2 btn-sm";
            submitBtn.style.borderRadius = "0px";
            submitBtn.innerHTML = "Editar";
    
            tweetContentDiv.append(tweetTextarea);
            tweetContentDiv.append(submitBtn);
            
            submitBtn.addEventListener('click', () => {
                const newTweetContent = tweetTextarea.value;
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
                    console.log(data);
                    if (data.message) {
                        tweetTextarea.remove();
                        submitBtn.remove();
                        tweetContentElement.innerHTML = newTweetContent;
                        tweetContentDiv.append(tweetContentElement);
                        editBtnDiv.append(this);
                    }
                })
            })
        })
    }
})