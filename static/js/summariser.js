let selectedMode = "summarise";
let selectedModel = "";

// MODE SELECTOR BUTTON
const settingButtonOne = document.querySelector(".model-setting-one");
const settingButtonTwo = document.querySelector(".model-setting-two");
const settingButtonThree = document.querySelector(".model-setting-three");

const resetActive = function () {
  settingButtonOne.classList.remove("active");
  settingButtonTwo.classList.remove("active");
  settingButtonThree.classList.remove("active");
};

settingButtonOne.addEventListener("click", function () {
  resetActive();
  settingButtonOne.classList.add("active");
  selectedMode = "summarise";
});

settingButtonTwo.addEventListener("click", function () {
  resetActive();
  settingButtonTwo.classList.add("active");
  selectedMode = "keyinfo";
});

settingButtonThree.addEventListener("click", function () {
  resetActive();
  settingButtonThree.classList.add("active");
  selectedMode = "entityrecognition";
});

// CHANGE MODEL DROPDOWN MENU BUTTON
const changeModelBtn = document.querySelector(".dropbtn");
const dropdownContent = document.querySelector(".dropdown-content");
const dropdownOptionOne = document.querySelector(".dropdown-option-one");
const dropdownOptionTwo = document.querySelector(".dropdown-option-two");
const dropdownOptionThree = document.querySelector(".dropdown-option-three");
const dropdownOptions = [
  dropdownOptionOne,
  dropdownOptionTwo,
  dropdownOptionThree,
];

changeModelBtn.addEventListener("click", function (e) {
  dropdownContent.style.display = "block";
  changeModelBtn.style.backgroundColor = "#fdc148";
  changeModelBtn.style.color = "#3f2e0c";
});

document.addEventListener("click", function (e) {
  if (
    !e.target.classList.contains("dropbtn") &&
    !e.target.classList.contains("dropdown-option")
  ) {
    dropdownContent.style.display = "none";

    if (changeModelBtn.textContent === "Select Model") {
      changeModelBtn.style.backgroundColor = "rgba(215, 211, 244, 0.24)";
      changeModelBtn.style.color = "#ffffff";
    }
  }
});

dropdownOptions.forEach((option) => {
  option.addEventListener("click", function () {
    dropdownContent.style.display = "none";
    changeModelBtn.style.backgroundColor = "#fdc148";
    changeModelBtn.style.color = "#ffffff";
    changeModelBtn.style.color = "#3f2e0c";
  });
});

dropdownOptionOne.addEventListener("click", function () {
  changeModelBtn.textContent = dropdownOptionOne.textContent;
  selectedModel = "gpt-4o-mini";
});

dropdownOptionTwo.addEventListener("click", function () {
  changeModelBtn.textContent = dropdownOptionTwo.textContent;
  selectedModel = "gpt4-o";
});

dropdownOptionThree.addEventListener("click", function () {
  changeModelBtn.textContent = dropdownOptionThree.textContent;
  selectedModel = "gpt4";
});

// HANDLING GENERATE BUTTON (AND ACTUAL API CALLS)
const generateButton = document.querySelector(".generate-btn");
const modal = document.querySelector(".modal");
const modalCloseButton = document.querySelector(".modal-close-btn");
const modalConfirmButton = document.querySelector(".modal-confirm-btn");
const userInput = document.querySelector(".input");
const outputSection = document.querySelector(".output");

modalCloseButton.addEventListener("click", function (e) {
  modal.style.display = "none";
});

modalConfirmButton.addEventListener("click", function (e) {
  modal.style.display = "none";
});

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

generateButton.addEventListener("click", async function (e) {
  e.preventDefault();

  if (selectedModel === "") {
    modal.style.display = "block";
  } else {
    try {
      let response = await fetch("/summarise_text", {
        method: "POST",
        headers: { "Content-Type": "application/JSON" },
        body: JSON.stringify({
          message: userInput.value,
          mode: selectedMode,
          model: selectedModel,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ERROR: ${response.status}`);
      }

      const reader = response.body.getReader();
      let output = "";

      let counter = 1;
      while (true) {
        const { done, value } = await reader.read();
        output += new TextDecoder().decode(value);
        outputSection.innerHTML = marked.parse(output);

        if (done) {
          return;
        }
      }
    } catch (error) {
      console.log("ERROR: " + error);
    }
  }
});
