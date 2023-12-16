const active_menu_btn = document.querySelector(".following");
active_menu_btn.style.fontWeight = "bold";
active_menu_btn.style.fontSize = "1.3rem";
const card_id = document.querySelector(".card-id");
const user_id = parseInt(card_id.attributes.id.value);
// const f = document.querySelector(".forms-list");
function isBottom() {
  // Get the current scroll position
  const scrollY = window.scrollY || window.pageYOffset;

  // Get the total height of the document
  const totalHeight = document.documentElement.scrollHeight;

  // Get the height of the viewport
  const viewportHeight = window.innerHeight;

  // Check if we are near the bottom (you can adjust the "10" for a different threshold)
  // return scrollY + viewportHeight >= totalHeight - 10;
  return scrollY + viewportHeight == totalHeight;
}
async function trackScroll() {
  if (isBottom()) {
    res = await axios.post(
      "/load-following-user",
      (data = { index: forms_list.children.length, id: user_id }),
    );

    // Perform your action here, such as loading more content
    for (user of res.data) {
      const follow_item = `
<li id="user_follow${user.id}" class="list-group-item display-follow">
  <div style="display: flex; gap: 1rem">
    <a href="/users/{{user.id}}">
      <img src="${user.image_url}" class="timeline-image" alt="" />
    </a>
    <div>
      <a class="">@${user.username}</a>

    ${
      user.follow_you
        ? `
      <small class="text-muted follow-indicator"> Follows you</small>

`
        : `<span></span>`
    }
      <br />
      <small>Following <span>${user.following}</span></small>
      <small>Followers <span>${user.followers}</span></small>
      <br />
      ${user.bio}
    </div>
  </div>
${
  user.id != user.guser
    ? `
 <div class="follow-bt">
    <form id="${user.id}" class="follows-btn" method="POST">
      <button
        class="btn btn-primary btn-sm unfollow f-btn"
        data-hover="Unfollow"
      >
        <span> Following </span>
      </button>
    </form>
  </div>

`
    : `<span></span>`
}
</li>



`;
      const template = document.createElement("template");
      template.innerHTML = follow_item;
      const t = template.content;
      forms_list.append(t);
    }
  }
}

// Attach scroll event listener
window.addEventListener("scroll", trackScroll);
