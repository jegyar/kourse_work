/**
 * AutoParts Store - Catalog Module (Clean Technical UX)
 * Implements real-time debounced search, instant selects, car model garage filter,
 * technical vector blueprints, and compact quantity-enabled buy actions.
 */

let currentPage = 1;
const pageSize = 12;
let searchDebounceTimer = null;

// Available car models mapped by make (from real catalog data)
const CAR_MODELS_BY_MAKE = {
    'Toyota': ['Toyota Camry', 'Toyota Corolla', 'Toyota RAV4'],
    'Volkswagen': ['Volkswagen Polo', 'Volkswagen Golf'],
    'Hyundai': ['Hyundai Solaris', 'Hyundai Creta'],
    'Kia': ['Kia Rio', 'Kia Sportage'],
    'Ford': ['Ford Focus', 'Ford Mondeo'],
    'Nissan': ['Nissan Qashqai'],
    'Skoda': ['Skoda Octavia', 'Skoda Rapid'],
    'Renault': ['Renault Duster', 'Renault Logan'],
    'Chevrolet': ['Chevrolet Aveo', 'Chevrolet Cruze'],
    'Mazda': ['Mazda 3']
};

function getEl(id) {
    return document.getElementById(id);
}

// ===== Render Strict Skeletons =====
function renderSkeletons() {
    const grid = getEl('productGrid');
    if (!grid) return;
    let html = '';
    for (let i = 0; i < 6; i++) {
        html += `
        <div class="part-card p-3.5 space-y-3">
            <div class="w-full h-36 skeleton"></div>
            <div class="flex gap-2">
                <div class="w-16 h-4 skeleton"></div>
                <div class="w-12 h-4 skeleton"></div>
            </div>
            <div class="space-y-1.5">
                <div class="w-full h-4 skeleton"></div>
                <div class="w-3/4 h-4 skeleton"></div>
            </div>
            <div class="pt-2 border-t border-slate-100 flex items-center justify-between">
                <div class="w-20 h-5 skeleton"></div>
                <div class="w-24 h-8 skeleton"></div>
            </div>
        </div>
        `;
    }
    grid.innerHTML = html;
}

// ===== Populate Garage Filter (Makes & Models) =====
function initCarFilters() {
    const carMakeSelect = getEl('carMakeSelect');
    const carModelSelect = getEl('carModelSelect');
    if (!carMakeSelect || !carModelSelect) return;

    carMakeSelect.addEventListener('change', () => {
        const make = carMakeSelect.value;
        carModelSelect.innerHTML = '<option value="">Все модели</option>';

        if (make && CAR_MODELS_BY_MAKE[make]) {
            CAR_MODELS_BY_MAKE[make].forEach(model => {
                const opt = document.createElement('option');
                opt.value = model;
                const shortName = model.replace(make, '').trim();
                opt.textContent = shortName ? `${make} ${shortName}` : model;
                carModelSelect.appendChild(opt);
            });
        }

        currentPage = 1;
        loadProducts();
    });

    carModelSelect.addEventListener('change', () => {
        currentPage = 1;
        loadProducts();
    });

    const resetCarBtn = getEl('resetCarFilter');
    if (resetCarBtn) {
        resetCarBtn.addEventListener('click', () => {
            carMakeSelect.value = '';
            carModelSelect.innerHTML = '<option value="">Все модели</option>';
            currentPage = 1;
            loadProducts();
        });
    }
}

// ===== Load Dynamic Categories & Brands (if not pre-populated) =====
async function loadFilterOptions() {
    const categorySelect = getEl('categorySelect');
    const brandSelect = getEl('brandSelect');
    const searchInput = getEl('searchInput');
    const clearSearchBtn = getEl('clearSearchBtn');

    try {
        const urlParams = new URLSearchParams(window.location.search);
        const urlCat = urlParams.get('category');
        const urlBrand = urlParams.get('brand');
        const urlSearch = urlParams.get('search');

        if (urlSearch && searchInput && !searchInput.value) {
            searchInput.value = urlSearch;
            if (clearSearchBtn) clearSearchBtn.classList.remove('hidden');
        }

        const needsCat = categorySelect && categorySelect.options.length <= 1;
        const needsBrand = brandSelect && brandSelect.options.length <= 1;

        if (needsCat || needsBrand) {
            const [catResp, brandResp] = await Promise.all([
                needsCat ? fetch('/products/categories') : Promise.resolve(null),
                needsBrand ? fetch('/products/brands') : Promise.resolve(null)
            ]);

            if (catResp && catResp.ok && categorySelect) {
                const categories = await catResp.json();
                categories.forEach(c => {
                    const opt = document.createElement('option');
                    opt.value = c;
                    opt.textContent = c;
                    if (urlCat === c) opt.selected = true;
                    categorySelect.appendChild(opt);
                });
            }

            if (brandResp && brandResp.ok && brandSelect) {
                const brands = await brandResp.json();
                brands.forEach(b => {
                    const opt = document.createElement('option');
                    opt.value = b;
                    opt.textContent = b;
                    if (urlBrand === b) opt.selected = true;
                    brandSelect.appendChild(opt);
                });
            }
        } else {
            // Apply URL selections to already populated selects
            if (urlCat && categorySelect) categorySelect.value = urlCat;
            if (urlBrand && brandSelect) brandSelect.value = urlBrand;
        }
    } catch (e) {
        console.error('Failed to load filter options', e);
    }
}

// ===== Format Technical Price (Integer + Small Pennies) =====
function formatTechnicalPrice(price) {
    const num = parseFloat(price);
    const formatted = isNaN(num) ? '0.00' : num.toFixed(2);
    const [rub, kop] = formatted.split('.');
    return `
        <span class="text-base font-extrabold text-slate-900">${rub}</span><span class="text-xs font-semibold text-slate-500">,${kop}</span>
        <span class="text-xs font-bold text-slate-700 ml-0.5">BYN</span>
    `;
}

// ===== Create Part Card HTML with Blueprint SVG =====
function createProductCardHTML(p) {
    const inStock = p.stock_quantity > 0;
    const priceHtml = formatTechnicalPrice(p.price);

    let imageContent = '';
    if (p.image_url) {
        imageContent = `<img src="${p.image_url}" alt="${p.name}" class="w-full h-full object-contain p-2" loading="lazy">`;
    } else {
        const svgIllustration = typeof getPartIllustration === 'function' 
            ? getPartIllustration(p.category) 
            : `<svg class="w-16 h-16 text-slate-400" viewBox="0 0 64 64"><circle cx="32" cy="32" r="20" stroke="currentColor" stroke-width="2"/></svg>`;
        imageContent = `<div class="p-2">${svgIllustration}</div>`;
    }

    return `
    <div class="part-card flex flex-col justify-between p-3.5">
        <div>
            <!-- Technical Blueprint Frame -->
            <div class="part-illustration w-full h-36 rounded mb-2.5 overflow-hidden">
                ${imageContent}
            </div>

            <!-- Tags: Quiet steel style -->
            <div class="flex flex-wrap items-center gap-1.5 mb-2">
                <span class="part-tag">${p.category || 'Запчасть'}</span>
                <span class="brand-tag">${p.brand || 'OEM'}</span>
            </div>

            <!-- Product Title -->
            <h3 class="font-semibold text-slate-900 text-sm leading-snug line-clamp-2 mb-1" title="${p.name}">
                ${p.name}
            </h3>

            <!-- Vehicle Application -->
            ${p.car_model ? `
                <p class="text-xs text-slate-500 mb-2 truncate">
                    Совместимость: <span class="font-medium text-slate-700">${p.car_model}</span>
                </p>
            ` : '<div class="h-4 mb-2"></div>'}
        </div>

        <!-- Card Footer -->
        <div class="pt-2.5 border-t border-slate-100 space-y-2.5">
            <div class="flex items-center justify-between">
                <!-- Stock status -->
                ${inStock ? `
                    <span class="stock-indicator text-emerald-700">
                        <span class="stock-dot-in"></span> В наличии: ${p.stock_quantity} шт.
                    </span>
                ` : `
                    <span class="stock-indicator text-amber-700">
                        <span class="stock-dot-out"></span> Склад: 2–3 дня
                    </span>
                `}

                <!-- Price -->
                <div class="text-right">
                    ${priceHtml}
                </div>
            </div>

            <!-- Compact Buy Controls (Stepper + Cart Button) -->
            <div class="flex items-center justify-between gap-2 pt-0.5">
                <div class="qty-control" title="Количество">
                    <button type="button" class="qty-btn" onclick="adjustQty(${p.product_id}, -1)">−</button>
                    <input type="text" class="qty-input" id="qty-input-${p.product_id}" value="1" readonly>
                    <button type="button" class="qty-btn" onclick="adjustQty(${p.product_id}, 1)">+</button>
                </div>

                ${inStock ? `
                    <button type="button" onclick="buyPart(${p.product_id})" class="btn-cart-compact flex-1 justify-center">
                        <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        <span>В корзину</span>
                    </button>
                ` : `
                    <button type="button" disabled class="btn-cart-compact flex-1 justify-center opacity-60">
                        <span>Под заказ</span>
                    </button>
                `}
            </div>
        </div>
    </div>
    `;
}

// ===== Quantity Control Stepper =====
window.adjustQty = function(productId, delta) {
    const input = document.getElementById(`qty-input-${productId}`);
    if (!input) return;
    let val = parseInt(input.value) || 1;
    val += delta;
    if (val < 1) val = 1;
    if (val > 99) val = 99;
    input.value = val;
};

// ===== Add Custom Quantity To Cart =====
window.buyPart = async function(productId) {
    const input = document.getElementById(`qty-input-${productId}`);
    const quantity = input ? (parseInt(input.value) || 1) : 1;

    const token = typeof getToken === 'function' ? getToken() : localStorage.getItem('access_token');
    if (!token) {
        if (typeof showNotification === 'function') {
            showNotification('Авторизуйтесь для добавления деталей в корзину', 'warning');
        } else {
            alert('Авторизуйтесь для добавления деталей в корзину');
        }
        setTimeout(() => window.location.href = '/login', 1200);
        return;
    }

    try {
        const resp = await apiRequest('/cart/', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity: quantity })
        });

        if (resp && resp.ok) {
            if (typeof showNotification === 'function') {
                showNotification(`Добавлено в корзину (${quantity} шт.)`, 'success');
            }
            if (typeof updateCartBadge === 'function') updateCartBadge();
        } else if (resp) {
            const err = await resp.json();
            if (typeof showNotification === 'function') {
                showNotification(err.detail || 'Ошибка добавления', 'error');
            }
        }
    } catch (e) {
        if (typeof showNotification === 'function') {
            showNotification('Ошибка связи с сервером', 'error');
        }
    }
};

window.addToCart = function(productId) {
    window.buyPart(productId);
};

// ===== Load Products (Instant & Filtered) =====
async function loadProducts() {
    const grid = getEl('productGrid');
    const countSpan = getEl('productCount');
    const pagination = getEl('pagination');
    if (!grid) return;

    renderSkeletons();

    const searchInput = getEl('searchInput');
    const categorySelect = getEl('categorySelect');
    const brandSelect = getEl('brandSelect');
    const sortSelect = getEl('sortSelect');
    const carMakeSelect = getEl('carMakeSelect');
    const carModelSelect = getEl('carModelSelect');
    const inStockCheckbox = getEl('inStockCheckbox');

    const params = new URLSearchParams();
    params.append('page', currentPage);
    params.append('size', pageSize);

    // Keyword search
    const rawSearch = searchInput?.value.trim() || '';
    if (rawSearch) {
        params.append('search', rawSearch);
    }

    // Car model / make filter
    const carMake = carMakeSelect?.value || '';
    const carModel = carModelSelect?.value || '';
    const effectiveCar = carModel || carMake;
    if (effectiveCar) {
        params.append('car_model', effectiveCar);
    }

    const category = categorySelect?.value;
    if (category) params.append('category', category);

    const brand = brandSelect?.value;
    if (brand) params.append('brand', brand);

    const sortVal = sortSelect?.value ? sortSelect.value.split('-') : ['product_id', 'false'];
    params.append('sort_by', sortVal[0]);
    params.append('sort_desc', sortVal[1]);

    try {
        const response = await fetch(`/products/?${params.toString()}`);
        if (!response.ok) throw new Error('API Error');

        const data = await response.json();
        let items = data.items || [];

        // In-stock filter on the client if checked
        if (inStockCheckbox && inStockCheckbox.checked) {
            items = items.filter(p => p.stock_quantity > 0);
        }

        if (items.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full py-12 px-4 text-center bg-white border border-slate-200 rounded">
                    <div class="w-12 h-12 mx-auto text-slate-400 mb-2">
                        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                    <h3 class="font-bold text-slate-800 text-sm mb-1">Ничего не найдено</h3>
                    <p class="text-xs text-slate-500 max-w-sm mx-auto mb-3">
                        По выбранным критериям запчастей не найдено. Попробуйте сбросить фильтр по автомобилю или изменить параметры поиска.
                    </p>
                    <button type="button" onclick="const r = document.getElementById('resetAllFilters'); if (r) r.click();" class="px-3 py-1.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors">
                        Сбросить фильтры
                    </button>
                </div>
            `;
            if (countSpan) countSpan.textContent = '0 позиций';
            if (pagination) pagination.innerHTML = '';
            return;
        }

        grid.innerHTML = items.map(p => createProductCardHTML(p)).join('');
        if (countSpan) countSpan.textContent = `Найдено: ${items.length} из ${data.total}`;
        renderPagination(data.total);

        // Inject blueprints into server or client cards if needed
        if (typeof injectBlueprints === 'function') {
            injectBlueprints();
        }
    } catch (e) {
        console.error('Failed to load products', e);
        grid.innerHTML = `
            <div class="col-span-full py-8 text-center text-xs text-rose-600 bg-rose-50 border border-rose-200 rounded">
                Ошибка при загрузке каталога деталей. <button onclick="loadProducts()" class="font-bold underline ml-1">Повторить</button>
            </div>
        `;
    }
}

// ===== Crisp Numbered Pagination =====
function renderPagination(totalItems) {
    const pagination = getEl('pagination');
    if (!pagination) return;
    const totalPages = Math.ceil(totalItems / pageSize);
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = `
        <button class="px-2.5 py-1 text-xs font-semibold rounded border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(${currentPage - 1})">
            Предыдущая
        </button>
    `;

    for (let i = 1; i <= totalPages; i++) {
        const isActive = i === currentPage;
        html += `
            <button class="w-8 h-7 text-xs font-bold rounded border ${isActive ? 'bg-slate-900 border-slate-900 text-white' : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'}" onclick="changePage(${i})">
                ${i}
            </button>
        `;
    }

    html += `
        <button class="px-2.5 py-1 text-xs font-semibold rounded border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed" ${currentPage === totalPages ? 'disabled' : ''} onclick="changePage(${currentPage + 1})">
            Следующая
        </button>
    `;

    pagination.innerHTML = html;
}

window.changePage = function(page) {
    currentPage = page;
    loadProducts();
    window.scrollTo({ top: 120, behavior: 'smooth' });
};

// ===== Setup Real-time Listeners =====
function setupFilterListeners() {
    const searchInput = getEl('searchInput');
    const clearSearchBtn = getEl('clearSearchBtn');
    const categorySelect = getEl('categorySelect');
    const brandSelect = getEl('brandSelect');
    const sortSelect = getEl('sortSelect');
    const inStockCheckbox = getEl('inStockCheckbox');
    const carMakeSelect = getEl('carMakeSelect');
    const carModelSelect = getEl('carModelSelect');

    // 1. Debounced Search (300ms)
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            if (clearSearchBtn) {
                clearSearchBtn.classList.toggle('hidden', !searchInput.value);
            }
            clearTimeout(searchDebounceTimer);
            searchDebounceTimer = setTimeout(() => {
                currentPage = 1;
                loadProducts();
            }, 300);
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            clearSearchBtn.classList.add('hidden');
            currentPage = 1;
            loadProducts();
        });
    }

    // 2. Instant Select triggers
    if (categorySelect) {
        categorySelect.addEventListener('change', () => {
            currentPage = 1;
            loadProducts();
        });
    }

    if (brandSelect) {
        brandSelect.addEventListener('change', () => {
            currentPage = 1;
            loadProducts();
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            currentPage = 1;
            loadProducts();
        });
    }

    if (inStockCheckbox) {
        inStockCheckbox.addEventListener('change', () => {
            currentPage = 1;
            loadProducts();
        });
    }

    // 3. Reset All Filters
    const resetAllBtn = getEl('resetAllFilters');
    if (resetAllBtn) {
        resetAllBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            if (clearSearchBtn) clearSearchBtn.classList.add('hidden');
            if (categorySelect) categorySelect.value = '';
            if (brandSelect) brandSelect.value = '';
            if (sortSelect) sortSelect.value = 'product_id-false';
            if (carMakeSelect) carMakeSelect.value = '';
            if (carModelSelect) carModelSelect.innerHTML = '<option value="">Все модели</option>';
            if (inStockCheckbox) inStockCheckbox.checked = false;

            currentPage = 1;
            loadProducts();
        });
    }
}

// ===== Initialization =====
async function initCatalog() {
    initCarFilters();
    setupFilterListeners();
    await loadFilterOptions();

    // If server already rendered product cards, inject blueprints without immediately refetching
    const grid = getEl('productGrid');
    if (grid && grid.children.length > 0 && !grid.querySelector('.skeleton')) {
        if (typeof injectBlueprints === 'function') {
            injectBlueprints();
        }
    } else {
        await loadProducts();
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCatalog);
} else {
    initCatalog();
}
