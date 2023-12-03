like_form = $(".like_form");
console.log(like_form);
like_form.on("submit", (evt) => {
  evt.preventDefault();
  console.log(evt.target.id);
  const msg_id = parseInt(evt.target.id);
  const res = like(msg_id);
  const like_icon = $(`#like_icon${msg_id}`);
  if (like_icon.hasClass("fa-regular")) {
    like_icon.removeClass("fa-regular");
    like_icon.addClass("fa-solid");
    like_icon.addClass("liked");
    like_icon[0].innerText = ` ${parseInt(like_icon[0].innerText) + 1}`;
  } else {
    like_icon.removeClass("fa-solid");
    like_icon.addClass("fa-regular");
    like_icon.removeClass("liked");
    like_icon[0].innerText = ` ${parseInt(like_icon[0].innerText) - 1}`;
  }
});

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

repost_form = $(".repost_form");
console.log(repost_form);
repost_form.on("submit", (evt) => {
  evt.preventDefault();
  const msg_id = parseInt(evt.target.id);
  repost(msg_id);
  const repost_icon = $(`#repost_icon${msg_id}`);
  if (repost_icon.hasClass("reposted")) {
    repost_icon.removeClass("reposted");
    repost_icon[0].innerText = ` ${parseInt(repost_icon[0].innerText) - 1}`;
  } else {
    repost_icon.addClass("reposted");
    repost_icon[0].innerText = ` ${parseInt(repost_icon[0].innerText) + 1}`;
  }
});

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
