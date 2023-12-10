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
//     delete_msg(evt);
//     msgs = document.querySelectorAll(`#msg${evt.target.id}`);
//     msgs.forEach((msg) => {
//       msg.remove();
//     });
//   }
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
//   console.log(evt.target.id);
//   const msg_id = parseInt(evt.target.id);
//   const res = like(msg_id);
//   const like_icon = document.querySelector(`#like_icon${msg_id}`);
//   const stat_likes = document.querySelector(".stat-likes");
//   const user_id = document.querySelector(".nav-img");
//
//   if (like_icon.classList.contains("fa-regular")) {
//     like_icon.classList.remove("fa-regular");
//     like_icon.classList.add("fa-solid");
//     like_icon.classList.add("liked");
//     console.log(like_icon.innerText);
//     like_icon.innerText = ` ${parseInt(like_icon.innerText) + 1}`;
//     if (stat_likes.attributes[0].value == user_id.attributes[0].value) {
//       stat_likes.innerText = `${parseInt(stat_likes.innerText) + 1}`;
//     }
//
//     stat_likes.innerText = `${parseInt(stat_likes.innerText) + 1}`;
//   } else {
//     like_icon.classList.remove("fa-solid");
//     like_icon.classList.add("fa-regular");
//     like_icon.classList.remove("liked");
//     console.log(like_icon.innerText);
//     stat_likes.innerText = `${parseInt(stat_likes.innerText) - 1}`;
//     like_icon.innerText = ` ${parseInt(like_icon.innerText) - 1}`;
//     if (stat_likes.attributes[0].value == user_id.attributes[0].value) {
//       stat_likes.innerText = `${parseInt(stat_likes.innerText) - 1}`;
//     }
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
//

//
// async function delete_msg(evt) {
//   const msg_id = evt.target.id;
//   data = {
//     message_id: msg_id,
//   };
//   await axios.post("/messages/delete", data);
//   stat_msg = document.querySelector(".stat-msg");
//   stat_msg.innerText = `${parseInt(stat_msg.innerText) - 1}`;
// }
//
const ul = document.querySelector(".list-group");
const post_form = document.querySelector("#post-form");
// console.log(post_form);
post_form.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  const text = document.querySelector("textarea");
  post_message(text.value);
  text.value = "";

  // stat_msg = document.querySelector(".stat-msg");
  // stat_msg.innerText = `${parseInt(stat_msg.innerText) + 1}`;
});

async function post_message(text) {
  const d = {
    text: text,
    csrf_token: document.querySelector("#csrf_token").value,
  };

  const data = await axios.post("/messages/", d);
  // console.log(data.data.user);
  // user = data.data.user;
  // console.log(user);

  const content = `
  <li id="msg${data.data.message.id}" class="list-group-item">
    <div class="m">
      <button
        type="button"
        class="btn btn-sm"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <i class="fa-solid fa-ellipsis"></i>
      </button>

      <ul class="dropdown-menu">
        <li class="dropdown-item">
          <form id="${data.data.message.id}" class="delete-msg" 
            method="POST">
            <button class="btn btn-link text-muted">Delete</button>
          </form>
        </li>
      </ul>
    </div>
    <div class="message">
      <a class="" href="/users/${data.data.user.id}">
        <img src="${data.data.user.image_url}" alt="" class="timeline-image" />
      </a>
      <div class="message-area">
        <a href="/users/${data.data.user.id}">@${data.data.user.username}</a>
        <span class="text-muted">${new Date(
          data.data.message.timestamp,
        ).toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        })}</span>
        <p>${data.data.message.text}</p>
      </div>
    </div>
    <hr class="hr-message" />
    <div id="msg${data.data.message.id}" class="like-btn">
    <div class="interaction">
      <form id="${data.data.message.id}" class="like_form" method="POST">
        <button class="btn">
              <i id="like_icon${
                data.data.message.id
              }" class="fa-regular fa-thumbs-up not-liked">
            0
          </i>
        </button>
      </form>
    </div>
    <div class="interaction">
      <a class="btn primary" href="/messages/${data.data.message.id}">
        <i class="fa-sharp fa-regular fa-comment not-commented">
          <small id="comments_count"> 0 </small>
        </i>
      </a>
    </div>
    <div class="interaction">
      <form id="${data.data.message.id}" class="repost_form" method="POST">
        <button class="btn">
          <i id="repost_icon${
            data.data.message.id
          }" class="fa-solid fa-retweet not-reposted">
            0
          </i>
        </button>
      </form>
    </div>
  </div>
  </li>
  
  `;
  const template = document.createElement("template");

  template.innerHTML = content;
  const t = template.content;
  ul.insertBefore(t, ul.firstChild);
  const current = document.querySelector("#current");
  current.innerText = "0";
}

const text_comment_form = document.querySelector("#text_post_form_home");
if (text_comment_form) {
  text_comment_form.addEventListener("keyup", (evt) => {
    const current = document.querySelector("#current");
    current.innerText = evt.target.value.length;
  });
}
