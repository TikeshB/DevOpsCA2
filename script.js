const form = document.getElementById("feedbackForm");
const toast = document.getElementById("toast");
let suppressResetToast = false;
const fields = {
  name: document.getElementById("name"),
  email: document.getElementById("email"),
  phone: document.getElementById("phone"),
  department: document.getElementById("department"),
  comments: document.getElementById("comments"),
};

const errors = {
  name: "",
  email: "",
  phone: "",
  department: "",
  gender: "",
  comments: "",
};

const showError = (field, message) => {
  const target = document.querySelector(`.field__error[data-for="${field}"]`);
  if (!target) return;
  target.textContent = message;
};

const clearErrors = () => {
  Object.keys(errors).forEach((key) => (errors[key] = ""));
  document.querySelectorAll(".field__error").forEach((el) => (el.textContent = ""));
};

const validate = () => {
  clearErrors();

  const name = fields.name.value.trim();
  const email = fields.email.value.trim();
  const phone = fields.phone.value.trim();
  const department = fields.department.value;
  const gender = form.querySelector("input[name='gender']:checked");
  const comments = fields.comments.value.trim();

  if (!name) {
    errors.name = "Student name is required.";
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) {
    errors.email = "Email is required.";
  } else if (!emailPattern.test(email)) {
    errors.email = "Please enter a valid email address.";
  }

  const phoneDigits = phone.replace(/[^0-9]/g, "");
  if (!phone) {
    errors.phone = "Mobile number is required.";
  } else if (phoneDigits.length !== 10) {
    errors.phone = "Mobile number must be 10 digits.";
  }

  if (!department) {
    errors.department = "Please select a department.";
  }

  if (!gender) {
    errors.gender = "Please choose a gender.";
  }

  const words = comments.split(/\s+/).filter(Boolean);
  if (!comments) {
    errors.comments = "Feedback comments are required.";
  } else if (words.length < 10) {
    errors.comments = "Please enter at least 10 words.";
  }

  Object.entries(errors).forEach(([key, message]) => {
    if (message) showError(key, message);
  });

  return !Object.values(errors).some(Boolean);
};

const showToast = (message, type = "success") => {
  toast.textContent = message;
  toast.style.borderColor = type === "success" ? "rgba(46, 231, 183, 0.7)" : "rgba(255, 104, 113, 0.7)";
  toast.style.background = type === "success" ? "rgba(10, 25, 30, 0.95)" : "rgba(30, 10, 10, 0.95)";
  toast.classList.add("show");

  window.clearTimeout(toast.dataset.timeout);
  toast.dataset.timeout = window.setTimeout(() => {
    toast.classList.remove("show");
  }, 3200);
};

const collectData = () => {
  const gender = form.querySelector("input[name='gender']:checked")?.value ?? null;
  return {
    name: fields.name.value.trim(),
    email: fields.email.value.trim(),
    phone: fields.phone.value.trim(),
    department: fields.department.value,
    gender,
    comments: fields.comments.value.trim(),
  };
};

form.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!validate()) {
    showToast("Please fix errors before submitting.", "error");
    return;
  }

  const data = collectData();
  console.log("Submitted payload:", data);

  showToast("Feedback submitted successfully!", "success");

  suppressResetToast = true;
  form.reset();
  // Allow reset event to finish and then re-enable toast
  window.setTimeout(() => {
    suppressResetToast = false;
  }, 0);
});

form.addEventListener("reset", () => {
  if (suppressResetToast) return;

  window.setTimeout(() => {
    clearErrors();
    showToast("Form reset successfully.", "success");
  }, 10);
});

// Accessibility helpers: focus first invalid field on submit
form.addEventListener("invalid", (event) => {
  event.preventDefault();
  const field = event.target;
  field.focus();
}, true);
