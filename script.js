/* =====================================================
   FobFather — script.js
   Vanilla JS frontend logic
   Handles form validation, submission, spinner, and response
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('submitBtn');
  const spinner = document.getElementById('formSpinner');
  const responseDiv = document.getElementById('formResponse');

  // Utility: show spinner
  function showSpinner() {
    spinner.style.display = 'inline-block';
  }

  // Utility: hide spinner
  function hideSpinner() {
    spinner.style.display = 'none';
  }

  // Utility: show response message
  function showResponse(message, isSuccess = true) {
    responseDiv.textContent = message;
    responseDiv.style.color = isSuccess ? 'green' : 'red';
  }

  // Simple phone validation
  function validatePhone(phone) {
    const phonePattern = /^\d{10}$/;
    return phonePattern.test(phone.replace(/\D/g, ''));
  }

  // Form validation
  function validateForm() {
    let valid = true;
    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    const consent = form.consent.checked;

    if (!phone || !validatePhone(phone)) {
      valid = false;
      showResponse('Please enter a valid 10-digit phone number.', false);
    } else if (!consent) {
      valid = false;
      showResponse('You must agree to be contacted.', false);
    } else {
      showResponse('', true);
    }
    return valid;
  }

  // Serialize form data into JSON
  function getFormData() {
    return {
      name: form.name.value.trim(),
      phone: form.phone.value.trim(),
      email: form.email.value.trim(),
      message: form.message.value.trim(),
      preferred: form.preferred.value.trim()
    };
  }

  // Handle form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    submitBtn.disabled = true;
    showSpinner();
    showResponse('');

    const payload = getFormData();

    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.ok) {
        showResponse('Thanks! We received your message. We’ll contact you soon.', true);
        form.reset();
      } else {
        let msg = data.message || 'Error submitting form. Please try again later.';
        showResponse(msg, false);
      }

    } catch (err) {
      console.error('Form submission error:', err);
      showResponse('Backend unreachable. Please try again later.', false);
    } finally {
      hideSpinner();
      submitBtn.disabled = false;
    }
  });

  // Hero CTA button scroll smooth
  const ctaBtns = document.querySelectorAll('#ctaPrimary, #headerMessageBtn');
  ctaBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      document.getElementById('contact').scrollIntoView({ behavior: 'smooth' });
    });
  });

});
