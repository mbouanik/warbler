// const forms_list = document.querySelector(".forms-list");
// console.log(forms_list);
// forms_list.addEventListener("submit", (evt) => {
//   evt.preventDefault();
//   if (evt.target.classList.contains("like_form")) {
//     console.log("HELLO WORLD ", evt.target.id);
//     like_form(evt);
//   } else if (evt.target.classList.contains("repost_form")) {
//     repost_form(evt);
//     console.log("Azzur ", evt.target.id);
//   } else if (evt.target.classList.contains("delete-msg")) {
//     console.log("MOUNTAIN", evt.target.id);
//     evt.preventDefault();
//     delete_msg(evt);
//     msgs = document.querySelectorAll(`#msg${evt.target.id}`);
//     msgs.forEach((msg) => {
//       msg.remove();
//     });
//   }
//   //   else if (evt.target.classList.contains("follows")) {
//   //   console.log("DOOR", evt.target.id);
//   //   follow_user(evt);
//   //   console.log();
//   //   if (evt.target[0].innerText == "Follow") {
//   //     evt.target[0].innerText = "Unfollow";
//   //   } else {
//   //     evt.target[0].innerText = "Follow";
//   //   }
//   // }
// });
//
// async function follow_user(evt) {
//   follow_id = evt.target.id;
//   data = {
//     follow_id: parseInt(follow_id),
//   };
//   res = await axios
//     .post("/users/follow", data)
//     .then(function (response) {
//       console.log(response);
//     })
//     .catch(function (error) {
//       console.log(error);
//     });
// }
//
// function like_form(evt) {
//   evt.preventDefault();
//   // console.log(evt.target.id);
//   const msg_id = parseInt(evt.target.id);
//   const res = like(msg_id);
//   const like_icon = document.querySelector(`#like_icon${msg_id}`);
//   const stat_likes = document.querySelector(".stat-likes");
//   if (like_icon.classList.contains("fa-regular")) {
//     like_icon.classList.remove("fa-regular");
//     like_icon.classList.add("fa-solid");
//     like_icon.classList.add("liked");
//     // console.log(like_icon.innerText);
//     like_icon.innerText = ` ${parseInt(like_icon.innerText) + 1}`;
//     stat_likes.innerText = `${parseInt(stat_likes.innerText) + 1}`;
//   } else {
//     like_icon.classList.remove("fa-solid");
//     like_icon.classList.add("fa-regular");
//     like_icon.classList.remove("liked");
//     // console.log(like_icon.innerText);
//     console.log(evt.target[0].children[0].innerText);
//     stat_likes.innerText = `${parseInt(stat_likes.innerText) - 1}`;
//     like_icon.innerText = ` ${parseInt(like_icon.innerText) - 1}`;
//     msgs = document.querySelectorAll(`#msg${evt.target.id}`);
//     // msgs.forEach((msg) => {
//     //   msg.remove();
//     // });
//   }
// }
//
// async function like(msg_id) {
//   const data = {
//     message_id: parseInt(msg_id),
//   };
//   const rest = await axios
//     .post(`/messages/like`, data)
//     .then(function (response) {
//       console.log(response);
//     })
//     .catch(function (error) {
//       console.log(error);
//     });
// }
//
// // console.log(repost_forms);
// function repost_form(evt) {
//   evt.preventDefault();
//   const msg_id = parseInt(evt.target.id);
//   repost(msg_id);
//   const repost_icon = document.querySelector(`#repost_icon${msg_id}`);
//   if (repost_icon.classList.contains("reposted")) {
//     repost_icon.classList.remove("reposted");
//     repost_icon.innerText = ` ${parseInt(repost_icon.innerText) - 1}`;
//   } else {
//     repost_icon.classList.add("reposted");
//     repost_icon.innerText = ` ${parseInt(repost_icon.innerText) + 1}`;
//   }
// }
//
// async function repost(msg_id) {
//   const data = {
//     message_id: msg_id,
//   };
//   res = await axios
//     .post("/messages/repost", data)
//     .then(function (response) {
//       console.log(response);
//     })
//     .catch(function (error) {
//       console.log(error);
//     });
// }
//
// async function delete_msg(evt) {
//   const msg_id = evt.target.id;
//   data = {
//     message_id: msg_id,
//   };
//   await axios.post("messages/delete", data);
//   stat_msg = document.querySelector(".stat-msg");
//   stat_msg.innerText = `${parseInt(stat_msg.innerText) - 1}`;
// }
//
// // const ul = document.querySelector(".list-group");
// // const post_form = document.querySelector("#post-form");
// // // console.log(post_form);
// // post_form.addEventListener("submit", async (evt) => {
// //   evt.preventDefault();
// //   const text = document.querySelector("textarea");
// //   post_message(text.value);
// //   text.value = "";
// //
// //   stat_msg = document.querySelector(".stat-msg");
// //   stat_msg.innerText = `${parseInt(stat_msg.innerText) + 1}`;
// // });
