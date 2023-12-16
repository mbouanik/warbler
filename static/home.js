const active_menu_btn = document.querySelector(".home");
active_menu_btn.style.fontWeight = "bold";
active_menu_btn.style.fontSize = "1.3rem";
const ul = document.querySelector(".list-group");
const post_form = document.querySelector("#post-form");
post_form.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  const text = document.querySelector("textarea");
  post_message(text.value);
  text.value = "";
});

async function post_message(text) {
  const d = {
    text: text,
    csrf_token: document.querySelector("#csrf_token").value,
  };

  const data = await axios.post("/messages", d);
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
        <div>${data.data.message.text}</div>
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
  <button
            type="button"
            class="btn btn-link text-danger"
            data-bs-toggle="modal"
            data-bs-target="#delete_msg"
          >
            <i class="fa-solid fa-trash"></i> Delete
          </button>

                 </li>
    </ul>
    </div>
  </div>
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
<div
  class="modal fade"
  id="delete_msg"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="delete_msg">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">Are You sure you want to delete this post?</div>
      <form
        id="${data.data.message.id}"
        action="/messages/delete/${data.data.message.id}}"
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

function isBottom() {
  // Get the current scroll position
  const scrollY = window.scrollY || window.pageYOffset;

  // Get the total height of the document
  const totalHeight = document.documentElement.scrollHeight;

  // Get the height of the viewport
  const viewportHeight = window.innerHeight;

  // Check if we are near the bottom (you can adjust the "10" for a different threshold)
  // return scrollY + viewportHeight >= totalHeight - 10;
  return scrollY + viewportHeight >= totalHeight;
}

async function trackScroll() {
  if (isBottom()) {
    res = await axios.post(
      "/load-messages",
      (data = { index: forms_list.children.length }),
    );

    // Perform your action here, such as loading more content
    for (msg of res.data) {
      const message = `
<li id="msg${msg.id}" class="list-group-item">
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
