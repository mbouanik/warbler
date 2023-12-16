const card_id = document.querySelector(".card-id");
const user_id = parseInt(card_id.attributes.id.value);
// const f = document.querySelector(".forms-list");
// console.log(f.children.length);

async function trackScroll() {
  if (isBottom()) {
    console.log("You reached the bottom of the page!");
    console.log(forms_list.children.length);
    res = await axios.post(
      "/load-followers-user",
      (data = { index: forms_list.children.length, id: user_id }),
    );

    console.log(res.data);
    // Perform your action here, such as loading more content
    for (user of res.data) {
      const follow_item = `
<li id="user_follow${user.id}" class="list-group-item display-follow">
  <div style="display: flex; gap: 1rem">
    <a href="/users/${user.id}">
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
    ${
      user.following
        ? `<button
        class="btn btn-primary btn-sm unfollow f-btn"
        data-hover="Unfollow"
      >
        <span> Following </span>
      </button>`
        : ` <button class="btn btn-outline-primary btn-sm f-btn">
        <span> Follow </span>
      </button>
`
    }
      
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
