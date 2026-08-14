// Theme Toggle Logic
function initTheme() {
    const savedTheme = localStorage.getItem('phishguard_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme);
}

function updateThemeIcons(theme) {
    const themeIcons = document.querySelectorAll('.theme-icon');
    themeIcons.forEach(icon => {
        icon.textContent = theme === 'light' ? '☀️' : '🌙';
    });
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('phishguard_theme', newTheme);
    updateThemeIcons(newTheme);
}

// Make functions globally accessible for inline HTML onclick attributes
window.toggleTheme = toggleTheme;
window.initTheme = initTheme;

// Quick Test Sample Pill Selector
function setSample(url) {
    const input = document.getElementById('urlInput');
    const form = document.getElementById('scanForm');
    if (input) {
        input.value = url;
        toggleClearBtn();
        if (form) {
            const btnText = document.querySelector('#submitBtn .btn-text');
            const btnSpinner = document.querySelector('#submitBtn .btn-spinner');
            if (btnText && btnSpinner) {
                btnText.textContent = 'Scanning...';
                btnSpinner.classList.remove('hidden');
            }
            form.submit();
        }
    }
}

window.setSample = setSample;

// Clear Input Logic
function toggleClearBtn() {
    const urlInput = document.getElementById('urlInput');
    const clearBtn = document.getElementById('clearBtn');
    if (urlInput && clearBtn) {
        clearBtn.style.display = urlInput.value.length > 0 ? 'block' : 'none';
    }
}

function clearInput() {
    const urlInput = document.getElementById('urlInput');
    if (urlInput) {
        urlInput.value = '';
        toggleClearBtn();
        urlInput.focus();
    }
}

window.clearInput = clearInput;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    // Bind Theme Toggle buttons
    document.querySelectorAll('.theme-toggle-btn, #themeToggle').forEach(btn => {
        btn.onclick = toggleTheme;
    });

    const urlInput = document.getElementById('urlInput');
    if (urlInput) {
        urlInput.addEventListener('input', toggleClearBtn);
        toggleClearBtn();
    }

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
    }

    // Smooth Scroll for Navigation Anchor Links with Fixed Navbar Offset
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetElem = document.querySelector(targetId);
                if (targetElem) {
                    e.preventDefault();
                    const navHeight = 90;
                    const elementPosition = targetElem.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - navHeight;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});

// Immediate execution to set theme attribute right away
initTheme();
