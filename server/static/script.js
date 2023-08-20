// script.js
const galacticUUID = "galacticUUID";
const latestMessage = "latestMessage";

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
  document.getElementById("update").addEventListener("click", function(event) {
    event.preventDefault();
    console.log("update button clicked");
    saveLatestMessageToLocalStorage(document.getElementById("message").value);
    const data = new FormData();
    data.append("uuid", document.getElementById("uuid").value);
    data.append("message", document.getElementById("message").value);

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
      }
      else{
        console.log("Error:", response);

      }
    };
    xhr.send(data);
  });

  let UUID = getUUIDFromLocalStorage();
  let latestMessage = getLatestMessageFromLocalStorage();
  document.getElementById("uuid").value = UUID;
  document.getElementById("message").value = latestMessage;
};



const button = document.querySelector("button"),
      toast = document.querySelector(".toast")
      closeIcon = document.querySelector(".close"),
      progress = document.querySelector(".progress");

      let timer1, timer2;

      button.addEventListener("click", () => {
        toast.classList.add("active");
        progress.classList.add("active");

        timer1 = setTimeout(() => {
            toast.classList.remove("active");
        }, 5000); //1s = 1000 milliseconds

        timer2 = setTimeout(() => {
          progress.classList.remove("active");
        }, 5300);
      });
      
      closeIcon.addEventListener("click", () => {
        toast.classList.remove("active");
        
        setTimeout(() => {
          progress.classList.remove("active");
        }, 300);

        clearTimeout(timer1);
        clearTimeout(timer2);
      });

