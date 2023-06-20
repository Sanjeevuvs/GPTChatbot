class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector('.chatbox__button'),
      chatBox: document.querySelector('.chatbox__support'),
      sendButton: document.querySelector('.send__button')
    };

    this.state = false;
    this.ApplicationName = null;
    this.chatst = null;
    this.messages = [];
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener('click', () => this.toggleState(chatBox));

    sendButton.addEventListener('click', () => this.onSendButton(chatBox));

    const node = chatBox.querySelector('input');
    node.addEventListener('keyup', ({ key }) => {
      if (key === 'Enter') {
        this.onSendButton(chatBox);
      }
    });
  }
  startChatLoop() {
    const textField = this.args.chatBox.querySelector('input');

    textField.addEventListener('keyup', ({ key }) => {
      if (key === 'Enter') {
        this.onSendButton(this.args.chatBox);
      }
    });

    textField.value = '';
    textField.focus();
  }

  toggleState(chatbox) {
    this.state = !this.state;

    // show or hide the box
    if (this.state) {
      chatbox.classList.add('chatbox--active');
    } else {
      chatbox.classList.remove('chatbox--active');
    }
  }

  onSendButton(chatbox) {
    const textField = chatbox.querySelector('input');
    const text = textField.value;

    if (text === '') {
      return;
    }
    //CreateRecord section
    else if (text.toLowerCase() === 'create record') {
      this.chatst = 'create Record';
      const fmsg8 = { name: 'User', message: text };
      this.messages.push(fmsg8);


      const fmsg9 = { name: 'Sanjeev', message: 'Please enter the application name:' };
      this.messages.push(fmsg9);
      this.updateChatText(chatbox);
      this.state = 'waitingForApplicationName';

      // Clear the input field
      textField.value = '';
      return;
    }
    else if (this.chatst === 'create Record') {
  switch (this.state) {
    case 'waitingForApplicationName':
      const applicationName = text;
      const fmsg10 = { name: 'User', message: applicationName };
      this.messages.push(fmsg10);
      this.ApplicationName=applicationName;
      // Display the loading indicator to the user
      const loadingMsg = { name: 'Sanjeev', message: 'Loading....' };
      this.messages.push(loadingMsg);
      this.updateChatText(chatbox);

      fetch('/getRecord', {
        method: 'POST',
        body: JSON.stringify(applicationName),
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then((r) => r.json())
      .then((response) => {
        const Recordsdf = response.searchresult;
        const valuelists = response.valuelist;

        // Remove the loading indicator from the `messages` array
          const loadingIndex = this.messages.findIndex((msg) => msg.message === 'Loading....');
          if (loadingIndex !== -1) {
            this.messages.splice(loadingIndex, 1);
          }
        let html = `
  <style>
    .input-row {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
    }

    .input-row label {
      margin-right: 10px;
    }
  </style>
`;

for (const record of Recordsdf) {
  if (record.type === '1') {
    html += `<div class="input-row">
               <label for="${record.name}">${record.name}:</label>
               <input type="text" name="${record.name}" id="${record.name}">
             </div>`;
  } else if (record.type === '2') {
    html += `<div class="input-row">
               <label for="${record.name}">${record.name}:</label>
               <input type="number" name="${record.name}" id="${record.name}">
             </div>`;
  } else if (record.type === '3') {
    html += `<div class="input-row">
               <label for="${record.name}">${record.name}:</label>
               <input type="date" name="${record.name}" id="${record.name}">
             </div>`;
  } else if (record.type === '4') {
    for (const val of valuelists) {
      if (record.name === val.name) {
        html += `<div class="input-row">
                   <label for="${val.name}">${val.name}:</label>
                   <select id="${val.name}" name="${val.name}">
                     <option value=""></option>`;
        for (const vl of val.list) {
          html += `<option value="${vl}">${vl}</option>`;
        }
        html += `</select>
                 </div>`;
      }
    }
  }
}

        const msg11 = { name: 'Sanjeev', message: html };
        this.messages.push(msg11);
        this.updateChatText(chatbox);

        // Capture input values and save them in variables
        const inputElements = chatbox.querySelectorAll('input, select');
        const formData = {};
        inputElements.forEach((input) => {
          formData[input.name] = input.value;
        });

        // Add a save button
        html += `<button id="saveButton">Save</button>`;
        msg11.message = html;
        this.updateChatText(chatbox);

        // Handle save button click event
        const saveButton = chatbox.querySelector('#saveButton');
        saveButton.addEventListener('click', () => {
          // Capture input values and save them in variables
          const inputElements = chatbox.querySelectorAll('input, select');
          const formData = {};
          inputElements.forEach((input) => {
            formData[input.name] = input.value;
          });

          const htmlIndex = this.messages.findIndex((msg) => msg.message === html);
      if (htmlIndex !== -1) {
        this.messages.splice(htmlIndex, 1);
      }

          // Show loading message
  const loadingMessage = { name: 'Sanjeev', message: 'Loading...' };
  this.messages.push(loadingMessage);
  this.updateChatText(chatbox);

          // Send formData to the Python code
          fetch('/submitForm', {
            method: 'POST',
            body: JSON.stringify({ 'formData': formData, 'ApplicationName': this.ApplicationName }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then((r) => r.json())
          .then((response) => {
            // Handle the response from the Python code
            console.log(response);
            // Remove the loading message from the messages array
      const loadingIndex = this.messages.findIndex((msg) => msg.message === 'Loading...');
      if (loadingIndex !== -1) {
        this.messages.splice(loadingIndex, 1);
      }

            // Example: Add a message with the Python code's response to the chatbox
            const message = { name: 'Sanjeev', message: response.message };
            this.messages.push(message);
            this.updateChatText(chatbox);
            this.state = false;
      this.chatst = null;

    // Start the chat loop again
    this.startChatLoop();

          })
          .catch((error) => {
            console.error('Error:', error);
          });
        });
      })
      .catch((error) => {
        console.error('Error:', error);
      });

      this.state = false;
      this.chatst = null;
      textField.value = '';
      break;

    default:
      this.chatst = null;
      this.state = false;
      const msg13 = { name: 'User', message: text };
      this.messages.push(msg13);
      this.updateChatText(chatbox);
      break;
  }
}

    //Chatgpt Section
    else {
      const msg13 = { name: 'User', message: text };
      this.messages.push(msg13);
      this.updateChatText(chatbox);
      // Show loading message
  const loadingMessage = { name: 'Sanjeev', message: 'Loading...' };
  this.messages.push(loadingMessage);
  this.updateChatText(chatbox);
      fetch('/predict', {
        method: 'POST',
        body: JSON.stringify({ message: text }),
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then((r) => r.json())
        .then((r) => {
        // Remove the loading message from the messages array
      const loadingIndex = this.messages.findIndex((msg) => msg.message === 'Loading...');
      if (loadingIndex !== -1) {
        this.messages.splice(loadingIndex, 1);
      }
          const msg14 = { name: 'Sanjeev', message: r.answer };
          this.messages.push(msg14);
          this.updateChatText(chatbox);
          textField.value = '';
      })
        .catch((error) => {
          console.error('Error:', error);
          this.updateChatText(chatbox);
          textField.value = '';
        });
    }
    // Start the chat loop again
    this.startChatLoop();

  }




//Updatechatboxfunction
  updateChatText(chatbox) {
    let html = '';
    this.messages
      .slice()
      .reverse()
      .forEach(function (item, index) {
        if (item.name === 'Sanjeev') {
          html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
        } else {
          html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
        }
      });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;

    const textField = chatbox.querySelector('input');
    textField.value = '';
  }
}

const chatbox = new Chatbox();
chatbox.display();



/* fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        body: JSON.stringify(),
        mode: 'cors',
        headers: {
        'Content-Type': 'application/json'
        }
        })
        .then((r) => r.json())
        .then((response) => {
    const Applidetails = response.Applidetails;
    const msg14 = { name: 'Sanjeev', message: Applidetails };
    this.messages.push(msg14);
    this.updateChatText(chatbox);
    textField.value = '';
  })
        .catch((error) => {
        console.error('Error:', error);
        this.updateChatText(chatbox);
        textField.value = '';
        });*/