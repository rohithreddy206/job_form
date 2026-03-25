/**
 * TalentBridge – Candidate Application Form · Frontend Logic
 * Handles: progress bar, drag-drop upload, inline validation, submit spinner, confetti
 */

'use strict';

/* ── Utilities ───────────────────────────────────────────── */
const $ = id => document.getElementById(id);
const show = el => el && (el.style.display = 'block');
const hide = el => el && (el.style.display = 'none');

function showError(id, msg) {
  const el = $(id);
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
}
function clearError(id) {
  const el = $(id);
  if (!el) return;
  el.textContent = '';
  el.classList.remove('show');
}

function isValidEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
function isValidPhone(v) { return /^\+?[\d\s\-().]{7,20}$/.test(v); }

/* ── Progress Bar ────────────────────────────────────────── */
const SECTIONS = ['section-personal', 'section-professional', 'section-compensation', 'section-additional', 'section-resume'];

function filledRatio(sectionId) {
  const sec = $(sectionId);
  if (!sec) return 0;
  const inputs = sec.querySelectorAll('input:not([type=file]), select, textarea');
  let filled = 0;
  inputs.forEach(el => { if (el.value && el.value.trim()) filled++; });
  const file = sec.querySelector('input[type=file]');
  if (file && file.files && file.files.length) filled++;
  return inputs.length ? filled / inputs.length : 0;
}

function updateProgress() {
  const total = SECTIONS.reduce((acc, id) => acc + filledRatio(id), 0);
  const pct = Math.round((total / SECTIONS.length) * 100);

  const bar   = $('progressBar');
  const label = $('progressLabel');
  if (bar)   bar.style.width = pct + '%';
  if (label) label.textContent = pct + '% Complete';

  // Step badges: activate them based on which sections have content
  const thresholds = [0, 25, 50, 75];
  thresholds.forEach((t, i) => {
    const badge = $('step' + (i + 1));
    if (!badge) return;
    if (pct >= t + 25) {
      badge.className = 'step-badge done';
      badge.innerHTML = '<i class="fa-solid fa-check text-[10px]"></i>';
    } else if (pct >= t) {
      badge.className = 'step-badge active';
      badge.textContent = i + 1;
    } else {
      badge.className = 'step-badge';
      badge.textContent = i + 1;
    }
  });
}

/* ── File Upload ─────────────────────────────────────────── */
function initFileUpload() {
  const zone    = $('dropZone');
  const input   = $('resume');
  const badge   = $('fileNameBadge');
  const nameEl  = $('fileNameText');
  if (!zone || !input) return;

  // Click to open picker (but not when clicking the hidden file input itself)
  zone.addEventListener('click', e => { if (e.target !== input) input.click(); });

  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      input.files = e.dataTransfer.files;
      handleFile();
    }
  });

  input.addEventListener('change', handleFile);

  function handleFile() {
    const file = input.files[0];
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'doc', 'docx'].includes(ext)) {
      showError('resumeError', 'Only PDF, DOC, or DOCX files are allowed.');
      input.value = '';
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      showError('resumeError', 'File size must be under 5 MB.');
      input.value = '';
      return;
    }
    clearError('resumeError');
    if (badge && nameEl) {
      nameEl.textContent = file.name;
      badge.classList.remove('hidden');
    }
    updateProgress();
  }
}

/* ── Live Inline Validation ──────────────────────────────── */
function attachValidation() {
  const rules = [
    { id: 'first_name',   err: 'firstNameError', check: v => v.trim().length >= 1, msg: 'First name is required.'         },
    { id: 'last_name',    err: 'lastNameError',  check: v => v.trim().length >= 1, msg: 'Last name is required.'          },
    { id: 'phone_number', err: 'phoneError',     check: isValidPhone,               msg: 'Enter a valid phone number.'     },
    { id: 'email',        err: 'emailError',     check: isValidEmail,               msg: 'Enter a valid email address.'   },
  ];

  rules.forEach(({ id, err, check, msg }) => {
    const el = $(id);
    if (!el) return;
    el.addEventListener('blur', () => {
      if (el.value && !check(el.value)) {
        showError(err, msg);
        el.classList.add('is-error');
      } else {
        clearError(err);
        el.classList.remove('is-error');
      }
    });
    el.addEventListener('input', () => {
      if (el.classList.contains('is-error') && check(el.value)) {
        clearError(err);
        el.classList.remove('is-error');
      }
      updateProgress();
    });
  });

  document.querySelectorAll('.field-input').forEach(el => {
    el.addEventListener('change', updateProgress);
  });
}

/* ── Form Submit ─────────────────────────────────────────── */
function initSubmit() {
  const form = $('applicationForm');
  if (!form) return;

  form.addEventListener('submit', e => {
    let valid = true;
    const firstName  = $('first_name');
    const lastName   = $('last_name');
    const phone      = $('phone_number');
    const email      = $('email');
    const resume     = $('resume');

    if (!firstName?.value.trim()) {
      showError('firstNameError', 'First name is required.'); firstName?.classList.add('is-error'); valid = false;
    }
    if (!lastName?.value.trim()) {
      showError('lastNameError', 'Last name is required.'); lastName?.classList.add('is-error'); valid = false;
    }
    if (!phone?.value || !isValidPhone(phone.value)) {
      showError('phoneError', 'A valid phone number is required.'); phone?.classList.add('is-error'); valid = false;
    }
    if (!email?.value || !isValidEmail(email.value)) {
      showError('emailError', 'A valid email is required.'); email?.classList.add('is-error'); valid = false;
    }
    if (!resume?.files?.length) {
      showError('resumeError', 'Please upload your resume.'); valid = false;
    }

    if (!valid) {
      e.preventDefault();
      const firstErr = document.querySelector('.field-error.show');
      if (firstErr) firstErr.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    // Show loading state
    const btn     = $('submitBtn');
    const btnText = $('btnText');
    const spinner = $('spinner');
    const btnIcon = $('btnIcon');
    if (btn)     btn.disabled = true;
    if (btnText) btnText.textContent = 'Submitting…';
    if (spinner) spinner.classList.add('show');
    if (btnIcon) btnIcon.style.display = 'none';
  });
}

/* ── Confetti (Success Page) ─────────────────────────────── */
function launchConfetti() {
  const colors = ['#4361ee', '#7b5ea7', '#10b981', '#f59e0b', '#ef4444'];
  for (let i = 0; i < 90; i++) {
    const el = document.createElement('div');
    el.className = 'confetti-particle';
    el.style.cssText = `
      left: ${Math.random() * 100}vw;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      width: ${6 + Math.random() * 8}px;
      height: ${6 + Math.random() * 8}px;
      animation-duration: ${1.8 + Math.random() * 2}s;
      animation-delay: ${Math.random() * 0.6}s;
      border-radius: ${Math.random() > 0.5 ? '50%' : '3px'};
    `;
    document.body.appendChild(el);
    el.addEventListener('animationend', () => el.remove());
  }
}

/* ── Init ────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initFileUpload();
  attachValidation();
  initSubmit();
  updateProgress();

  if ($('successCard')) {
    launchConfetti();
  }
});
