/**
 * AutoParts Store - Admin Module (Industrial Clean Architecture)
 */

const statusMap = {
    'new': ['Новый', 'status-new'],
    'confirmed': ['Подтверждён', 'status-confirmed'],
    'processing': ['В обработке', 'status-processing'],
    'shipped': ['Отправлен', 'status-shipped'],
    'delivered': ['Доставлен', 'status-delivered'],
    'cancelled': ['Отменён', 'status-cancelled']
};

function fmtDate(d) {
    return new Date(d).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

function fmtPrice(v) {
    return parseFloat(v).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' BYN';
}

// ==================== TAB SWITCHING ====================
function showTab(tab) {
    document.querySelectorAll('.admin-tab').forEach(t => t.classList.add('hidden'));
    const target = document.getElementById('tab-' + tab);
    if (target) target.classList.remove('hidden');

    document.querySelectorAll('.admin-nav-link').forEach(btn => {
        if (btn.getAttribute('data-tab') === tab) {
            btn.className = 'admin-nav-link active w-full px-3 py-2 rounded text-xs font-bold text-left bg-slate-900 text-white transition-colors';
        } else {
            btn.className = 'admin-nav-link w-full px-3 py-2 rounded text-xs font-semibold text-slate-700 hover:bg-slate-100 text-left transition-colors';
        }
    });

    if (tab === 'dashboard') loadDashboard();
    if (tab === 'products') loadAdminProducts();
    if (tab === 'orders') loadAdminOrders();
    if (tab === 'users') loadAdminUsers();
}

// ==================== DASHBOARD ====================
async function loadDashboard() {
    const resp = await apiRequest('/admin_api/stats');
    if (!resp || !resp.ok) return;
    const d = await resp.json();

    const statsCards = document.getElementById('statsCards');
    if (statsCards) {
        statsCards.innerHTML = `
            <div class="part-card p-3.5">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Номенклатура</div>
                <div class="text-xl font-black text-slate-900 mt-0.5">${d.products} шт.</div>
            </div>
            <div class="part-card p-3.5">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Всего заказов</div>
                <div class="text-xl font-black text-slate-900 mt-0.5">${d.orders}</div>
            </div>
            <div class="part-card p-3.5">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Клиентская база</div>
                <div class="text-xl font-black text-slate-900 mt-0.5">${d.users}</div>
            </div>
            <div class="part-card p-3.5">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Общий оборот</div>
                <div class="text-xl font-black text-slate-900 mt-0.5">${fmtPrice(d.revenue)}</div>
            </div>
        `;
    }

    const tbody = document.getElementById('recentOrdersBody');
    if (tbody && d.recent_orders) {
        tbody.innerHTML = d.recent_orders.map(o => `
            <tr class="hover:bg-slate-50">
                <td class="px-4 py-2 font-bold text-slate-900">#${o.order_id}</td>
                <td class="px-4 py-2 text-slate-700">${o.email}</td>
                <td class="px-4 py-2 font-bold text-slate-900">${fmtPrice(o.total_amount)}</td>
                <td class="px-4 py-2"><span class="status-pill ${statusMap[o.status]?.[1] || 'status-new'}">${statusMap[o.status]?.[0] || o.status}</span></td>
                <td class="px-4 py-2 text-slate-500">${fmtDate(o.created_at)}</td>
            </tr>
        `).join('');
    }
}

// ==================== PRODUCTS ====================
async function loadAdminProducts() {
    const resp = await apiRequest('/admin_api/products');
    if (!resp || !resp.ok) return;
    const products = await resp.json();

    const tbody = document.getElementById('productsBody');
    if (!tbody) return;

    tbody.innerHTML = products.map(p => `
        <tr class="hover:bg-slate-50">
            <td class="px-3 py-2 font-mono text-slate-500">${p.product_id}</td>
            <td class="px-3 py-2 font-semibold text-slate-900">${p.name}</td>
            <td class="px-3 py-2 text-slate-700">${p.brand}</td>
            <td class="px-3 py-2 text-slate-500">${p.category}</td>
            <td class="px-3 py-2 font-bold text-slate-900">${fmtPrice(p.price)}</td>
            <td class="px-3 py-2">${p.stock_quantity} шт.</td>
            <td class="px-3 py-2">
                ${p.is_active ? '<span class="text-emerald-700 font-semibold">Активен</span>' : '<span class="text-slate-400">Скрыт</span>'}
            </td>
            <td class="px-3 py-2 text-right">
                <button type="button" class="text-slate-600 hover:text-slate-900 font-semibold mr-2" onclick='showProductModal(${JSON.stringify(p)})'>Правка</button>
                <button type="button" class="text-rose-600 hover:text-rose-800 font-semibold" onclick="deleteProduct(${p.product_id})">Отключить</button>
            </td>
        </tr>
    `).join('');
}

function showProductModal(data = null) {
    const modal = document.getElementById('productModal');
    const title = document.getElementById('productModalTitle');
    if (!modal) return;

    const isEdit = !!data;
    title.textContent = isEdit ? `Редактирование: ${data.name}` : 'Добавить товар в номенклатуру';

    document.getElementById('pId').value = data?.product_id || '';
    document.getElementById('pName').value = data?.name || '';
    document.getElementById('pBrand').value = data?.brand || '';
    document.getElementById('pCategory').value = data?.category || '';
    document.getElementById('pCarModel').value = data?.car_model || '';
    document.getElementById('pPrice').value = data?.price || '';
    document.getElementById('pStock').value = data?.stock_quantity ?? '';
    document.getElementById('pDesc').value = data?.description || '';

    modal.classList.remove('hidden');
}

function closeProductModal() {
    const modal = document.getElementById('productModal');
    if (modal) modal.classList.add('hidden');
}

const productModalForm = document.getElementById('productModalForm');
if (productModalForm) {
    productModalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const pid = document.getElementById('pId').value;
        const payload = {
            name: document.getElementById('pName').value.trim(),
            brand: document.getElementById('pBrand').value.trim(),
            category: document.getElementById('pCategory').value.trim(),
            car_model: document.getElementById('pCarModel').value.trim() || null,
            price: parseFloat(document.getElementById('pPrice').value),
            stock_quantity: parseInt(document.getElementById('pStock').value),
            description: document.getElementById('pDesc').value.trim() || null,
            image_url: null,
            is_active: true
        };

        const url = pid ? `/admin_api/products/${pid}` : '/admin_api/products';
        const method = pid ? 'PUT' : 'POST';

        const resp = await apiRequest(url, { method, body: JSON.stringify(payload) });
        if (resp && resp.ok) {
            showNotification(pid ? 'Данные обновлены' : 'Товар добавлен', 'success');
            closeProductModal();
            loadAdminProducts();
        } else if (resp) {
            const err = await resp.json();
            showNotification(err.detail || 'Ошибка сохранения', 'error');
        }
    });
}

async function deleteProduct(id) {
    if (!confirm('Отключить товар из каталога?')) return;
    const resp = await apiRequest(`/admin_api/products/${id}`, { method: 'DELETE' });
    if (resp && resp.ok) {
        showNotification('Товар отключен', 'info');
        loadAdminProducts();
    }
}

// ==================== EXPORT / IMPORT ====================
function exportProducts(format) {
    const token = getToken();
    fetch(`/admin_api/export/products?format=${format}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(resp => {
        if (!resp.ok) throw new Error('Export error');
        return resp.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `products.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        showNotification(`Каталог экспортирован в ${format.toUpperCase()}`, 'success');
    })
    .catch(() => showNotification('Ошибка экспорта', 'error'));
}

const importForm = document.getElementById('importForm');
if (importForm) {
    importForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = document.getElementById('importFile');
        if (!fileInput.files.length) {
            showNotification('Выберите файл для импорта', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const token = getToken();
        try {
            const resp = await fetch('/admin_api/import/products', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            if (resp.ok) {
                const data = await resp.json();
                showNotification(data.message || 'Импорт завершен', 'success');
                fileInput.value = '';
                loadAdminProducts();
            } else {
                const err = await resp.json();
                showNotification(err.detail || 'Ошибка импорта', 'error');
            }
        } catch (e) {
            showNotification('Ошибка связи', 'error');
        }
    });
}

// ==================== ORDERS ====================
async function loadAdminOrders() {
    const status = document.getElementById('orderStatusFilter')?.value;
    const url = status ? `/admin_api/orders?status=${status}` : '/admin_api/orders';
    const resp = await apiRequest(url);
    if (!resp || !resp.ok) return;
    const orders = await resp.json();

    const tbody = document.getElementById('ordersBody');
    if (!tbody) return;

    tbody.innerHTML = orders.map(o => `
        <tr class="hover:bg-slate-50">
            <td class="px-3 py-2 font-bold text-slate-900">#${o.order_id}</td>
            <td class="px-3 py-2 text-slate-700">
                ${o.first_name} ${o.last_name} <span class="text-slate-400">(${o.email})</span>
            </td>
            <td class="px-3 py-2 font-bold text-slate-900">${fmtPrice(o.total_amount)}</td>
            <td class="px-3 py-2">
                <span class="status-pill ${statusMap[o.status]?.[1] || 'status-new'}">${statusMap[o.status]?.[0] || o.status}</span>
            </td>
            <td class="px-3 py-2 text-slate-500">${fmtDate(o.created_at)}</td>
            <td class="px-3 py-2 text-right">
                <select onchange="changeOrderStatus(${o.order_id}, this.value)" class="text-xs h-7 px-1.5 border border-slate-300 rounded bg-white mr-1">
                    ${['new', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'].map(
                        s => `<option value="${s}" ${s === o.status ? 'selected' : ''}>${statusMap[s]?.[0] || s}</option>`
                    ).join('')}
                </select>
                <button type="button" class="text-slate-600 hover:text-slate-900 font-semibold" onclick="downloadOrderPdf(${o.order_id})">PDF</button>
            </td>
        </tr>
    `).join('');
}

function downloadOrderPdf(orderId) {
    const token = getToken();
    fetch(`/admin_api/orders/${orderId}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(resp => {
        if (!resp.ok) throw new Error('PDF error');
        return resp.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `order_${orderId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        showNotification(`Накладная #${orderId} сохранена`, 'success');
    })
    .catch(() => showNotification('Ошибка загрузки PDF', 'error'));
}

async function changeOrderStatus(orderId, status) {
    const resp = await apiRequest(`/admin_api/orders/${orderId}/status?status=${status}`, { method: 'PATCH' });
    if (resp && resp.ok) {
        showNotification(`Статус заказа #${orderId} изменен`, 'success');
        loadAdminOrders();
    } else if (resp) {
        const err = await resp.json();
        showNotification(err.detail || 'Ошибка смены статуса', 'error');
    }
}

// ==================== REPORTS ====================
function downloadReport(type) {
    const token = getToken();
    fetch(`/admin_api/export/sales/${type}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(resp => {
        if (!resp.ok) throw new Error('Report error');
        return resp.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const ext = type === 'excel' ? 'xlsx' : 'docx';
        a.download = `report.${ext}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        showNotification('Сводка сформирована', 'success');
    })
    .catch(() => showNotification('Ошибка генерации отчета', 'error'));
}

// ==================== USERS ====================
async function loadAdminUsers() {
    const resp = await apiRequest('/admin_api/users');
    if (!resp || !resp.ok) return;
    const users = await resp.json();

    const tbody = document.getElementById('usersBody');
    if (!tbody) return;

    tbody.innerHTML = users.map(u => `
        <tr class="hover:bg-slate-50">
            <td class="px-3 py-2 font-mono text-slate-500">${u.user_id}</td>
            <td class="px-3 py-2 font-semibold text-slate-900">${u.email}</td>
            <td class="px-3 py-2 text-slate-700">${u.first_name} ${u.last_name}</td>
            <td class="px-3 py-2">
                <span class="text-xs font-semibold ${u.role_name === 'admin' ? 'text-purple-700' : 'text-slate-600'}">
                    ${u.role_name === 'admin' ? 'Администратор' : 'Клиент'}
                </span>
            </td>
            <td class="px-3 py-2 text-slate-500">${fmtDate(u.created_at)}</td>
            <td class="px-3 py-2 text-right">
                <select onchange="changeUserRole(${u.user_id}, this.value)" class="text-xs h-7 px-1.5 border border-slate-300 rounded bg-white mr-1">
                    <option value="1" ${u.role_name === 'admin' ? 'selected' : ''}>Админ</option>
                    <option value="2" ${u.role_name === 'client' ? 'selected' : ''}>Клиент</option>
                </select>
                <button type="button" class="text-rose-600 hover:text-rose-800 font-semibold" onclick="deleteUser(${u.user_id})">Удалить</button>
            </td>
        </tr>
    `).join('');
}

async function changeUserRole(userId, roleId) {
    const resp = await apiRequest(`/admin_api/users/${userId}/role?role_id=${roleId}`, { method: 'PATCH' });
    if (resp && resp.ok) {
        showNotification('Роль изменена', 'success');
        loadAdminUsers();
    }
}

async function deleteUser(userId) {
    if (!confirm('Удалить пользователя?')) return;
    const resp = await apiRequest(`/admin_api/users/${userId}`, { method: 'DELETE' });
    if (resp && resp.ok) {
        showNotification('Пользователь удален', 'info');
        loadAdminUsers();
    }
}

window.downloadReport = downloadReport;
window.downloadOrderPdf = downloadOrderPdf;
window.exportProducts = exportProducts;
window.showProductModal = showProductModal;
window.closeProductModal = closeProductModal;
window.changeOrderStatus = changeOrderStatus;

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
