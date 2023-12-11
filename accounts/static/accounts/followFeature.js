document.addEventListener("DOMContentLoaded", () => {
    const followForm = document.querySelector("#followForm");
    if (followForm) {
        followForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const followStatus = document.querySelector(".follow-status");
            const profileFollowers = document.querySelector(".profile-followers");
            const followBtn = document.querySelector(".follow-feature");
            const request_user = document.querySelector(".request_user").value;
            const user_profile = document.querySelector(".user_profile").value;
            const csrf_token = document.querySelector("[name='csrfmiddlewaretoken']").value;
            const baseUrl = "http://localhost:8000";
    
            fetch(`/follow`, {
                method:"POST",
                headers: {"X-CSRFToken": csrf_token},
                body: JSON.stringify({
                    status: followStatus.value,
                    request_user: request_user,
                    user_profile: user_profile
                })
            })
            .then(respose => respose.json())
            .then(data => {
                if (data.message == "Ok") {
                    if (followStatus.value === "follow"){
                        let newFollowers = parseInt(profileFollowers.innerHTML) + 1;
                        profileFollowers.innerHTML = newFollowers;
                        followStatus.value = "unfollow";
                        followBtn.innerHTML = '<span style="font-weight: bolder;">Unfollow &rarr;</span>';
                        followBtn.className = 'follow-feature unfollow-btn btn btn-outline-info btn-sm';
                    } else {
                        let newFollowers = parseInt(profileFollowers.innerHTML) - 1;
                        profileFollowers.innerHTML = newFollowers;
                        followStatus.value = "follow";
                        followBtn.innerHTML = '<span style="font-weight: bolder;">Follow &rarr;</span>';
                        followBtn.className = 'follow-feature follow-btn btn btn-outline-info btn-sm';
                    }
                }
            });
        });
    }
});