/* SmartWash Pro - Main JavaScript
   Owner: Suresh Gopi
*/

// ============ DARK MODE ============
const darkToggle = document.getElementById('darkModeToggle');
const html = document.documentElement;

function initDarkMode() {
    const saved = localStorage.getItem('swp-theme') || 'light';
    html.setAttribute('data-theme', saved);
    updateDarkIcon(saved);
}

function updateDarkIcon(theme) {
    if (!darkToggle) return;
    const icon = darkToggle.querySelector('i');
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

darkToggle?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('swp-theme', next);
    updateDarkIcon(next);
});

initDarkMode();

// ============ SIDEBAR TOGGLE ============
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');

sidebarToggle?.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});

mobileMenuBtn?.addEventListener('click', () => {
    sidebar.classList.toggle('mobile-open');
    // Add overlay
    const overlay = document.getElementById('mobileOverlay') || createMobileOverlay();
    overlay.style.display = sidebar.classList.contains('mobile-open') ? 'block' : 'none';
});

function createMobileOverlay() {
    const ov = document.createElement('div');
    ov.id = 'mobileOverlay';
    ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:99;display:none;';
    ov.addEventListener('click', () => {
        sidebar.classList.remove('mobile-open');
        ov.style.display = 'none';
    });
    document.body.appendChild(ov);
    return ov;
}

// ============ BARCODE SCANNER MODAL ============
let html5QrScanner = null;

function openScanModal() {
    const modal = document.getElementById('scanModal');
    modal.style.display = 'flex';
    
    // Start camera
    setTimeout(() => {
        if (typeof Html5Qrcode !== 'undefined') {
            try {
                html5QrScanner = new Html5Qrcode("reader");
                html5QrScanner.start(
                    { facingMode: "environment" },
                    { fps: 10, qrbox: { width: 250, height: 150 } },
                    (decodedText) => {
                        html5QrScanner.stop();
                        document.getElementById('manualBarcode').value = decodedText;
                        fetchByBarcode(decodedText);
                    }
                ).catch(err => {
                    console.log('Camera not available:', err);
                    document.getElementById('scanArea').innerHTML = `
                        <div style="text-align:center;padding:30px;color:#64748b;">
                            <i class="fas fa-video-slash" style="font-size:40px;margin-bottom:10px;display:block;"></i>
                            <p>Camera not available. Use manual entry below.</p>
                        </div>`;
                });
            } catch(e) {
                console.log('QR error:', e);
            }
        }
    }, 100);
}

function closeScanModal() {
    if (html5QrScanner) {
        html5QrScanner.stop().catch(() => {});
        html5QrScanner = null;
    }
    document.getElementById('scanModal').style.display = 'none';
    document.getElementById('scanResult').style.display = 'none';
    document.getElementById('manualBarcode').value = '';
}

function fetchByBarcode(barcode) {
    const val = barcode || document.getElementById('manualBarcode').value.trim();
    if (!val) { showToast('Please enter a barcode or order ID', 'warning'); return; }
    
    const resultDiv = document.getElementById('scanResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '<div style="text-align:center;"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    
    fetch('/api/scan-barcode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ barcode: val })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success && data.order) {
            const o = data.order;
            resultDiv.innerHTML = `
                <div style="padding:4px 0;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                        <strong style="color:#2563EB;font-size:16px;">${o.order_id}</strong>
                        <span class="status-badge status-${o.status}">${o.status}</span>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px;">
                        <div><span style="color:#64748b;">Customer:</span><br><strong>${o.customer_name}</strong></div>
                        <div><span style="color:#64748b;">Phone:</span><br><strong>${o.phone}</strong></div>
                        <div><span style="color:#64748b;">Service:</span><br><strong>${o.service_type?.replace(/_/g,' ')}</strong></div>
                        <div><span style="color:#64748b;">Amount:</span><br><strong>₹${parseFloat(o.final_amount).toFixed(2)}</strong></div>
                    </div>
                    <a href="/orders/view/${o.order_id}" class="btn btn-primary" style="width:100%;margin-top:14px;justify-content:center;">
                        <i class="fas fa-eye"></i> View Full Order
                    </a>
                </div>`;
        } else {
            resultDiv.innerHTML = `<div style="text-align:center;color:#EF4444;"><i class="fas fa-exclamation-circle"></i> ${data.message || 'Order not found'}</div>`;
        }
    })
    .catch(() => {
        resultDiv.innerHTML = '<div style="text-align:center;color:#EF4444;"><i class="fas fa-times-circle"></i> Error searching. Please try again.</div>';
    });
}

// Close modal on overlay click
document.getElementById('scanModal')?.addEventListener('click', function(e) {
    if (e.target === this) closeScanModal();
});

// ============ GLOBAL SEARCH ============
const globalSearch = document.getElementById('globalSearch');
let searchTimeout;

globalSearch?.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        const val = e.target.value.trim();
        if (val.length >= 3) {
            window.location.href = `/orders?search=${encodeURIComponent(val)}`;
        }
    }, 600);
});

// ============ TOAST NOTIFICATIONS ============
function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const icons = { success: 'check-circle', danger: 'exclamation-circle', warning: 'exclamation-triangle', info: 'info-circle' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-${icons[type] || 'info-circle'}" style="color:var(--${type === 'info' ? 'info' : type === 'warning' ? 'warning' : type === 'danger' ? 'danger' : 'success'})"></i> ${message}`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// ============ AUTO-DISMISS ALERTS ============
setTimeout(() => {
    document.querySelectorAll('.alert').forEach(alert => {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

// ============ KEYBOARD SHORTCUTS ============
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeScanModal();
    }
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        globalSearch?.focus();
    }
    if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/orders/new';
    }
});

// ============ ANIMATE STAT VALUES ============
function animateValue(el, start, end, duration) {
    let startTime = null;
    const step = (currentTime) => {
        if (!startTime) startTime = currentTime;
        const progress = Math.min((currentTime - startTime) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        el.textContent = el.dataset.prefix ? el.dataset.prefix + current.toLocaleString('en-IN') : current.toLocaleString('en-IN');
        if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
}

document.querySelectorAll('.stat-value').forEach(el => {
    const text = el.textContent;
    const num = parseFloat(text.replace(/[₹,]/g, ''));
    if (!isNaN(num) && num > 0) {
        if (text.includes('₹')) el.dataset.prefix = '₹';
        animateValue(el, 0, num, 1000);
    }
});

console.log('%c🧺 SmartWash Pro', 'color:#2563EB;font-size:20px;font-weight:800;');
console.log('%cOwner: Suresh Gopi | Professional Laundry Management System', 'color:#10B981;font-size:12px;');
