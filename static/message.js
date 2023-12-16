const forms_list_comments = document.querySelector(".forms-list-comments");
console.log(forms_list_comments);
forms_list_comments.addEventListener("submit", (evt) => {
  evt.preventDefault();
  if (evt.target.classList.contains("follows")) {
    console.log("DOOR", evt.target.id);
    follow_user(parseInt(evt.target.id));
    forms_list_follow(evt);
  } else if (evt.target.classList.contains("delete-comment")) {
    console.log("COMMENT", evt.target.id);
    delete_comment(parseInt(evt.target.id));
    remove_comment(evt);
    const comment_icon = document.querySelector(".cmt");
    comment_icon.innerText = ` ${parseInt(comment_icon.innerText) - 1}`;
  }
});
// delete_msg = document.querySelector(".delete-msg");
// delete_msg.addEventListener("submit", (evt) => {
//   console.log("LOOK OVER HERE");
// });
async function delete_comment(comment_id, message_id) {
  data = {
    comment_id: comment_id,
  };
  const res = await axios.post("/messages/comment/delete", data);
  console.log(await res);
  if (res.data.response.commented == false) {
    const comment_icon = document.querySelector(
      `#comment_icon${res.data.response.message_id}`,
    );
    comment_icon.classList.remove("liked");
    comment_icon.classList.add("fa-regular");
    comment_icon.classList.remove("fa-solid");
  }
}

function remove_comment(evt) {
  console.log(evt.target.id);
  const comment = document.querySelector(`#comment${evt.target.id}`);
  comment.remove();
}

const comment_form = document.querySelector(".post-comment");

comment_form.addEventListener("submit", (evt) => {
  evt.preventDefault();
  console.log(evt.target.children[1].value);
  post_comment(evt);
});

async function post_comment(evt) {
  const message_id = parseInt(evt.target.id);
  const text = document.querySelector("#text_comment_form").value;
  const csrf_token = evt.target.csrf_token.value;
  const d = {
    csrf_token: csrf_token,
    message_id: message_id,
    text: text,
  };
  const data = await axios.post(`/messages/comments/add`, d);
  const comment_icon = document.querySelector(`#comment_icon${message_id}`);
  console.log(comment_icon.innerText);
  comment_icon.innerText = ` ${parseInt(comment_icon.innerText) + 1}`;
  if (!comment_icon.classList.contains("liked")) {
    comment_icon.classList.add("liked");
    comment_icon.classList.remove("fa-regular");
    comment_icon.classList.add("fa-solid");
  }
  evt.target.children[1].value = "";

  const content = `
<li id="comment${data.data.comment.id}" class="list-group-item">
  <div class="top-message">
    <div class="message">
      <a class="" href="/users/${data.data.user.id}">
        <img src="${data.data.user.image_url}" alt="" class="timeline-image" />
      </a>
      <div class="message-area">
        <a href="/users/${data.data.user.id}">@${data.data.user.username}</a>
 <span class="text-muted">${new Date(
   data.data.comment.timestamp,
 ).toLocaleDateString("en-US", {
   month: "short",
   day: "numeric",
   year: "numeric",
 })}</span>
              <p>${data.data.comment.text}</p>
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
        <li class="dropdown-ite">
 <button
            type="button"
            class="btn btn-link text-danger"
            data-bs-toggle="modal"
            data-bs-target="#delete_cmt"
          >
            <i class="fa-solid fa-trash"></i> Delete
          </button>
                  </li>
      </ul>
    </div>
  </div>
<div
  class="modal fade"
  id="delete_cmt"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="delete_cmt">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">
        Are You sure you want to delete this comment?
      </div>

      <form id="${data.data.comment.id}" class="delete-comment" method="POST">
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
  forms_list_comments.insertBefore(t, forms_list_comments.firstChild);
  const current = document.querySelector("#current");
  current.innerHTML = "0";
}
const text_comment_form = document.querySelector("#text_comment_form");
if (text_comment_form) {
  text_comment_form.addEventListener("keyup", (evt) => {
    const current = document.querySelector("#current");
    current.innerText = evt.target.value.length;
  });
}

async function trackScroll() {
  if (isBottom()) {
    console.log("You reached the bottom of the page!");
    const form = document.querySelector(".post-comment");
    const message_id = parseInt(form.attributes.id.value);
    res = await axios.post(
      "/load-comments",
      (data = {
        index: parseInt(forms_list_comments.children.length),
        message_id: message_id,
      }),
    );

    console.log(res.data);
    // Perform your action here, such as loading more content
    for (cmt of res.data) {
      const message = `
<li id="comment${cmt.id}" class="list-group-item">
  <div class="top-message">
    <div class="message">
      <div>
        <a class="" href="/users/${cmt.user_id}">
          <img src="${cmt.image_url}" alt="" class="timeline-image" />
        </a>
      </div>
      <div class="message-area">
        <a href="/users/${cmt.user_id}">@${cmt.username}</a>
         <span class="text-muted">${new Date(cmt.timestamp).toLocaleDateString(
           "en-US",
           {
             month: "short",
             day: "numeric",
             year: "numeric",
           },
         )}</span>

    <div>${cmt.text}</div>
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
          cmt.user_id != cmt.guser
            ? `
          <form id="${cmt.user_id}" class="follows" method="POST">
            ${
              cmt.follow
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
            data-bs-target="#delete_msg${cmt.id}"
          >
            <i class="fa-solid fa-trash"></i> Delete
          </button>
</li>
`
        }
      </ul>
    </div>
  </div>


<div
  class="modal fade"
  id="delete_msg${cmt.id}"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="delete_msg${cmt.id}">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">Are You sure you want to delete this post?</div>
      <form
        id="${cmt.id}"
        action="/messages/delete/${cmt.id}"
        class="delete-comment"
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
      forms_list_comments.append(t);
    }
  }
}

// Attach scroll event listener
window.addEventListener("scroll", trackScroll);
