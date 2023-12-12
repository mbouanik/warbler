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

  // const content = `
  // <li id="msg${data.data.message.id}" class="list-group-item">
  //   <div class="m">
  //     <button
  //       type="button"
  //       class="btn btn-sm"
  //       data-bs-toggle="dropdown"
  //       aria-expanded="false"
  //     >
  //       <i class="fa-solid fa-ellipsis"></i>
  //     </button>
  //
  //     <ul class="dropdown-menu">
  //       <li class="dropdown-item">
  //         <form id="${data.data.message.id}" class="delete-msg"
  //           method="POST">
  //           <button class="btn btn-link text-muted">Delete</button>
  //         </form>
  //       </li>
  //     </ul>
  //   </div>
  //   <div class="message">
  //     <a class="" href="/users/${data.data.user.id}">
  //       <img src="${data.data.user.image_url}" alt="" class="timeline-image" />
  //     </a>
  //     <div class="message-area">
  //       <a href="/users/${data.data.user.id}">@${data.data.user.username}</a>
  //       <span class="text-muted">${new Date(
  //         data.data.message.timestamp,
  //       ).toLocaleDateString("en-US", {
  //         month: "short",
  //         day: "numeric",
  //         year: "numeric",
  //       })}</span>
  //       <p>${data.data.message.text}</p>
  //     </div>
  //   </div>
  //   <hr class="hr-message" />
  //   <div id="msg${data.data.message.id}" class="like-btn">
  //   <div class="interaction">
  //     <form id="${data.data.message.id}" class="like_form" method="POST">
  //       <button class="btn">
  //             <i id="like_icon${
  //               data.data.message.id
  //             }" class="fa-regular fa-thumbs-up not-liked">
  //           0
  //         </i>
  //       </button>
  //     </form>
  //   </div>
  //   <div class="interaction">
  //     <a class="btn primary" href="/messages/${data.data.message.id}">
  //       <i class="fa-sharp fa-regular fa-comment not-commented">
  //         <small id="comments_count"> 0 </small>
  //       </i>
  //     </a>
  //   </div>
  //   <div class="interaction">
  //     <form id="${data.data.message.id}" class="repost_form" method="POST">
  //       <button class="btn">
  //         <i id="repost_icon${
  //           data.data.message.id
  //         }" class="fa-solid fa-retweet not-reposted">
  //           0
  //         </i>
  //       </button>
  //     </form>
  //   </div>
  // </div>
  // </li>
  //
  // `;
  const content = `<li id="msg${data.data.message.id}" class="list-group-item">
  <div class="top-message">
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
        <li class="dropdown-ite ">
          <form id="${data.data.message.id}" class="delete-msg" method="POST">
            <button class="btn btn-link text-danger">
              <i class="fa-solid fa-trash"></i> Delete
            </button>
          </form>
        </li>
    </ul>
    </div>
  </div>
  <hr class="hr-message" />
  <div id="msg${data.data.message.id}" class="like-btn">
    <div class="interaction">
      <form id="${data.data.message.id}" class="like-form" method="POST">
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
        <i
          id="comment_icon${data.data.message.id}"
          class="fa-sharp fa-regular fa-comments not-commented cmt"
        >
0
        </i>
      </a>
    </div>
    <div class="interaction">
      <form id="${data.data.message.id}" class="repost-form" method="POST">
        <button class="btn">
          <i
            id="repost_icon${data.data.message.id}"
            class="fa-solid fa-retweet not-reposted"
          >
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
  // ul.insertBefore(t, ul.firstChild);
  ul.prepend(t);
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
