const form_list_search = document.querySelector(".forms-list-search");
form_list_search.addEventListener("submit", (evt) => {
  evt.preventDefault();
  if (evt.target.classList.contains("follows")) {
    follow_user(parseInt(evt.target.id));
    forms_list_follow(evt);
  } else if (evt.target.classList.contains("delete-msg")) {
    delete_msg(parseInt(evt.target.id));
    stat_msg = document.querySelector(".stat-msg");
    if (stat_msg) {
      stat_msg.innerText = `${parseInt(stat_msg.innerText) - 1}`;
    }
    const msg = document.querySelector(`#msg${evt.target.id}`);
    msg.remove();
  } else if (evt.target.classList.contains("like-form")) {
    like_msg(parseInt(evt.target.id));
    like_form(evt);
  } else if (evt.target.classList.contains("repost-form")) {
    repost(parseInt(evt.target.id));
    repost_form(evt);
  }
});
