const card_id = document.querySelector(".card-id");
const user_id = parseInt(card_id.attributes.id.value);
const f = document.querySelector(".forms-list");
console.log(f.children.length);

async function trackScroll() {
  if (isBottom()) {
    console.log("You reached the bottom of the page!");
    console.log(f.children.length);
    // load_more();
    res = await axios.post(
      "/load-profile-msg",
      (data = { index: f.children.length, id: user_id }),
    );

    console.log(res.data);
    // Perform your action here, such as loading more content
    for (msg of res.data) {
      const message = `


<li id="msg${msg.id}" class="list-group-item">
  <div class="repost-message">
${
  msg.not_original
    ? ` ${
        msg.page
          ? `
 <small style="position: absolute"
      >You reposted <i class="fa-solid fa-retweet"></i>
    </small>

`
          : `
 <small style="position: absolute"
      >${msg.page_username} reposted <i class="fa-solid fa-retweet"></i>
    </small>

`
      }

`
    : `<span></span>`
}
     </div>
  <div class="top-message">
    <div class="message">
      <div>
        <a class="" href="/users/${msg.user_id}">
          <img src="${msg.image_url}" alt="" class="timeline-image" />
        </a>
      </div>
      <div class="message-area">
        <a href="/users/${msg.user_id}">@${msg.username}</a>
         <span class="text-muted">${new Date(msg.timestamp).toLocaleDateString(
           "en-US",
           {
             month: "short",
             day: "numeric",
             year: "numeric",
           },
         )}</span>

    <div>${msg.text}</div>
      </div>
    </div>
    <div class="">
      <button
        type="button"
        class="btn btn-sm"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <i class="fa-solid fa-ellipsis"></i>
      </button>

      <ul class="dropdown-menu">
         
        </li>
        <li class="dropdown-itr text-primary">
        ${
          msg.user_id != msg.guser
            ? `
          <form id="${msg.user_id}}" class="follows" method="POST">
            ${
              msg.follow
                ? `  <button class="btn btn-link text-danger">Unfollow</button>
`
                : ` <button class="btn btn-link text-mut">Follow</button>`
            }
            </form>
        </li>
`
            : `
        <li class="dropdown-ite text-dange">

            <button
            type="button"
            class="btn btn-link text-danger"
            data-bs-toggle="modal"
            data-bs-target="#delete_msg${msg.id}"
          >
            <i class="fa-solid fa-trash"></i> Delete
          </button>
</li>
`
        }
      </ul>
    </div>
  </div>
  <!-- <hr class="hr-message" /> -->
  <div id="msg${msg.id}" class="like-btn">
    <div class="interaction">
      <form id="${msg.id}}" class="like-form" method="POST">
        <button class="btn">
            ${
              msg.like
                ? ` <i id="like_icon${msg.id}" class="fa-solid fa-thumbs-up liked">
            ${msg.likes_cnt}
          </i>`
                : `<i id="like_icon${msg.id}" class="fa-regular fa-thumbs-up not-liked">
            ${msg.likes_cnt}
          </i>`
            }
        </button>
      </form>
    </div>
    <div class="interaction">
      <a class="btn primary" href="/messages/${msg.id}">
        ${
          msg.commented
            ? ` <i
          id="comment_icon${msg.id}"
          class="fa-sharp fa-solid fa-comments liked cmt"
        >
          ${msg.cmt_cnt}
        </i>
`
            : ` <i
          id="comment_icon${msg.id}"
          class="fa-sharp fa-regular fa-comments not-commented cmt"
        >
          ${msg.cmt_cnt}
        </i>
`
        }
             </a>
    </div>
    <div class="interaction">
      <form id="${msg.id}" class="repost-form" method="POST">
        <button class="btn">
        ${
          msg.repost
            ? ` <i id="repost_icon${msg.id}" class="fa-solid fa-retweet reposted">
            ${msg.repost_cnt}
          </i>`
            : `<i
            id="repost_icon${msg.id}"
            class="fa-solid fa-retweet not-reposted"
          >
            ${msg.repost_cnt}
          </i>`
        }
                 </button>
      </form>
    </div>
  </div>


<div
  class="modal fade"
  id="delete_msg${msg.id}"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="delete_msg${msg.id}">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">Are You sure you want to delete this post?</div>
      <form
        id="${msg.id}"
        action="/messages/delete/${msg.id}"
        class="delete-msg"
        method="POST"
      >
        <div class="modal-footer">
          <button class="btn btn-danger" data-bs-dismiss="modal">Delete</button>
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
</li>
`;
      const template = document.createElement("template");
      template.innerHTML = message;
      const t = template.content;
      forms_list.append(t);
    }
  }
}

// Attach scroll event listener
window.addEventListener("scroll", trackScroll);

// const forms_list = document.querySelector(".forms-list");
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
//   await axios
//     .post("/users/follow", data)
//     .then(function (response) {
//       console.log(response);
//     })
//     .catch(function (error) {
//       console.log(error);
//     });
// }

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
//     stat_likes.innerText = `${parseInt(stat_likes.innerText) - 1}`;
//     like_icon.innerText = ` ${parseInt(like_icon.innerText) - 1}`;
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
// console.log(repost_forms);
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
//   const msg_id = parseInt(evt.target.id);
//   data = {
//     message_id: msg_id,
//   };
//   const res = await axios.post("/messages/delete", data);
//   stat_msg = document.querySelector(".stat-msg");
//   stat_msg.innerText = `${parseInt(stat_msg.innerText) - 1}`;
// }

// const ul = document.querySelector(".list-group");
// const post_form = document.querySelector("#post-form");
// // console.log(post_form);
// post_form.addEventListener("submit", async (evt) => {
//   evt.preventDefault();
//   const text = document.querySelector("textarea");
//   post_message(text.value);
//   text.value = "";
//
//   stat_msg = document.querySelector(".stat-msg");
//   stat_msg.innerText = `${parseInt(stat_msg.innerText) + 1}`;
// });
//
// async function post_message(text) {
//   const d = {
//     text: text,
//     csrf_token: document.querySelector("#csrf_token").value,
//   };
//
//   const data = await axios.post("/messages/", d);
//   // console.log(data.data.user);
//   // user = data.data.user;
//   // console.log(user);
//
//   const content = `
//   <li id="msg${data.data.message.id}" class="list-group-item">
//     <div class="m">
//       <button
//         type="button"
//         class="btn btn-sm"
//         data-bs-toggle="dropdown"
//         aria-expanded="false"
//       >
//         <i class="fa-solid fa-ellipsis"></i>
//       </button>
//
//       <ul class="dropdown-menu">
//         <li class="dropdown-item">
//           <form id="${data.data.message.id}" class="delete-msg"
//             method="POST">
//             <button class="btn btn-link text-muted">Delete</button>
//           </form>
//         </li>
//       </ul>
//     </div>
//     <div class="message">
//       <a class="" href="/users/${data.data.user.id}">
//         <img src="${data.data.user.image_url}" alt="" class="timeline-image" />
//       </a>
//       <div class="message-area">
//         <a href="/users/${data.data.user.id}">@${data.data.user.username}</a>
//         <span class="text-muted">${new Date(
//           data.data.message.timestamp,
//         ).toLocaleDateString("en-US", {
//           month: "short",
//           day: "numeric",
//           year: "numeric",
//         })}</span>
//         <p>${data.data.message.text}</p>
//       </div>
//     </div>
//   </li>
//   <div id="msg${data.data.message.id}" class="like-btn">
//     <div class="interaction">
//       <form id="${data.data.message.id}" class="like_form" method="POST">
//         <button class="btn">
//               <i id="like_icon${
//                 data.data.message.id
//               }" class="fa-regular fa-thumbs-up not-liked">
//             0
//           </i>
//         </button>
//       </form>
//     </div>
//     <div class="interaction">
//       <a class="btn primary" href="/messages/${data.data.message.id}">
//         <i class="fa-sharp fa-regular fa-comment not-commented">
//           <small id="comments_count"> 0 </small>
//         </i>
//       </a>
//     </div>
//     <div class="interaction">
//       <form id="${data.data.message.id}" class="repost_form" method="POST">
//         <button class="btn">
//           <i id="repost_icon${
//             data.data.message.id
//           }" class="fa-solid fa-retweet not-reposted">
//             0
//           </i>
//         </button>
//       </form>
//     </div>
//   </div>
//
//   `;
//   const div = document.createElement("div");
//
//   div.innerHTML = content;
//   ul.prepend(div);
// }
