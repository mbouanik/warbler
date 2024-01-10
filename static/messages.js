const post_btn = document.querySelector(".post-btn").remove();
const message_form = document.querySelector(".message-form");
const messages_list = document.querySelector(".direct-messages");
message_form.addEventListener("submit", (evt) => {
  evt.preventDefault();
  console.log(evt.target.id);
  console.log(evt.target.children[0].value);
  send_message(evt);
  evt.target.children[1].value = "";
});

async function send_message(evt) {
  data = {
    text: evt.target.children[1].value,
    csrf_token: evt.target.children[0].value,
    conversation_id: parseInt(evt.target.id),
  };
  const res = await axios.post("/conversations/messages/new", data);
  console.log(res.data);

  const message = `
 <div class="list-group-ite d-flex " style="justify-content:flex-end; ">
        <div class="msg-sender">
            ${res.data.text}
        </div>
        </div>
     <div class="text-muted time-ago d-flex"  style="justify-content:flex-end;">
            ${res.data.timestamp}
        </div>


`;

  const template = document.createElement("template");
  template.innerHTML = message;
  const t = template.content;
  messages_list.append(t);
}

function istop() {
  // Get the current scroll position
  const scrollY = window.scrollY || window.pageYOffset;

  // Get the total height of the document
  const totalHeight = document.documentElement.scrollHeight;

  // Get the height of the viewport
  const viewportHeight = window.innerHeight;

  // Check if we are near the bottom (you can adjust the "10" for a different threshold)
  // return scrollY + viewportHeight >= totalHeight - 10;
  return scrollY + viewportHeight <= totalHeight;
}

if (istop()) {
  console.log("Hello");
}
