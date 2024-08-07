// HANDLING PAGINATION DATA
let currentPage = 1;
let maxPages = 0;
let data = [];

const fetchPageData = async function () {
  try {
    let response = await fetch(`/get_past_generations/${currentPage}`, {
      method: "POST",
      headers: { "Content-Type": "application/JSON" },
      body: JSON.stringify({ page_number: currentPage }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ERROR: ${response.status}`);
    }

    data = await response.json();
    maxPages = data["max_pages"] + 1;
    data = data["data"];
  } catch (error) {
    console.log("ERROR: " + error);
  }
};

const dataContainer = document.querySelector(".data-container");

const updatePage = function () {
  dataContainer.innerHTML = "";
  data.forEach((value) => {
    dataContainer.innerHTML += `
    <div class="generation-container">
      <div class="generation-header">
        <p class="generation-header-date">${value.time_generated}</p>
        <p class="generation-header-heading">${value.aboutText}</p>
        <ion-icon class="arrow-icon" name="chevron-down-outline"></ion-icon>
      </div>
      <div class="generation-meta">
        <p class="meta-mode">Mode: ${value.mode}</p>
        <p class="meta-model">Model: ${value.model}</p>
        <p class="meta-timestamp">${value.time_generated}</p>
      </div>
      <div class="generation-main">
        <div class="generation-main-input">
          <p class="generation-main-input-title">Input Text</p>
          <p class="generation-main-input-text">${value.inputText}</p>
        </div>
        <div class="generation-main-output">
          <p class="generation-main-output-title">Output Text</p>
          <p class="generation-main-output-text">${marked.parse(
            value.outputText
          )}</p>
        </div>
      </div>
    </div>
    `;
  });
  document.getElementById(
    "current-page"
  ).textContent = `Page ${currentPage} of ${maxPages}`;
};

const nextBtn = document.querySelector(".next-btn");
const prevBtn = document.querySelector(".prev-btn");

nextBtn.addEventListener("click", async function () {
  if (currentPage < maxPages) {
    currentPage++;
    await fetchPageData();
    updatePage();
    updateButtonVisibility();
    addArrowEventListeners();
  }
});

prevBtn.addEventListener("click", async function () {
  if (currentPage > 1) {
    currentPage--;
    await fetchPageData();
    updatePage();
    updateButtonVisibility();
    addArrowEventListeners();
  }
});

function updateButtonVisibility() {
  nextBtn.style.visibility = currentPage === maxPages ? "hidden" : "visible";
  nextBtn.style.pointerEvents = currentPage === maxPages ? "none" : "auto";
  prevBtn.style.visibility = currentPage === 1 ? "hidden" : "visible";
  prevBtn.style.pointerEvents = currentPage === 1 ? "none" : "auto";
}

const addArrowEventListeners = function () {
  const arrows = document.querySelectorAll(".arrow-icon");
  const generationMain = document.querySelectorAll(".generation-main");

  arrows.forEach((arrow, index) => {
    generationMain[index].style.display = "none";

    arrow.addEventListener("click", function () {
      if (arrow.getAttribute("name") === "chevron-up-outline") {
        arrow.setAttribute("name", "chevron-down-outline");
        generationMain[index].style.display = "none";
      } else {
        arrow.setAttribute("name", "chevron-up-outline");
        generationMain[index].style.display = "flex";
      }
    });
  });
};

// Initial load
(async function () {
  await fetchPageData();
  updatePage();
  updateButtonVisibility();
  addArrowEventListeners();
})();
