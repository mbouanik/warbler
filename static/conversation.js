const active_menu_btn = document.querySelector(".direct-message");
active_menu_btn.style.fontWeight = "bold";
active_menu_btn.style.fontSize = "1.3rem";

const name_list = document.querySelector(".list-name");
const name_search = document.querySelector("#name_search");
name_search.addEventListener("keyup", (evt) => {
  console.log(evt.target.value.length);
  name_list.replaceChildren();
  if (evt.target.value.length > 0) {
    name_list.replaceChildren();
    lookup(evt.target.value);
  } else {
    name_list.replaceChildren();
  }
});
async function lookup(name) {
  const data = {
    name: name,
  };
  res = await axios.post("/search-user", data);
  for (user of res.data) {
    let content = `
<li id="user_follow{{user.id}}" class="list-group-item display-follow">
  <div style="display: flex; gap: 1rem">
    <a href="/users/${user.id}">
      <img src="${user.image_url}" class="timeline-image" alt="" />
    </a>
    <div>
      <a
        href="/users/${user.id}"
        class=""
        >@${user.username}</a
      >
    <br />
      ${user.bio}
    </div>
  </div>
 <div class="follow-bt">
<a href="/conversations/new/${user.id}">  <i class="fa-solid fa-message"></i>
</a>
</div>

</li>
`;
    const template = document.createElement("template");
    template.innerHTML = content;
    const t = template.content;
    name_list.append(t);
  }
}
