// const profile_stat_follow_form = document.querySelector(
//   ".profile-stat-follow-form",
// );
// profile_stat_follow_form.addEventListener("submit", (evt) => {
//   if (evt.target.classList.contains("follows-stat")) {
//     evt.preventDefault();
//     follow_user(evt);
//     if (evt.target[0].innerText == "Follow") {
//       evt.target[0].innerText = "Following";
//       evt.target[0].classList.remove("btn-outline-primary");
//       evt.target[0].classList.add("btn-primary");
//       evt.target[0].classList.add("unfollow");
//       evt.target[0].setAttribute("data-hover", "Unfollow");
//     } else {
//       evt.target[0].innerText = "Follow";
//       evt.target[0].classList.remove("btn-primary");
//       evt.target[0].classList.remove("unfollow");
//       evt.target[0].classList.add("btn-outline-primary");
//     }
//     menus = document.querySelectorAll(".follows");
//     console.log(menus);
//     menus.forEach((menu) => {
//       // console.log(menu.id);
//       // console.log(evt.target.id);
//       // console.log(menu.id);
//       // console.log(evt.target.id);
//       // console.log(menu.children[0].innerText)
//       if (menu.id == evt.target.id) {
//         if (menu.children[0].innerText == "Follow") {
//           menu.children[0].innerText = "Unfollow";
//           // memu.children[0].classList.value.add("unfollow");
//         } else {
//           menu.children[0].innerText = "Follow";
//           // memu.children[0].classList.value.remove("unfollow");
//         }
//       }
//     });
//   } else if (evt.target.classList.contains("like_form")) {
//     console.log("HELLO WORLD ", evt.target.id);
//     evt.preventDefault();
//
//     like_form(evt);
//   }
// });
// const forms_list = document.querySelector(".forms-list");

const forms_list = document.querySelector(".forms-list");

forms_list.addEventListener("submit", (evt) => {
  evt.preventDefault();
  if (evt.target.classList.contains("follows")) {
    console.log("DOOR", evt.target.id);
    follow_user(evt);
    const stat_follow_btn = document.querySelector(".stat-follow-btn");
    const stat_following = document.querySelector(".stat-following");
    const user_id = document.querySelector(".logout");
    if (stat_follow_btn) {
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
    }

    if (
      stat_following &&
      stat_following.attributes[0].value == user_id.attributes[0].value
    ) {
      if (evt.target[0].innerText == "Unfollow") {
        console.log(evt.target.id);
        stat_following.innerText = `${parseInt(stat_following.innerText) - 1}`;
      } else {
        stat_following.innerText = `${parseInt(stat_following.innerText) + 1}`;
      }
    }
    console.log(evt.target[0].innerText);
    menus = document.querySelectorAll(".follows");
    menus.forEach((menu) => {
      console.log(menu.id);
      console.log(evt.target.id);
      console.log(menu.children[0].classList);
      if (menu.id == evt.target.id)
        if (menu.children[0].innerText == "Follow") {
          menu.children[0].innerText = "Unfollow";

          // memu.children[0].classList.add("unfollow");
        } else {
          // memu.children[0].classList.remove("unfollor");
          menu.children[0].innerText = "Follow";
        }
    });
  } else if (evt.target.classList.contains("delete-msg")) {
    console.log("MOUNTAIN", evt.target.id);
    delete_msg(evt);
    msgs = document.querySelectorAll(`#msg${evt.target.id}`);
    msgs.forEach((msg) => {
      msg.remove();
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

function like_form(evt) {
  evt.preventDefault();
  // console.log(evt.target.id);
  const msg_id = parseInt(evt.target.id);
  const res = like(msg_id);
  const like_icon = document.querySelector(`#like_icon${msg_id}`);
  const stat_likes = document.querySelector(".stat-likes");
  const user_id = document.querySelector(".logout");
  if (like_icon.classList.contains("fa-regular")) {
    like_icon.classList.remove("fa-regular");
    like_icon.classList.add("fa-solid");
    like_icon.classList.add("liked");
    // console.log(like_icon.innerText);
    console.log(stat_likes.attributes[0].value);
    // console.log(evt.target.id);
    console.log(user_id.attributes[0].value);
    like_icon.innerText = ` ${parseInt(like_icon.innerText) + 1}`;

    if (stat_likes.attributes[0].value == user_id.attributes[0].value) {
      stat_likes.innerText = `${parseInt(stat_likes.innerText) + 1}`;
    }
  } else {
    like_icon.classList.remove("fa-solid");
    like_icon.classList.add("fa-regular");
    like_icon.classList.add("not-liked");
    like_icon.classList.remove("liked");
    // console.log(like_icon.innerText);
    like_icon.innerText = ` ${parseInt(like_icon.innerText) - 1}`;

    if (stat_likes.attributes[0].value == user_id.attributes[0].value) {
      stat_likes.innerText = `${parseInt(stat_likes.innerText) - 1}`;
    }
  }
}

async function like(msg_id) {
  const data = {
    message_id: parseInt(msg_id),
  };
  const rest = await axios
    .post(`/messages/like`, data)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}

async function delete_msg(evt) {
  const msg_id = parseInt(evt.target.id);
  data = {
    message_id: msg_id,
  };
  const res = await axios.post("/messages/delete", data);
  stat_msg = document.querySelector(".stat-msg");
  stat_msg.innerText = `${parseInt(stat_msg.innerText) - 1}`;
}
