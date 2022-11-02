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
var replyField = document.getElementById("replyto");
var recipientsLabel = document.getElementById("recipientsLabel");
var recipientsInputField = document.getElementById("recipients");

var getAllMessages = async () => {
  const id = reqId++;
  const q = `/messages`;
  res = await fetch(q);
  const body = document.createElement("span");
  data = await res.text();
  json = JSON.parse(data);
  let messages = json.data;
  const sanitizer = new Sanitizer();

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
    replyToElement = document.createElement("p");
    replyButton = document.createElement("button");

    replyToText = "";
    if (m && m.reply_to !== "") {
      replyToText = ` (Reply to message ${m.reply_to})`;
    }

    headerElement.setHTML(`Message ${m.id}${replyToText}`, { sanitizer });
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
    replyButton.onclick = () => {
      replyField.value = m.id;
      recipientsLabel.textContent = `Replying to message ${m.id}...`;

      const cancelButton = document.createElement("button");
      cancelButton.textContent = "Cancel";
      cancelButton.type = "button";
      cancelButton.onclick = () => {
        recipientsLabel.setHTML("");
        recipientsLabel.textContent = "Recipients:";
        recipientsInputField.hidden = 0;
        replyField.value = "";
      };

      recipientsLabel.appendChild(cancelButton);
      recipientsInputField.hidden = 1;
    };
    body.appendChild(headerElement);
    body.appendChild(senderElement);
    body.appendChild(recipientElement);
    body.appendChild(messageElement);
    body.appendChild(timestampElement);
    body.appendChild(replyToElement);
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

getAllMessages();
