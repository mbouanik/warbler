const forms_list_comments = document.querySelector(".forms-list-comments");
console.log(forms_list_comments);
forms_list_comments.addEventListener("submit", (evt) => {
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
          <form id="${data.data.comment.id}" class="delete-comment" 
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
          data.data.comment.timestamp,
        ).toLocaleDateString("en-US", {
          month: "short",
          day: "numeric",
          year: "numeric",
        })}</span>
        <p>${data.data.comment.text}</p>
      </div>
    </div>
    <hr class="hr-message" />
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
