const active_menu_btn = document.querySelector(".likes");
active_menu_btn.style.fontWeight = "bold";
active_menu_btn.style.fontSize = "1.3rem";
const card_id = document.querySelector(".card-id");
const user_id = parseInt(card_id.attributes.id.value);
let prev = 9;
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
  const index = forms_list.children.length;
  if (isBottom() && index > prev) {
    // console.log("You reached the bottom of the page!");
    // load_more();
    prev = index;
    res = await axios.post(
      "/load-likes-post",
      (data = { index: index, id: user_id }),
    );

    // Perform your action here, such as loading more content
    for (pst of res.data) {
      const post = `
<li id="post${pst.id}" class="list-group-item">
  <div class="top-message">
    <div class="message">
      <div>
        <a class="" href="/users/${pst.user_id}">
          <img src="${pst.image_url}" alt="" class="timeline-image" />
        </a>
      </div>
      <div class="message-area">
        <a href="/users/${pst.user_id}">@${pst.username}</a>
         <span class="text-muted">${new Date(pst.timestamp).toLocaleDateString(
           "en-US",
           {
             month: "short",
             day: "numeric",
             year: "numeric",
           },
         )}</span>

    <div>${pst.text}</div>
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
          pst.user_id != pst.guser
            ? `
          <form id="${pst.user_id}}" class="follows" method="POST">
            ${
              pst.follow
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
            data-bs-target="#delete_post${pst.id}"
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
  <div id="post${pst.id}" class="like-btn">
    <div class="interaction">
      <form id="${pst.id}}" class="like-form" method="POST">
        <button class="btn">
            ${
              pst.like
                ? ` <i id="like_icon${pst.id}" class="fa-solid fa-thumbs-up liked">
            ${pst.likes_cnt}
          </i>`
                : `<i id="like_icon${pst.id}" class="fa-regular fa-thumbs-up not-liked">
            ${pst.likes_cnt}
          </i>`
            }
        </button>
      </form>
    </div>
    <div class="interaction">
      <a class="btn primary" href="/posts/${pst.id}">
        ${
          pst.commented
            ? ` <i
          id="comment_icon${pst.id}"
          class="fa-sharp fa-solid fa-comments liked cmt"
        >
          ${pst.cmt_cnt}
        </i>
`
            : ` <i
          id="comment_icon${pst.id}"
          class="fa-sharp fa-regular fa-comments not-commented cmt"
        >
          ${pst.cmt_cnt}
        </i>
`
        }
             </a>
    </div>
    <div class="interaction">
      <form id="${pst.id}" class="repost-form" method="POST">
        <button class="btn">
        ${
          pst.repost
            ? ` <i id="repost_icon${pst.id}" class="fa-solid fa-retweet reposted">
            ${pst.repost_cnt}
          </i>`
            : `<i
            id="repost_icon${pst.id}"
            class="fa-solid fa-retweet not-reposted"
          >
            ${pst.repost_cnt}
          </i>`
        }
                 </button>
      </form>
    </div>
  </div>


<div
  class="modal fade"
  id="delete_post${pst.id}"
  tabindex="-1"
  aria-labelledby="exampleModalLabel"
  aria-hidden="true"
>
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="delete_post${pst.id}">Modal title</h1>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="modal"
          aria-label="Close"
        ></button>
      </div>
      <div class="modal-body">Are You sure you want to delete this post?</div>
      <form
            id="${pst.id}"
            action="/posts/delete/${pst.id}"
            class="delete-post"
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
      template.innerHTML = post;
      const t = template.content;
      forms_list.append(t);
    }
  }
}

// Attach scroll event listener
window.addEventListener("scroll", trackScroll);
