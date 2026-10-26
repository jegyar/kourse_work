/**
 * AutoParts Store - Main Core Module (Technical Industrial Aesthetics)
 * Light theme only. Handles authentication, toast stack, and live cart counter.
 */

const API_BASE = '';

// ===== Authentication Helpers =====
function getToken() {
    return localStorage.getItem('access_token');
}

function setToken(token) {
    localStorage.setItem('access_token', token);
}

function removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_role');
}

function getUserRole() {
    return localStorage.getItem('user_role');
}

function parseJwt(token) {
    try {
        const payload = token.split('.')[1];
        return JSON.parse(atob(payload));
    } catch (e) {
        return null;
    }
}

/**
 * Make an authenticated API request with auto 401 handling.
 */
async function apiRequest(url, options = {}) {
    const token = getToken();
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${API_BASE}${url}`, { ...options, headers });
        if (response.status === 401) {
            removeToken();
            showNotification('Сессия завершена. Требуется повторный вход.', 'warning');
            setTimeout(() => {
                window.location.href = '/login';
            }, 1000);
            return null;
        }
        return response;
    } catch (err) {
        console.error('API request error:', err);
        throw err;
    }
}

// ===== Clean Engineering Toast Notification =====
function showNotification(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none';
        document.body.appendChild(container);
    }

    const typeConfig = {
        success: {
            bg: 'bg-white border-emerald-500 text-slate-800',
            icon: `<svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>`
        },
        error: {
            bg: 'bg-white border-rose-500 text-slate-800',
            icon: `<svg class="w-4 h-4 text-rose-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>`
        },
        warning: {
            bg: 'bg-white border-amber-500 text-slate-800',
            icon: `<svg class="w-4 h-4 text-amber-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
        },
        info: {
            bg: 'bg-white border-slate-500 text-slate-800',
            icon: `<svg class="w-4 h-4 text-slate-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
        }
    };

    const cfg = typeConfig[type] || typeConfig.info;

    const toast = document.createElement('div');
    toast.className = `${cfg.bg} border-l-4 border-y border-r border-slate-200 px-3.5 py-2.5 rounded shadow-md flex items-center justify-between gap-3 pointer-events-auto text-xs font-semibold transition-all duration-200`;
    toast.setAttribute('role', 'alert');

    toast.innerHTML = `
        <div class="flex items-center gap-2.5 overflow-hidden">
            ${cfg.icon}
            <span class="truncate">${message}</span>
        </div>
        <button type="button" class="text-slate-400 hover:text-slate-700 p-0.5" onclick="this.closest('[role=alert]').remove()" aria-label="Закрыть">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(6px)';
            setTimeout(() => toast.remove(), 200);
        }
    }, 3000);
}

// ===== Live Cart Badge Counter =====
async function updateCartBadge() {
    const badges = document.querySelectorAll('.cart-badge');
    if (!badges.length) return;

    const token = getToken();
    if (!token) {
        badges.forEach(b => {
            b.classList.add('hidden');
            b.textContent = '0';
        });
        return;
    }

    try {
        const resp = await apiRequest('/cart/');
        if (resp && resp.ok) {
            const data = await resp.json();
            const count = data.items ? data.items.reduce((sum, item) => sum + item.quantity, 0) : 0;
            badges.forEach(b => {
                if (count > 0) {
                    b.classList.remove('hidden');
                    b.textContent = count;
                } else {
                    b.classList.add('hidden');
                    b.textContent = '0';
                }
            });
        }
    } catch (e) {}
}

// ===== Header Auth State UI =====
function updateAuthUI() {
    const authContainer = document.getElementById('auth-section');
    if (!authContainer) return;

    const token = getToken();
    let isAuth = false;
    let isAdmin = false;
    let email = '';

    if (token) {
        const payload = parseJwt(token);
        if (payload) {
            isAuth = true;
            isAdmin = payload.role_id === 1;
            email = payload.sub || 'Пользователь';
            localStorage.setItem('user_role', isAdmin ? 'admin' : 'client');
        }
    }

    if (isAuth) {
        authContainer.innerHTML = `
            <div class="flex items-center gap-3">
                ${isAdmin ? `
                    <a href="/admin" class="px-2.5 py-1 text-xs font-semibold rounded bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100 transition-colors">
                        Администрирование
                    </a>
                ` : ''}
                <div class="flex items-center gap-2 pl-2 border-l border-slate-200">
                    <span class="text-xs text-slate-600 font-medium truncate max-w-[150px]">${email}</span>
                    <button onclick="logout()" class="text-xs font-semibold text-rose-600 hover:text-rose-700 ml-1">Выйти</button>
                </div>
            </div>
        `;
    } else {
        authContainer.innerHTML = `
            <div class="flex items-center gap-2">
                <a href="/login" class="px-3 py-1.5 text-xs font-semibold text-slate-700 hover:text-slate-900 border border-slate-300 rounded hover:bg-slate-50 transition-colors">Вход</a>
                <a href="/register" class="px-3 py-1.5 text-xs font-semibold text-white bg-slate-800 hover:bg-slate-900 rounded transition-colors">Регистрация</a>
            </div>
        `;
    }
}

function logout() {
    removeToken();
    showNotification('Вы вышли из учетной записи', 'info');
    setTimeout(() => {
        window.location.href = '/';
    }, 500);
}

// ===== Mobile Menu Toggle =====
function toggleMobileMenu() {
    const nav = document.getElementById('mobile-nav');
    if (nav) nav.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    updateCartBadge();
});
