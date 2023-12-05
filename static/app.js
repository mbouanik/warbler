const profile_stat_follow_form = document.querySelector(
  ".profile-stat-follow-form",
);
profile_stat_follow_form.addEventListener("submit", (evt) => {
  if (evt.target.classList.contains("follows-stat")) {
    evt.preventDefault();
    follow_user(evt);
    if (evt.target[0].innerText == "Follow") {
      evt.target[0].innerText = "Following";
      evt.target[0].classList.remove("btn-outline-primary");
      evt.target[0].classList.add("btn-primary");
      evt.target[0].classList.add("unfollow");
      evt.target[0].setAttribute("data-hover", "Unfollow");
    } else {
      evt.target[0].innerText = "Follow";
      evt.target[0].classList.remove("btn-primary");
      evt.target[0].classList.remove("unfollow");
      evt.target[0].classList.add("btn-outline-primary");
    }
    menus = document.querySelectorAll(".follows");
    menus.forEach((menu) => {
      // console.log(menu.id);
      // console.log(evt.target.id);
      console.log(menu.children[0].classList.value);
      if (menu.id == evt.target.id)
        if (menu.children[0].innerText == "Follow") {
          menu.children[0].innerText = "Unfollow";
          // memu.children[0].classList.value.add("unfollow");
        } else {
          menu.children[0].innerText = "Follow";
          // memu.children[0].classList.value.remove("unfollow");
        }
    });
  }
});
// const forms_list = document.querySelector(".forms-list");

forms_list.addEventListener("submit", (evt) => {
  evt.preventDefault();
  if (evt.target.classList.contains("follows")) {
    console.log("DOOR", evt.target.id);
    follow_user(evt);
    const stat_follow_btn = document.querySelector(".stat-follow-btn");
    if (stat_follow_btn.innerText == "Follow") {
      stat_follow_btn.innerText = "Following";
      stat_follow_btn.classList.add("btn-primary");
      stat_follow_btn.classList.remove("btn-outline-primary");
      stat_follow_btn.classList.add("unfollow");
      stat_follow_btn.setAttribute("data-hover", "Unfollow");
    } else {
      stat_follow_btn.innerText = "Follow";
      stat_follow_btn.classList.remove("btn-primary");
      stat_follow_btn.classList.remove("unfollow");
      stat_follow_btn.classList.add("btn-outline-primary");
    }
    console.log(stat_follow_btn);

    // console.log();
    // if (evt.target[0].innerText == "Follow") {
    //   evt.target[0].innerText = "Unfollow";
    // } else {
    //   evt.target[0].innerText = "Follow";
    // }
    menus = document.querySelectorAll(".follows");
    menus.forEach((menu) => {
      // console.log(menu.id);
      // console.log(evt.target.id);
      console.log(menu.children[0]);
      if (menu.id == evt.target.id)
        if (menu.children[0].innerText == "Follow") {
          menu.children[0].innerText = "Unfollow";
          // memu.children[0].classList.value.add("unfollow");
        } else {
          // memu.children[0].classList.value.remove("unfollow");
          menu.children[0].innerText = "Follow";
        }
    });
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
