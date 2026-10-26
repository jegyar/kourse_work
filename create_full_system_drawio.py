import xml.etree.ElementTree as ET

def create_flowchart(filepath):
    mxfile = ET.Element('mxfile', version="14.6.13")
    diagram = ET.SubElement(mxfile, 'diagram', id="full_system", name="Full System Flow")
    mxGraphModel = ET.SubElement(diagram, 'mxGraphModel', dx="1200", dy="1000", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1800", pageHeight="1400", math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, 'root')
    
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    start_style = "shape=ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;strokeWidth=2;"
    process_style = "shape=rectangle;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;strokeWidth=1.5;"
    admin_style = "shape=rectangle;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;strokeWidth=1.5;"
    decision_style = "shape=rhombus;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=1.5;"
    db_style = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;strokeWidth=2;"
    edge_style = "endArrow=classic;html=1;rounded=0;strokeWidth=1.5;strokeColor=#4D4D4D;"
    edge_dashed = "endArrow=classic;html=1;rounded=0;dashed=1;strokeWidth=1.5;strokeColor=#808080;"

    def add_node(node_id, value, style, x, y, w, h):
        cell = ET.SubElement(root, 'mxCell', id=node_id, value=value, style=style, vertex="1", parent="1")
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})
        
    def add_edge(edge_id, source, target, label="", style=edge_style, exitX=None, exitY=None, entryX=None, entryY=None):
        cell = ET.SubElement(root, 'mxCell', id=edge_id, value=label, style=style, edge="1", parent="1", source=source, target=target)
        geo = ET.SubElement(cell, 'mxGeometry', relative="1", **{'as': 'geometry'})
        if exitX is not None and exitY is not None:
            cell.set('style', style + f"exitX={exitX};exitY={exitY};exitDx=0;exitDy=0;")
        if entryX is not None and entryY is not None:
            cell.set('style', cell.get('style') + f"entryX={entryX};entryY={entryY};entryDx=0;entryDy=0;")

        if label:
            label_cell = ET.SubElement(root, 'mxCell', id=f"lbl_{edge_id}", value=label, style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];backgroundColor=#ffffff;", vertex="1", connectable="0", parent=edge_id)
            ET.SubElement(label_cell, 'mxGeometry', relative="1", **{'as': 'geometry'})

    # Nodes
    add_node("Start", "Вход на сайт\n(Начало)", start_style, 740, 50, 120, 50)
    
    add_node("Home", "Главная страница\n(Навигация)", process_style, 740, 150, 140, 60)
    add_node("Action", "Раздел?", decision_style, 740, 260, 140, 80)
    
    # Auth Branch
    add_node("AuthBranch", "Блок Авторизации", process_style, 300, 350, 140, 50)
    add_node("CheckLogin", "Уже\nавторизован?", decision_style, 290, 450, 160, 80)
    add_node("LoginForm", "Вход / Регистрация", process_style, 100, 465, 140, 50)
    add_node("Profile", "Личный кабинет", process_style, 300, 580, 140, 50)
    add_node("OrderHistory", "История заказов", process_style, 300, 680, 140, 50)
    
    # Catalog Branch
    add_node("CatalogBranch", "Блок Каталога", process_style, 600, 350, 140, 50)
    add_node("SearchFilter", "Поиск и Фильтрация", process_style, 600, 465, 140, 50)
    add_node("ProductCard", "Карточка товара", process_style, 600, 580, 140, 50)
    add_node("AddToCart", "Добавление в корзину", process_style, 600, 680, 140, 50)
    
    # Cart Branch
    add_node("CartBranch", "Блок Корзины", process_style, 900, 350, 140, 50)
    add_node("CartView", "Просмотр корзины", process_style, 900, 465, 140, 50)
    add_node("IsAuthOrder", "Авторизован?", decision_style, 890, 565, 160, 80)
    add_node("CheckoutFlow", "Оформление заказа\n(Оплата, Доставка)", process_style, 900, 680, 140, 50)
    add_node("PaymentApi", "API Платежей", db_style, 1150, 675, 120, 60)
    add_node("OrderResult", "Успешно / Ошибка", process_style, 900, 780, 140, 50)
    
    # Admin Branch
    add_node("AdminBranch", "Панель\nАдминистратора", admin_style, 1300, 350, 140, 50)
    add_node("IsAdminRole", "Проверка\nроли Admin", decision_style, 1290, 450, 160, 80)
    add_node("AdminProducts", "Управление товарами", admin_style, 1200, 580, 140, 50)
    add_node("AdminOrders", "Управление заказами", admin_style, 1400, 580, 140, 50)
    
    # Database
    add_node("Database", "База Данных\nAutoPartsDB", db_style, 740, 950, 140, 90)

    # Main Edges
    add_edge("e1", "Start", "Home")
    add_edge("e2", "Home", "Action")
    
    add_edge("e_act1", "Action", "AuthBranch", "Профиль")
    add_edge("e_act2", "Action", "CatalogBranch", "Каталог")
    add_edge("e_act3", "Action", "CartBranch", "Корзина")
    add_edge("e_act4", "Action", "AdminBranch", "Управление")
    
    # Auth
    add_edge("a1", "AuthBranch", "CheckLogin")
    add_edge("a2", "CheckLogin", "LoginForm", "Нет")
    add_edge("a3", "LoginForm", "Profile", "Успешно")
    add_edge("a4", "CheckLogin", "Profile", "Да")
    add_edge("a5", "Profile", "OrderHistory")
    
    # Catalog
    add_edge("c1", "CatalogBranch", "SearchFilter")
    add_edge("c2", "SearchFilter", "ProductCard")
    add_edge("c3", "ProductCard", "AddToCart")
    add_edge("c4", "AddToCart", "CartBranch", "Перейти в корзину", edge_dashed)
    
    # Cart
    add_edge("cr1", "CartBranch", "CartView")
    add_edge("cr2", "CartView", "IsAuthOrder", "Оформить")
    add_edge("cr3", "IsAuthOrder", "LoginForm", "Нет", edge_dashed)
    add_edge("cr4", "IsAuthOrder", "CheckoutFlow", "Да")
    add_edge("cr5", "CheckoutFlow", "PaymentApi", "Вызов", edge_dashed)
    add_edge("cr6", "PaymentApi", "OrderResult", "Ответ", edge_dashed)
    add_edge("cr7", "CheckoutFlow", "OrderResult")
    add_edge("cr8", "OrderResult", "OrderHistory", "Мои заказы", edge_dashed)
    
    # Admin
    add_edge("ad1", "AdminBranch", "IsAdminRole")
    add_edge("ad2", "IsAdminRole", "Home", "Отказ", edge_dashed)
    add_edge("ad3", "IsAdminRole", "AdminProducts", "Да")
    add_edge("ad4", "IsAdminRole", "AdminOrders", "Да")

    # DB Integrations (dashed lines pointing to DB)
    add_edge("db1", "LoginForm", "Database", "Users", edge_dashed)
    add_edge("db2", "OrderHistory", "Database", "Orders", edge_dashed)
    add_edge("db3", "SearchFilter", "Database", "Products", edge_dashed)
    add_edge("db4", "AddToCart", "Database", "Cart", edge_dashed)
    add_edge("db5", "CheckoutFlow", "Database", "Orders, Trans", edge_dashed)
    add_edge("db6", "AdminProducts", "Database", "CRUD", edge_dashed)
    add_edge("db7", "AdminOrders", "Database", "CRUD", edge_dashed)

    tree = ET.ElementTree(mxfile)
    tree.write(filepath, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    create_flowchart('C:/Users/Lenovo/Desktop/Korse_work/full_system_flowchart.drawio')
    print("Full system diagram created!")
