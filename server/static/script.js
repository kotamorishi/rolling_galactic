// script.js
const galacticUUID = "galacticUUID";
const latestMessage = "latestMessage";
const errorTitle = "Error";
// declare global variables(pretty bad practice, but it's ok for this small project. pull request is welcome)
let timer1, timer2;

// Save data to localStorage
function saveUUIDToLocalStorage(value) {
  localStorage.setItem(galacticUUID, value);
}

// Retrieve data from localStorage
function getUUIDFromLocalStorage() {
  try {
    const savedUUID = localStorage.getItem(galacticUUID);
    if (savedUUID !== null) {
      return savedUUID;
    }
  } catch (error) {}

  // grenarate new UUID
  UUID = uuidv4();
  saveUUIDToLocalStorage(UUID);
  return UUID;
}

function getLatestMessageFromLocalStorage() {
  try {
    const lm = localStorage.getItem(latestMessage);
    return lm;
  } catch (error) {
    return "";
  }
}

function saveLatestMessageToLocalStorage(value) {
  try {
    const lm = localStorage.setItem(latestMessage, value);
  } catch (error) {}
}

function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

// run this function when page loads
window.onload = function () {
  let form = document.getElementById("messenger-form");
  document.getElementById("update").addEventListener("click", function (event) {
    event.preventDefault();
    console.log("update button clicked");
    saveLatestMessageToLocalStorage(document.getElementById("message").value);
    const data = new FormData();
    data.append("uuid", document.getElementById("uuid").value);
    data.append("message", document.getElementById("message").value);
    data.append("colorpicker", document.getElementById("colorpicker").value);
    data.append("colorpickerBg", document.getElementById("colorpicker-bg").value);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (response.status === "success") {
          setButtonMessage("Updating...");
        }
      } else {
        setButtonMessage(errorTitle);
      }
    };
    try {
      xhr.send(data);
    } catch (error) {
      setButtonMessage(errorTitle);
    }
  });

  let UUID = getUUIDFromLocalStorage();
  let latestMessage = getLatestMessageFromLocalStorage();
  document.getElementById("uuid").value = UUID;
  document.getElementById("message").value = latestMessage;
};

// change button text to "Updating..." for 5 second
function setButtonMessage(message) {
  // clear previous timer
  clearTimeout(timer1);
  const button = document.getElementById("buttonText");
  const icon = document.getElementById("icon");
  if (message !== errorTitle) {
    icon.classList.remove(...icon.classList);
    icon.classList.add("fas", "fa-sync-alt", "fa-spin");
    button.classList.add("green");
  }
  else{
    icon.classList.remove(...icon.classList);
    icon.classList.add("fas", "fa-exclamation-triangle", "fa-beat-fade");
    // button background color changed to red
    button.classList.add("red");
  }
  button.innerHTML = message;
  timer1 = setTimeout(() => {
    button.innerHTML = "Submit";
    icon.classList.remove(...icon.classList);
    icon.classList.add("fas", "fa-regular", "fa-paper-plane");
  }, 5000);
}

const colorInput = document.getElementById("colorpicker");
const colorCircles = document.getElementById("color-circles");

const colorInputBg = document.getElementById("colorpicker-bg");
const colorCirclesBg = document.getElementById("color-circles-bg");

// Define an array of color values
const colors = ["#FF0000", "#EB5353","#FF7B54", "#F9D923", "#36AE7C", "#187498", "#FF00FF", "#0000FF", "#FFFFFF", "#000000"];

// Create a color circle for each color value
colors.forEach(color => {
  // for text circles
  const circle = document.createElement("div");
  circle.classList.add("color-circle");
  circle.style.backgroundColor = color;
  circle.addEventListener("click", () => {
    colorInput.value = color;
    colorInput.style.backgroundColor = color;
  });
  colorCircles.appendChild(circle);

  // for background circles
  const circleBg = document.createElement("div");
  circleBg.classList.add("color-circle");
  circleBg.style.backgroundColor = color;
  circleBg.addEventListener("click", () => {
    colorInputBg.value = color;
    colorInputBg.style.backgroundColor = color;
  });
  colorCirclesBg.appendChild(circleBg);
});