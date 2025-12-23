document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-form");
  const list = document.getElementById("bbs-list");
  const errorsBox = document.getElementById("form-errors");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errorsBox.textContent = "";

    const formData = new FormData(form);

    const csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;

    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      },
      body: formData
    });

    const data = await response.json();

    if (data.ok) {
      list.insertAdjacentHTML("afterbegin", data.html);
      form.reset();
    } else {
      errorsBox.textContent = data.errors;
    }
  });
});