const follow_form = document.querySelector(".search-page");
follow_form.addEventListener("submit", (evt) => {
  evt.preventDefault();
  if (evt.target.classList.contains("follows")) {
    console.log("ClAIM", evt.target.id);
    follow_user(evt);
    if (evt.target[0].innerText == "Follow") {
      evt.target[0].innerText = "Unfollow";
      evt.target[0].classList.remove("btn-outline-primary");
      evt.target[0].classList.add("btn-primary");
    } else {
      evt.target[0].innerText = "Follow";
      evt.target[0].classList.remove("btn-primary");
      evt.target[0].classList.add("btn-outline-primary");
    }
  }
});

async function follow_user(evt) {
  follow_id = evt.target.id;
  data = {
    follow_id: parseInt(follow_id),
  };
  res = await axios
    .post("/users/follow", data)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}
