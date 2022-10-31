var reqId = 0;
var anchor = document.getElementById("anchor");
var searchField = document.getElementById("search");
var recipientsField = document.getElementById("recipients");
var messageField = document.getElementById("message");
var searchBtn = document.getElementById("searchBtn");
var sendBtn = document.getElementById("sendBtn");
var allBtn = document.getElementById("allBtn");
var output = document.getElementById("output");
var header = document.getElementById("header");
var replyField = document.getElementById("reply_to");
var recipientsLabel = document.getElementById("recipientsLabel");

var getAllMessages = async () => {
  const id = reqId++;
  const q = `/messages`;
  res = await fetch(q);
  const body = document.createElement("span");
  data = await res.text();
  json = JSON.parse(data);
  let messages = json.data;
  const sanitizer = new Sanitizer();

  console.log(messages);

  output.setHTML("");

  // Sorting messages by timestamp
  messages = messages.sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  messages.forEach((m) => {
    headerElement = document.createElement("h3");
    senderElement = document.createElement("p");
    recipientElement = document.createElement("p");
    messageElement = document.createElement("p");
    timestampElement = document.createElement("p");
    replyButton = document.createElement("button");
    headerElement.setHTML("Message:", { sanitizer });
    messageElement.setHTML(`Message: ${m.message}`, { sanitizer });
    senderElement.setHTML(`From: ${m.sender}`, { sanitizer });
    recipientElement.setHTML(
      `To: ${m.recipient === "*" ? "All" : m.recipient}`,
      { sanitizer }
    );
    timestampElement.setHTML(
      `When: ${new Date(m.timestamp).toString().substring(0, 24)}`
    );
    replyButton.textContent = "Reply";
    replyButton.onclick = () => (replyField.value = m.id);
    body.appendChild(headerElement);
    body.appendChild(senderElement);
    body.appendChild(recipientElement);
    body.appendChild(messageElement);
    body.appendChild(timestampElement);
    body.appendChild(replyButton);
  });

  output.appendChild(body);
  body.scrollIntoView({
    block: "end",
    inline: "nearest",
    behavior: "smooth",
  });
  anchor.scrollIntoView();
};

// var send = async (message, recipients, reply) => {
//   const id = reqId++;
//   const q = `/new?message=${encodeURIComponent(
//     message
//   )}&recipients=${encodeURIComponent(recipients)}&reply_to=${encodeURIComponent(
//     reply
//   )}`;
//   res = await fetch(q, { method: "post" });
//   getAllMessages();
//   recipientsField.value = "";
//   messageField.value = "";
// };

// sendBtn.addEventListener("click", () =>
//   send(messageField.value, recipientsField.value, replyField.value)
// );

getAllMessages();
