/**
 * Technical Blueprint SVG Illustrations for Automotive Parts
 * Precise vector schematics for each part category.
 */

const PartIcons = {
    // 1. Тормозная система: Вентилируемый диск с суппортом и перфорацией
    'Тормозная система': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Brake Disc Rotor -->
            <circle cx="32" cy="32" r="26" stroke="#64748b" stroke-width="2" stroke-dasharray="4 2"/>
            <circle cx="32" cy="32" r="22" stroke="#475569" stroke-width="1.5"/>
            <!-- Ventilation slots / holes -->
            <circle cx="32" cy="18" r="1.5" fill="#94a3b8"/>
            <circle cx="32" cy="46" r="1.5" fill="#94a3b8"/>
            <circle cx="18" cy="32" r="1.5" fill="#94a3b8"/>
            <circle cx="46" cy="32" r="1.5" fill="#94a3b8"/>
            <circle cx="22" cy="22" r="1.5" fill="#94a3b8"/>
            <circle cx="42" cy="42" r="1.5" fill="#94a3b8"/>
            <circle cx="22" cy="42" r="1.5" fill="#94a3b8"/>
            <circle cx="42" cy="22" r="1.5" fill="#94a3b8"/>
            <!-- Center Hat & Hub -->
            <circle cx="32" cy="32" r="12" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <circle cx="32" cy="32" r="5" stroke="#94a3b8" stroke-width="1.5"/>
            <!-- Lug Bolt Holes -->
            <circle cx="32" cy="25" r="1.5" fill="#0f172a"/>
            <circle cx="38" cy="29" r="1.5" fill="#0f172a"/>
            <circle cx="36" cy="36" r="1.5" fill="#0f172a"/>
            <circle cx="28" cy="36" r="1.5" fill="#0f172a"/>
            <circle cx="26" cy="29" r="1.5" fill="#0f172a"/>
            <!-- Caliper (Orange Accent) -->
            <path d="M42 12C46 16 48 22 48 28H56C56 19 50 12 42 12Z" fill="#ffedd5" stroke="#ea580c" stroke-width="2" stroke-linejoin="round"/>
            <rect x="47" y="18" width="6" height="12" rx="1" fill="#ea580c"/>
        </svg>
    `,

    // 2. Фильтры: Масляный/воздушный фильтр (Canister & Fluted core)
    'Фильтры': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Filter Canister Body -->
            <rect x="18" y="16" width="28" height="36" rx="3" fill="#f8fafc" stroke="#475569" stroke-width="2"/>
            <!-- Grip ribs -->
            <line x1="24" y1="22" x2="24" y2="44" stroke="#cbd5e1" stroke-width="1.5"/>
            <line x1="32" y1="22" x2="32" y2="44" stroke="#cbd5e1" stroke-width="1.5"/>
            <line x1="40" y1="22" x2="40" y2="44" stroke="#cbd5e1" stroke-width="1.5"/>
            <!-- Filter Top Base Flange -->
            <path d="M15 16H49V13C49 11.5 47.5 10 46 10H18C16.5 10 15 11.5 15 13V16Z" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
            <!-- O-Ring Seal (Orange Accent) -->
            <rect x="17" y="14" width="30" height="2.5" rx="1" fill="#ea580c"/>
            <!-- Center Threaded Hole -->
            <circle cx="32" cy="13" r="3" fill="#334155"/>
            <circle cx="26" cy="13" r="1.5" fill="#64748b"/>
            <circle cx="38" cy="13" r="1.5" fill="#64748b"/>
        </svg>
    `,

    // 3. Система зажигания: Свеча зажигания
    'Система зажигания': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Terminal nut -->
            <rect x="29.5" y="8" width="5" height="5" rx="1" fill="#334155"/>
            <!-- Ceramic Insulator Ribs -->
            <rect x="28" y="13" width="8" height="15" rx="1" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
            <line x1="28" y1="16" x2="36" y2="16" stroke="#94a3b8" stroke-width="1.5"/>
            <line x1="28" y1="20" x2="36" y2="20" stroke="#94a3b8" stroke-width="1.5"/>
            <line x1="28" y1="24" x2="36" y2="24" stroke="#94a3b8" stroke-width="1.5"/>
            <!-- Hexagonal Steel Nut -->
            <path d="M25 28H39L41 33H23L25 28Z" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
            <!-- Threaded Shell -->
            <rect x="27" y="33" width="10" height="18" fill="#e2e8f0" stroke="#334155" stroke-width="1.5"/>
            <line x1="26" y1="36" x2="38" y2="36" stroke="#475569" stroke-width="1.5"/>
            <line x1="26" y1="40" x2="38" y2="40" stroke="#475569" stroke-width="1.5"/>
            <line x1="26" y1="44" x2="38" y2="44" stroke="#475569" stroke-width="1.5"/>
            <line x1="26" y1="48" x2="38" y2="48" stroke="#475569" stroke-width="1.5"/>
            <!-- Center & Ground Electrode -->
            <rect x="31" y="51" width="2" height="4" fill="#0f172a"/>
            <path d="M28 51V57H33" stroke="#0f172a" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    `,

    // 4. Двигатель: Поршень с шатуном
    'Двигатель': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Piston Crown & Skirt -->
            <path d="M18 14H46V28C46 30 43 32 40 32H38V28H26V32H24C21 32 18 30 18 28V14Z" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <!-- Piston Ring Grooves -->
            <line x1="18" y1="18" x2="46" y2="18" stroke="#ea580c" stroke-width="1.5"/>
            <line x1="18" y1="21" x2="46" y2="21" stroke="#ea580c" stroke-width="1.5"/>
            <line x1="18" y1="24" x2="46" y2="24" stroke="#94a3b8" stroke-width="1.5"/>
            <!-- Wrist Pin Hole -->
            <circle cx="32" cy="27" r="3.5" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>
            <!-- Connecting Rod (Шатун) -->
            <path d="M30 30L28 48H36L34 30H30Z" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>
            <!-- Big End Journal -->
            <circle cx="32" cy="50" r="6" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <circle cx="32" cy="50" r="3" fill="#cbd5e1"/>
        </svg>
    `,

    // 5. Система охлаждения: Радиатор и помпа
    'Система охлаждения': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Radiator Core Grid -->
            <rect x="16" y="18" width="32" height="28" rx="2" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <!-- Honeycomb cooling fins -->
            <line x1="22" y1="18" x2="22" y2="46" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <line x1="28" y1="18" x2="28" y2="46" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <line x1="36" y1="18" x2="36" y2="46" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <line x1="42" y1="18" x2="42" y2="46" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <!-- Top Tank & Inlets -->
            <rect x="14" y="14" width="36" height="5" rx="1" fill="#e2e8f0" stroke="#334155" stroke-width="1.5"/>
            <rect x="20" y="10" width="6" height="4" fill="#ea580c"/>
            <!-- Bottom Tank & Outlets -->
            <rect x="14" y="45" width="36" height="5" rx="1" fill="#e2e8f0" stroke="#334155" stroke-width="1.5"/>
            <rect x="38" y="50" width="6" height="4" fill="#ea580c"/>
        </svg>
    `,

    // 6. Подвеска: Амортизаторная стойка с пружиной
    'Подвеска': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Top Mount -->
            <rect x="26" y="8" width="12" height="4" rx="1" fill="#334155"/>
            <!-- Chrome Strut Rod -->
            <rect x="30" y="12" width="4" height="20" fill="#e2e8f0" stroke="#64748b" stroke-width="1"/>
            <!-- Coil Spring (Витая пружина) -->
            <path d="M24 16C28 17 36 17 40 18C40 20 24 20 24 22C28 23 36 23 40 24C40 26 24 26 24 28C28 29 36 29 40 30C40 32 24 32 24 34C28 35 36 35 40 36" stroke="#ea580c" stroke-width="2.5" stroke-linecap="round"/>
            <!-- Lower Spring Perch -->
            <rect x="22" y="36" width="20" height="3" rx="1" fill="#334155"/>
            <!-- Damper Body Cylinder -->
            <rect x="27" y="39" width="10" height="16" rx="2" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <!-- Bottom Bushing Mount -->
            <circle cx="32" cy="56" r="4" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <circle cx="32" cy="56" r="1.5" fill="#334155"/>
        </svg>
    `,

    // 7. Электрика: Аккумулятор / Генератор
    'Электрика': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Battery Casing -->
            <rect x="14" y="20" width="36" height="32" rx="2" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <!-- Terminal Posts -->
            <rect x="18" y="14" width="6" height="6" fill="#334155"/>
            <rect x="40" y="14" width="6" height="6" fill="#ea580c"/>
            <!-- Polarity Marks -->
            <path d="M19.5 25H22.5" stroke="#334155" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M41.5 25H44.5M43 23.5V26.5" stroke="#ea580c" stroke-width="1.5" stroke-linecap="round"/>
            <!-- Battery Cell Caps / Bar -->
            <rect x="18" y="32" width="28" height="12" rx="1" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
            <!-- Voltage Lightning Bolt -->
            <path d="M33 34L29 40H33L31 44" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    `,

    // 8. Освещение: Лампа фары H7/H4
    'Освещение': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Glass Bulb -->
            <path d="M26 12C26 9.79 28.68 8 32 8C35.31 8 38 9.79 38 12V32H26V12Z" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
            <!-- Filament (Нить накала) -->
            <path d="M30 18L32 15L34 18M32 15V28" stroke="#f97316" stroke-width="1.2" stroke-linecap="round"/>
            <!-- Metal Collar / Flange -->
            <path d="M22 32H42V36H22V32Z" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
            <!-- Base Connectors -->
            <rect x="25" y="36" width="14" height="14" fill="#334155"/>
            <rect x="28" y="50" width="2" height="6" fill="#94a3b8"/>
            <rect x="34" y="50" width="2" height="6" fill="#94a3b8"/>
            <!-- Ray accents -->
            <line x1="20" y1="16" x2="16" y2="15" stroke="#fb923c" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="44" y1="16" x2="48" y2="15" stroke="#fb923c" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    `,

    // 9. Трансмиссия: Косозубые шестерни
    'Трансмиссия': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Big Gear Outer -->
            <circle cx="28" cy="34" r="16" stroke="#334155" stroke-width="2"/>
            <circle cx="28" cy="34" r="19" stroke="#64748b" stroke-width="2" stroke-dasharray="5 3"/>
            <circle cx="28" cy="34" r="7" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <circle cx="28" cy="34" r="3" fill="#cbd5e1"/>
            <!-- Small Meshing Gear (Accent Orange) -->
            <circle cx="44" cy="22" r="9" stroke="#ea580c" stroke-width="2"/>
            <circle cx="44" cy="22" r="12" stroke="#ea580c" stroke-width="2" stroke-dasharray="4 2"/>
            <circle cx="44" cy="22" r="3" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
        </svg>
    `,

    // 10. Рулевое управление: Рулевой наконечник
    'Рулевое управление': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Tie Rod Tube -->
            <rect x="10" y="34" width="22" height="6" rx="1" fill="#e2e8f0" stroke="#334155" stroke-width="1.5"/>
            <!-- Adjustment Threads -->
            <line x1="14" y1="34" x2="14" y2="40" stroke="#475569" stroke-width="1.2"/>
            <line x1="18" y1="34" x2="18" y2="40" stroke="#475569" stroke-width="1.2"/>
            <line x1="22" y1="34" x2="22" y2="40" stroke="#475569" stroke-width="1.2"/>
            <!-- Ball Joint Housing (Шарнир) -->
            <circle cx="40" cy="37" r="9" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <!-- Rubber Dust Boot (Orange) -->
            <path d="M36 28H44L46 22H34L36 28Z" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
            <!-- Tapered Ball Stud Pin -->
            <rect x="38" y="12" width="4" height="10" fill="#334155"/>
            <!-- Castle Nut & Hole -->
            <rect x="36" y="8" width="8" height="4" rx="1" fill="#64748b"/>
        </svg>
    `,

    // Дефолт / Общее: Металлическая ступица
    'default': `
        <svg class="w-20 h-20 text-slate-600" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="32" r="22" stroke="#475569" stroke-width="2" stroke-dasharray="6 3"/>
            <circle cx="32" cy="32" r="14" fill="#f8fafc" stroke="#334155" stroke-width="2"/>
            <circle cx="32" cy="32" r="6" fill="#cbd5e1" stroke="#334155" stroke-width="1.5"/>
            <circle cx="32" cy="22" r="2" fill="#ea580c"/>
            <circle cx="42" cy="32" r="2" fill="#ea580c"/>
            <circle cx="32" cy="42" r="2" fill="#ea580c"/>
            <circle cx="22" cy="32" r="2" fill="#ea580c"/>
        </svg>
    `
};

function getPartIllustration(category) {
    if (category && PartIcons[category]) {
        return PartIcons[category];
    }
    return PartIcons['default'];
}

function injectBlueprints() {
    document.querySelectorAll('[data-category]').forEach(card => {
        const target = card.querySelector('.part-blueprint-target');
        if (target && !target.hasAttribute('data-injected')) {
            const cat = card.getAttribute('data-category');
            target.innerHTML = getPartIllustration(cat);
            target.setAttribute('data-injected', 'true');
        }
    });
}

// Auto-inject blueprints on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectBlueprints);
} else {
    injectBlueprints();
}
