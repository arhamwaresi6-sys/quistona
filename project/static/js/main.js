/* =========================================================
   QUESTONA - main.js
   Simple JavaScript, one small job per section.
   Used on every page.
   ========================================================= */

/* ---------- 1. Phone menu button ---------- */
var menuBtn = document.getElementById("menuBtn");
var navLinks = document.getElementById("navLinks");

if (menuBtn) {
  menuBtn.addEventListener("click", function () {
    navLinks.classList.toggle("open"); // add/remove the "open" class
  });
}

/* ---------- 2. Pop-ups (modals) ----------
   A button with  data-open="someId"  opens the modal with that id.
   A button with  data-close          closes the modal it is inside. */
var openButtons = document.querySelectorAll("[data-open]");

openButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    var modal = document.getElementById(button.dataset.open);
    modal.classList.add("open");
  });
});

var closeButtons = document.querySelectorAll("[data-close]");

closeButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    button.closest(".modal").classList.remove("open");
  });
});

// clicking the dark background also closes the modal
var allModals = document.querySelectorAll(".modal");

allModals.forEach(function (modal) {
  modal.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.classList.remove("open");
    }
  });
});

/* ---------- 3. Search box ----------
   <input data-search=".card">  hides every .card that
   does not contain the typed text. */
var searchBox = document.querySelector("[data-search]");

if (searchBox) {
  searchBox.addEventListener("input", function () {
    var text = searchBox.value.toLowerCase();
    var items = document.querySelectorAll(searchBox.dataset.search);
    var shown = 0;

    items.forEach(function (item) {
      if (item.textContent.toLowerCase().includes(text)) {
        item.style.display = "";
        shown++;
      } else {
        item.style.display = "none";
      }
    });

    // show the "nothing found" message if needed
    var empty = document.getElementById("emptyMessage");
    if (empty) {
      empty.style.display = shown === 0 ? "block" : "none";
    }
  });
}

/* ---------- 4. Delete confirmation ----------
   A button with  data-delete="Batch 2022"  asks before deleting.
   (Flask will do the real delete later.) */
var deleteButtons = document.querySelectorAll("[data-delete]");

deleteButtons.forEach(function (button) {
  button.addEventListener("click", function (event) {
    var name = button.dataset.delete;
    var sure = confirm("Delete " + name + "? This cannot be undone.");
    if (!sure) {
      event.preventDefault(); // stop the delete
    }
  });
});

/* ---------- 5. Show / hide password ---------- */
var toggles = document.querySelectorAll("[data-toggle-password]");

toggles.forEach(function (toggle) {
  toggle.addEventListener("click", function () {
    var input = document.getElementById(toggle.dataset.togglePassword);
    if (input.type === "password") {
      input.type = "text";
      toggle.textContent = "Hide";
    } else {
      input.type = "password";
      toggle.textContent = "Show";
    }
  });
});

/* ---------- 6. Question page: filter by exam type ----------
   Buttons with  data-filter="midterm"  show only matching posts. */
var filterButtons = document.querySelectorAll("[data-filter]");

filterButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    var type = button.dataset.filter;

    // highlight the active button
    filterButtons.forEach(function (b) {
      b.classList.remove("active");
    });
    button.classList.add("active");

    // show / hide posts
    var posts = document.querySelectorAll(".post");
    posts.forEach(function (post) {
      if (type === "all" || post.dataset.type === type) {
        post.style.display = "";
      } else {
        post.style.display = "none";
      }
    });
  });
});

/* ---------- 7. Full-screen image viewer (lightbox) ---------- */
var lightbox = document.getElementById("lightbox");
var lightboxImg = document.getElementById("lightboxImg");

if (lightbox) {
  document.querySelectorAll(".post-img").forEach(function (img) {
    img.addEventListener("click", function () {
      lightboxImg.src = img.src;
      lightbox.classList.add("open");
    });
  });

  lightbox.addEventListener("click", function () {
    lightbox.classList.remove("open");
  });
}
// for edit modal to show selected bacth card
document.querySelectorAll("[data-edit-modal]").forEach(function (button) {
  button.addEventListener("click", function () {
    var modal = document.getElementById(button.dataset.editModal);

    if (!modal) return;

    var form = modal.querySelector("form");
    var input = form.querySelector('input[name="name"]');

    if (!form || !input) return;

    // Fill in the selected item's existing name
    input.value = button.dataset.name;

    // Set the correct Flask update route
    form.action = button.dataset.action;

    // Open the modal
    modal.classList.add("open");
  });
});
var deleteButtons = document.querySelectorAll("[data-delete]");

deleteButtons.forEach(function (button) {
  button.addEventListener("submit", function (event) {
    var name = button.dataset.delete;

    var sure = confirm("Delete " + name + "'s account? This cannot be undone.");

    if (!sure) {
      event.preventDefault();
    }
  });
});
