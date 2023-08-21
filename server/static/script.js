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

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (response.status === "success") {
          showPopup("Success", "Message updated.");
        }
      } else {
        showPopup(errorTitle, "Failed to update message.");
      }
    };
    try {
      xhr.send(data);
    } catch (error) {
      showPopup(errorTitle, "Failed to update message.");
    }
  });

  let UUID = getUUIDFromLocalStorage();
  let latestMessage = getLatestMessageFromLocalStorage();
  document.getElementById("uuid").value = UUID;
  document.getElementById("message").value = latestMessage;
};


function showPopup(title, message) {
  const toast = document.querySelector(".toast");
  const closeIcon = document.querySelector(".close");
  const progress = document.querySelector(".progress");

  document.getElementById("popup-title").innerHTML = title;
  document.getElementById("popup-message").innerHTML = message;

  // if the tile is errorTitle, then show the error icon
  const ic = document.getElementById("popup-icon");
  if (title === errorTitle) {
    ic.className = 'fas fa-solid fa-triangle-exclamation fa-bounce check';
    ic.style="background-color: #ff1605;";
  }
  else{
    ic.className = 'fas fa-solid fa-check check';
    ic.style="background-color: rgb(63, 128, 232);";
  }

  toast.classList.add("active");
  progress.classList.add("active");

  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000); //1s = 1000 milliseconds

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);
}

const button = document.querySelector("button"),
  toast = document.querySelector(".toast");
(closeIcon = document.querySelector(".close")),
  (progress = document.querySelector(".progress"));

closeIcon.addEventListener("click", () => {
  toast.classList.remove("active");

  setTimeout(() => {
    progress.classList.remove("active");
  }, 300);

  clearTimeout(timer1);
  clearTimeout(timer2);
});


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