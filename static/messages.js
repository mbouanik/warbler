const active_menu_btn = document.querySelector(".direct-message");
active_menu_btn.style.fontWeight = "bold";
active_menu_btn.style.fontSize = "1.3rem";
window.scrollTo(0, document.body.scrollHeight);
const post_btn = document.querySelector(".post-btn").remove();
const message_form = document.querySelector(".message-form");
const messages_list = document.querySelector(".direct-messages");
let prev = 9;
message_form.addEventListener("submit", (evt) => {
  evt.preventDefault();
  // console.log(evt.target.id);
  // console.log(evt.target.children[0].value);
  send_message(evt);
  evt.target.children[1].value = "";
  // window.scrollTo(0, document.body.scrollHeigrt);
});

async function send_message(evt) {
  console.log(evt.target.id);
  data = {
    text: evt.target.children[1].value,
    csrf_token: evt.target.children[0].value,
    user_id: parseInt(evt.target.id),
    // user_id: parseInt(
    //   document.querySelector(".top-dmessage").attributes.id.value,
    // ),
  };
  const res = await axios.post("/conversations/messages/new", data);
  // console.log(res.data);

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
  const totalHeight = document.documentElement.scrollHeight;

  // Get the height of the viewport
  const viewportHeight = window.innerHeight;
  // Get the current scroll position
  const scrollY = window.scrollY || window.pageYOffset;
  return scrollY <= 0;
}
async function trackScroll() {
  const index = messages_list.children.length / 2;
  console.log(index, prev);

  if (istop() && index > prev) {
    prev = index;
    console.log("Hello");
    data = {
      index: index,
      user_id: parseInt(message_form.attributes.id.value),
    };
    const res = await axios.post("/load-conversation", data);
    console.log(res.data);
    for (message of res.data) {
      const msg = `
    ${
      message.guser
        ? `
 <div class="list-group-ite d-flex " style="justify-content:flex-end; ">
        <div class="msg-sender">
            ${message.text}
        </div>
        </div>
     <div class="text-muted time-ago d-flex"  style="justify-content:flex-end;">
            ${message.timestamp}
        </div>
`
        : `
    <div class="list-group-itm  d-flex dmessage " style="justify-content:flex-start;">

 <div class="msg-receiver">
            ${message.text}
        </div>
    </div>
      <div class="text-muted time-ago d-flex"  style="justify-content:flex-start;">
            ${message.timestamp}
        </div>

`
    } `;

      const template = document.createElement("template");
      template.innerHTML = msg;
      const t = template.content;
      messages_list.prepend(t);
    }
  }
}
window.addEventListener("scroll", trackScroll);
