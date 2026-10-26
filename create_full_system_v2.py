import xml.etree.ElementTree as ET

def create_flowchart(filepath):
    mxfile = ET.Element('mxfile', version="14.6.13")
    diagram = ET.SubElement(mxfile, 'diagram', id="full_sys_v2", name="Full System Flow v2")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1400", dy="1200", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1600", pageHeight="1400", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')

    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    # ── Styles ──
    start_style   = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=13;strokeWidth=2;"
    end_style     = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;strokeWidth=2;"
    process_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;strokeWidth=1.5;"
    decision_style= "shape=rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;fontStyle=1;strokeWidth=1.5;"
    io_style      = "shape=parallelogram;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=12;strokeWidth=1.5;"
    db_style      = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e6d0de;strokeColor=#996185;fontSize=12;fontStyle=1;strokeWidth=2;"
    admin_style   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=12;strokeWidth=1.5;"
    edge_style    = "endArrow=classic;html=1;rounded=1;strokeWidth=1.5;strokeColor=#333333;jetSize=auto;orthogonalLoop=1;edgeStyle=orthogonalEdgeStyle;"
    edge_back     = "endArrow=classic;html=1;rounded=1;strokeWidth=1.5;strokeColor=#999999;dashed=1;jetSize=auto;orthogonalLoop=1;edgeStyle=orthogonalEdgeStyle;"

    # Block group styles (containers)
    block_auth    = "rounded=1;whiteSpace=wrap;html=1;fillColor=#EBF5FB;strokeColor=#5DADE2;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;strokeWidth=2;dashed=0;container=1;collapsible=0;swimlaneLine=0;"
    block_catalog = "rounded=1;whiteSpace=wrap;html=1;fillColor=#EAFAF1;strokeColor=#58D68D;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;strokeWidth=2;dashed=0;container=1;collapsible=0;swimlaneLine=0;"
    block_cart    = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF9E7;strokeColor=#F4D03F;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;strokeWidth=2;dashed=0;container=1;collapsible=0;swimlaneLine=0;"
    block_admin   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FDEDEC;strokeColor=#E74C3C;fontSize=14;fontStyle=1;verticalAlign=top;spacingTop=5;strokeWidth=2;dashed=0;container=1;collapsible=0;swimlaneLine=0;"

    cid = [100]  # counter for unique ids

    def nid():
        cid[0] += 1
        return str(cid[0])

    def add_node(node_id, value, style, x, y, w, h, parent="1"):
        cell = ET.SubElement(root, 'mxCell', id=node_id, value=value, style=style, vertex="1", parent=parent)
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})

    def add_edge(edge_id, source, target, label="", style_=edge_style):
        cell = ET.SubElement(root, 'mxCell', id=edge_id, value=label, style=style_, edge="1", parent="1", source=source, target=target)
        geo = ET.SubElement(cell, 'mxGeometry', relative="1", **{'as': 'geometry'})
        if label:
            lbl = ET.SubElement(root, 'mxCell', id=f"lbl_{edge_id}", value=label, style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];backgroundColor=#ffffff;fontSize=10;fontColor=#555555;", vertex="1", connectable="0", parent=edge_id)
            ET.SubElement(lbl, 'mxGeometry', relative="1", **{'as': 'geometry'})

    # ========================================
    # TOP SECTION: Start + Main Page + Router
    # ========================================
    add_node("Start", "Вход на сайт", start_style, 680, 30, 140, 50)
    add_node("Home",  "Главная страница\nинтернет-магазина", process_style, 670, 120, 160, 55)
    add_node("Router", "Выбор\nраздела", decision_style, 690, 230, 120, 80)

    add_edge("eS1", "Start", "Home")
    add_edge("eS2", "Home", "Router")

    # ========================================
    # BLOCK 1 — AUTH (left, x=30..280)
    # ========================================
    BW, BH = 270, 570
    BX1, BY1 = 30, 350
    add_node("GrpAuth", "Авторизация и Профиль", block_auth, BX1, BY1, BW, BH)

    # Nodes inside (coords relative to parent container)
    add_node("CheckAuth",   "Авторизован?",         decision_style, 55, 40, 160, 70,  "GrpAuth")
    add_node("LoginPage",   "Страница входа\n/ регистрации",  io_style,  65, 150, 140, 50, "GrpAuth")
    add_node("ValidCreds",  "Данные\nверны?",       decision_style, 55, 240, 160, 70,  "GrpAuth")
    add_node("AuthError",   "Ошибка\nавторизации",  end_style,      5, 350, 120, 50,   "GrpAuth")
    add_node("Profile",     "Личный кабинет",       process_style,  65, 360, 140, 45,  "GrpAuth")
    add_node("OrderHist",   "Просмотр\nистории заказов", process_style, 65, 440, 140, 50, "GrpAuth")
    add_node("Logout",      "Выход",                end_style,      75, 520, 120, 40,  "GrpAuth")

    add_edge("a0", "Router", "CheckAuth",    "Профиль")
    add_edge("a1", "CheckAuth", "LoginPage",  "Нет")
    add_edge("a2", "LoginPage", "ValidCreds")
    add_edge("a3", "ValidCreds", "AuthError",  "Нет")
    add_edge("a4", "ValidCreds", "Profile",    "Да")
    add_edge("a5", "CheckAuth",  "Profile",    "Да")
    add_edge("a6", "Profile",    "OrderHist")
    add_edge("a7", "OrderHist",  "Logout")

    # ========================================
    # BLOCK 2 — CATALOG (center-left, x=330..600)
    # ========================================
    BX2 = 330
    add_node("GrpCatalog", "Каталог товаров", block_catalog, BX2, BY1, BW, BH)

    add_node("CatPage",    "Страница каталога",          process_style,  65, 40,  140, 45, "GrpCatalog")
    add_node("Filter",     "Поиск / Фильтрация\n(бренд, категория, модель)", io_style, 35, 120, 200, 55, "GrpCatalog")
    add_node("HasResults", "Найдены\nтовары?",           decision_style, 55, 215, 160, 70, "GrpCatalog")
    add_node("NoResults",  "Нет результатов\n(изменить фильтр)", process_style, 5, 330, 130, 50, "GrpCatalog")
    add_node("ProdCard",   "Карточка товара\n(описание, цена, фото)", process_style, 55, 330, 160, 55, "GrpCatalog")
    add_node("AddBtn",     "Добавить\nв корзину?",       decision_style, 55, 420, 160, 70, "GrpCatalog")
    add_node("SaveCart",   "Сохранение\nв корзину",       process_style,  65, 520, 140, 40, "GrpCatalog")

    add_edge("c0",  "Router",     "CatPage",    "Каталог")
    add_edge("c1",  "CatPage",    "Filter")
    add_edge("c2",  "Filter",     "HasResults")
    add_edge("c3",  "HasResults", "NoResults",   "Нет")
    add_edge("c3b", "NoResults",  "Filter",      "",       edge_back)
    add_edge("c4",  "HasResults", "ProdCard",    "Да")
    add_edge("c5",  "ProdCard",   "AddBtn")
    add_edge("c6",  "AddBtn",     "CatPage",     "Нет",    edge_back)
    add_edge("c7",  "AddBtn",     "SaveCart",     "Да")

    # ========================================
    # BLOCK 3 — CART & ORDER (center-right, x=630..900)
    # ========================================
    BX3 = 630
    add_node("GrpCart", "Корзина и Оформление заказа", block_cart, BX3, BY1, BW+20, BH+60)

    add_node("CartPage",    "Просмотр корзины\n(товары, кол-во, сумма)", process_style, 55, 40,  170, 55, "GrpCart")
    add_node("CartEmpty",   "Корзина\nпуста?",          decision_style,  60, 130, 150, 70,  "GrpCart")
    add_node("EditQty",     "Изменение\nколичества / удаление", process_style, 55, 240, 170, 50, "GrpCart")
    add_node("IsAuthCart",  "Авторизован?",             decision_style,  60, 325, 150, 70,  "GrpCart")
    add_node("DelivInput",  "Ввод данных\nдоставки",     io_style,       65, 430, 150, 50,  "GrpCart")
    add_node("PayChoice",   "Выбор способа\nоплаты",     io_style,       65, 510, 150, 50,  "GrpCart")
    add_node("CreateOrder", "Создание заказа",           process_style,  70, 580, 140, 40,  "GrpCart")

    add_edge("cr0",  "Router",      "CartPage",   "Корзина")
    add_edge("cr0b", "SaveCart",    "CartPage",    "",        edge_back)
    add_edge("cr1",  "CartPage",    "CartEmpty")
    add_edge("cr1b", "CartEmpty",   "CatPage",     "Да",     edge_back)
    add_edge("cr2",  "CartEmpty",   "EditQty",     "Нет")
    add_edge("cr3",  "EditQty",     "IsAuthCart",   "Оформить")
    add_edge("cr4",  "IsAuthCart",  "LoginPage",    "Нет",    edge_back)
    add_edge("cr5",  "IsAuthCart",  "DelivInput",   "Да")
    add_edge("cr6",  "DelivInput",  "PayChoice")
    add_edge("cr7",  "PayChoice",   "CreateOrder")

    # Below groups — Payment result
    add_node("PayProc",   "Обработка\nоплаты",    process_style,  700, 1000, 150, 50)
    add_node("PayOk",     "Оплата\nуспешна?",     decision_style, 700, 1090, 150, 80)
    add_node("OrdOk",     "Заказ подтверждён\n(confirmed)",   process_style, 700, 1210, 150, 50)
    add_node("OrdFail",   "Заказ отменён\n(cancelled)",       end_style,     500, 1110, 140, 50)
    add_node("EndOk",     "Конец\n(Успешно)",     start_style, 700, 1310, 140, 50)

    add_edge("p1", "CreateOrder", "PayProc")
    add_edge("p2", "PayProc",    "PayOk")
    add_edge("p3", "PayOk",      "OrdFail",   "Нет")
    add_edge("p4", "PayOk",      "OrdOk",     "Да")
    add_edge("p5", "OrdOk",      "EndOk")

    # ========================================
    # BLOCK 4 — ADMIN (right, x=950..1220)
    # ========================================
    BX4 = 960
    add_node("GrpAdmin", "Панель Администратора", block_admin, BX4, BY1, BW, BH)

    add_node("AdminCheck", "Роль =\nAdmin?",            decision_style, 55, 40, 160, 70,  "GrpAdmin")
    add_node("AccessDeny", "Доступ\nзапрещён",          end_style,      80, 150, 120, 45,  "GrpAdmin")
    add_node("AdminDash",  "Панель управления\n(Dashboard)", process_style, 55, 220, 160, 50, "GrpAdmin")
    add_node("AdminAct",   "Действие?",                 decision_style, 55, 310, 160, 70,  "GrpAdmin")
    add_node("MngProd",    "Управление товарами\n(CRUD)", admin_style,   55, 420, 160, 50,  "GrpAdmin")
    add_node("MngOrd",     "Управление заказами\n(статусы)", admin_style, 55, 500, 160, 50, "GrpAdmin")

    add_edge("ad0", "Router",      "AdminCheck",  "Админ")
    add_edge("ad1", "AdminCheck",  "AccessDeny",  "Нет")
    add_edge("ad2", "AccessDeny",  "Home",        "",         edge_back)
    add_edge("ad3", "AdminCheck",  "AdminDash",   "Да")
    add_edge("ad4", "AdminDash",   "AdminAct")
    add_edge("ad5", "AdminAct",    "MngProd",     "Товары")
    add_edge("ad6", "AdminAct",    "MngOrd",      "Заказы")

    # ========================================
    # DATABASE at the bottom center
    # ========================================
    add_node("DB", "База Данных\nAutoPartsDB\n(MS SQL Server)", db_style, 340, 1180, 180, 100)

    # DB connections (dashed)
    add_edge("db1", "ValidCreds",  "DB", "users",          edge_back)
    add_edge("db2", "OrderHist",   "DB", "orders",         edge_back)
    add_edge("db3", "Filter",      "DB", "products",       edge_back)
    add_edge("db4", "SaveCart",    "DB", "carts",           edge_back)
    add_edge("db5", "CreateOrder", "DB", "orders",          edge_back)
    add_edge("db6", "MngProd",     "DB", "products",        edge_back)
    add_edge("db7", "MngOrd",      "DB", "orders",          edge_back)

    tree = ET.ElementTree(mxfile)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    create_flowchart('C:/Users/Lenovo/Desktop/Korse_work/full_system_flowchart_v2.drawio')
    print("Done!")
