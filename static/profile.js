like_forms = document.querySelectorAll(".like_form");
console.log(like_forms);
for (like_form of like_forms) {
  like_form.addEventListener("submit", (evt) => {
    evt.preventDefault();
    console.log(evt.target.id);
    const msg_id = parseInt(evt.target.id);
    const res = like(msg_id);
    const like_icon = document.querySelector(`#like_icon${msg_id}`);
    if (like_icon.classList.contains("fa-regular")) {
      like_icon.classList.remove("fa-regular");
      like_icon.classList.add("fa-solid");
      like_icon.classList.add("liked");
      console.log(like_icon.innerText);
      like_icon.innerText = ` ${parseInt(like_icon.innerText) + 1}`;
    } else {
      like_icon.classList.remove("fa-solid");
      like_icon.classList.add("fa-regular");
      like_icon.classList.remove("liked");
      console.log(like_icon.innerText);

      like_icon.innerText = ` ${parseInt(like_icon.innerText) - 1}`;
    }
  });
}

async function like(msg_id) {
  const data = {
    message_id: parseInt(msg_id),
  };
  const rest = await axios
    .post(`/messages/like`, data)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}

repost_forms = document.querySelectorAll(".repost_form");
console.log(repost_forms);
for (repost_form of repost_forms) {
  repost_form.addEventListener("submit", (evt) => {
    evt.preventDefault();
    const msg_id = parseInt(evt.target.id);
    repost(msg_id);
    const repost_icon = document.querySelector(`#repost_icon${msg_id}`);
    if (repost_icon.classList.contains("reposted")) {
      repost_icon.classList.remove("reposted");
      repost_icon.innerText = ` ${parseInt(repost_icon.innerText) - 1}`;
    } else {
      repost_icon.classList.add("reposted");
      repost_icon.innerText = ` ${parseInt(repost_icon.innerText) + 1}`;
    }
  });
}

async function repost(msg_id) {
  const data = {
    message_id: msg_id,
  };
  res = await axios
    .post("/messages/repost", data)
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
}
