/**
 * AutoParts Store - Cart Module (Technical Clean Layout)
 */

document.addEventListener('DOMContentLoaded', () => {
    loadCart();
});

async function loadCart() {
    const container = document.getElementById('cartItems');
    const token = getToken();

    if (!token) {
        if (container) {
            container.innerHTML = `
                <div class="p-8 text-center bg-white border border-slate-200 rounded space-y-3">
                    <p class="text-sm font-semibold text-slate-800">Авторизуйтесь для просмотра корзины</p>
                    <p class="text-xs text-slate-500">Войдите в учетную запись для управления списком выбранных запчастей.</p>
                    <div class="pt-1">
                        <a href="/login" class="px-4 py-2 bg-slate-900 text-white rounded text-xs font-semibold hover:bg-slate-800 inline-block">Войти</a>
                    </div>
                </div>
            `;
        }
        return;
    }

    try {
        const response = await apiRequest('/cart/');
        if (response && response.ok) {
            const data = await response.json();
            renderCart(data);
        }
    } catch (e) {
        console.error('Failed to load cart', e);
        if (container) {
            container.innerHTML = `
                <div class="p-4 text-center text-xs text-rose-600 bg-rose-50 border border-rose-200 rounded">
                    Ошибка загрузки позиций корзины. <button onclick="loadCart()" class="font-bold underline ml-1">Повторить</button>
                </div>
            `;
        }
    }
}

function renderCart(data) {
    const container = document.getElementById('cartItems');
    const totalEl = document.getElementById('cartTotal');
    const subtotalEl = document.getElementById('cartSubtotal');
    const checkoutBtn = document.getElementById('checkoutBtn');
    const headerCount = document.getElementById('cartCountHeader');

    if (!container) return;

    if (!data.items || data.items.length === 0) {
        container.innerHTML = `
            <div class="part-card py-12 px-4 text-center space-y-3">
                <div class="w-10 h-10 mx-auto text-slate-400">
                    <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                </div>
                <h3 class="font-bold text-slate-900 text-sm">В корзине пока нет запчастей</h3>
                <p class="text-xs text-slate-500 max-w-sm mx-auto">
                    Используйте каталог для поиска нужных деталей по артикулу или автомобилю.
                </p>
                <div class="pt-2">
                    <a href="/catalog" class="px-4 py-2 rounded bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs inline-block">
                        Перейти в каталог
                    </a>
                </div>
            </div>
        `;

        if (totalEl) totalEl.textContent = '0.00 BYN';
        if (subtotalEl) subtotalEl.textContent = '0.00 BYN';
        if (checkoutBtn) checkoutBtn.disabled = true;
        if (headerCount) headerCount.textContent = '0 позиций';

        if (typeof updateCartBadge === 'function') updateCartBadge();
        return;
    }

    const totalQty = data.items.reduce((sum, item) => sum + item.quantity, 0);
    if (headerCount) headerCount.textContent = `${totalQty} позиций`;

    let html = '<div class="space-y-2">';
    data.items.forEach(item => {
        const itemTotal = (item.price * item.quantity).toFixed(2);
        const [rub, kop] = itemTotal.split('.');
        const [unitRub, unitKop] = item.price.toFixed(2).split('.');

        let imageContent = '';
        if (item.image_url) {
            imageContent = `<img src="${item.image_url}" alt="${item.name}" class="w-full h-full object-contain p-1">`;
        } else {
            const svgIcon = typeof getPartIllustration === 'function' ? getPartIllustration(item.category) : '';
            imageContent = svgIcon ? `<div class="p-1 scale-75">${svgIcon}</div>` : `<span class="text-xs text-slate-400">OEM</span>`;
        }

        html += `
        <div class="part-card p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3" id="cart-item-${item.cart_id}">
            <div class="flex items-center gap-3 flex-1 min-w-0">
                <div class="w-14 h-14 rounded bg-slate-50 border border-slate-100 flex items-center justify-center flex-shrink-0 overflow-hidden">
                    ${imageContent}
                </div>
                <div class="min-w-0">
                    <h3 class="font-bold text-xs sm:text-sm text-slate-900 truncate" title="${item.name}">${item.name}</h3>
                    <div class="text-[11px] text-slate-500 mt-0.5">
                        Цена: <span class="font-semibold text-slate-800">${unitRub},${unitKop} BYN</span> / шт.
                    </div>
                </div>
            </div>

            <div class="flex items-center justify-between w-full sm:w-auto gap-4 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                <!-- Compact Quantity Stepper -->
                <div class="qty-control">
                    <button type="button" class="qty-btn" onclick="updateQty(${item.cart_id}, ${item.quantity - 1})">−</button>
                    <input type="text" class="qty-input" value="${item.quantity}" readonly>
                    <button type="button" class="qty-btn" onclick="updateQty(${item.cart_id}, ${item.quantity + 1})">+</button>
                </div>

                <!-- Line Total -->
                <div class="text-right min-w-[80px]">
                    <span class="text-sm font-extrabold text-slate-900">${rub}</span><span class="text-xs font-semibold text-slate-500">,${kop}</span>
                    <span class="text-xs font-bold text-slate-700 ml-0.5">BYN</span>
                </div>

                <!-- Delete Action -->
                <button type="button" class="p-1.5 text-slate-400 hover:text-rose-600 rounded transition-colors" onclick="removeItem(${item.cart_id})" title="Удалить из заказа">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                </button>
            </div>
        </div>
        `;
    });
    html += '</div>';

    container.innerHTML = html;

    const formattedTotal = data.total_amount.toFixed(2) + ' BYN';
    if (totalEl) totalEl.textContent = formattedTotal;
    if (subtotalEl) subtotalEl.textContent = formattedTotal;
    if (checkoutBtn) checkoutBtn.disabled = false;

    if (typeof updateCartBadge === 'function') updateCartBadge();
}

async function updateQty(cartId, newQty) {
    if (newQty < 1) {
        removeItem(cartId);
        return;
    }

    const resp = await apiRequest(`/cart/${cartId}`, {
        method: 'PATCH',
        body: JSON.stringify({ quantity: newQty })
    });

    if (resp && resp.ok) {
        const data = await resp.json();
        renderCart(data);
    } else if (resp) {
        const err = await resp.json();
        showNotification(err.detail || 'Не удалось обновить', 'error');
    }
}

async function removeItem(cartId) {
    const resp = await apiRequest(`/cart/${cartId}`, {
        method: 'DELETE'
    });

    if (resp && resp.ok) {
        const data = await resp.json();
        renderCart(data);
        showNotification('Позиция удалена из заказа', 'info');
    }
}

function checkout() {
    window.location.href = '/orders/checkout';
}
