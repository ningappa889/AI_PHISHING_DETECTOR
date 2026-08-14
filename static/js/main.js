// Theme Toggle Logic
const themeToggleBtn = document.getElementById('themeToggle');
const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('.theme-icon') : null;

const savedTheme = localStorage.getItem('phishguard_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
if (themeIcon) {
    themeIcon.textContent = savedTheme === 'light' ? '☀️' : '🌙';
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('phishguard_theme', newTheme);
        if (themeIcon) {
            themeIcon.textContent = newTheme === 'light' ? '☀️' : '🌙';
        }
    });
}

// Sample Pill Selector
function setSample(url) {
    const input = document.getElementById('urlInput');
    if (input) {
        input.value = url;
        toggleClearBtn();
        input.focus();
    }
}

// Clear Input Logic
const urlInput = document.getElementById('urlInput');
const clearBtn = document.getElementById('clearBtn');

function toggleClearBtn() {
    if (urlInput && clearBtn) {
        clearBtn.style.display = urlInput.value.length > 0 ? 'block' : 'none';
    }
}

if (urlInput) {
    urlInput.addEventListener('input', toggleClearBtn);
    toggleClearBtn();
}

function clearInput() {
    if (urlInput) {
        urlInput.value = '';
        toggleClearBtn();
        urlInput.focus();
    }
}

// Form Loading State
const scanForm = document.getElementById('scanForm');
const submitBtn = document.getElementById('submitBtn');

if (scanForm && submitBtn) {
    scanForm.addEventListener('submit', () => {
        const btnText = submitBtn.querySelector('.btn-text');
        const btnSpinner = submitBtn.querySelector('.btn-spinner');
        if (btnText && btnSpinner) {
            btnText.textContent = 'Scanning...';
            btnSpinner.classList.remove('hidden');
            submitBtn.style.opacity = '0.85';
        }
    });
// Smooth Scroll for Navigation Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId && targetId !== '#') {
            const targetElem = document.querySelector(targetId);
            if (targetElem) {
                e.preventDefault();
                targetElem.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});
