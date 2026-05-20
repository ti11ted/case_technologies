// Массив для хранения заказов
let orders = [];

// Получаем форму добавления заказа
const orderForm = document.getElementById("orderForm");

// Получаем тело таблицы, куда будут добавляться строки
const ordersTable = document.getElementById("ordersTable");

// Получаем кнопку очистки таблицы
const clearButton = document.getElementById("clearButton");

// При загрузке страницы получаем сохраненные заказы из localStorage
window.addEventListener("load", function () {
    const savedOrders = localStorage.getItem("atelierOrders");

    if (savedOrders) {
        orders = JSON.parse(savedOrders);
    } else {
        orders = [
            {
                clientName: "Иванова Мария Сергеевна",
                phone: "+7-913-111-22-33",
                service: "Ушить платье",
                orderDate: "2026-05-01",
                status: "В работе",
                price: 1500
            },
            {
                clientName: "Петрова Анна Викторовна",
                phone: "+7-913-222-33-44",
                service: "Подшить брюки",
                orderDate: "2026-05-02",
                status: "Готов",
                price: 800
            }
        ];
    }

    renderTable();
});

// Обрабатываем отправку формы
orderForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const order = {
        clientName: document.getElementById("clientName").value,
        phone: document.getElementById("phone").value,
        service: document.getElementById("service").value,
        orderDate: document.getElementById("orderDate").value,
        status: document.getElementById("status").value,
        price: Number(document.getElementById("price").value)
    };

    orders.push(order);
    saveOrders();
    renderTable();
    orderForm.reset();
    document.getElementById("price").value = 1500;
});

// Очищаем все записи
clearButton.addEventListener("click", function () {
    if (confirm("Удалить все записи из таблицы?")) {
        orders = [];
        saveOrders();
        renderTable();
    }
});

// Сохраняем заказы в localStorage браузера
function saveOrders() {
    localStorage.setItem("atelierOrders", JSON.stringify(orders));
}

// Выводим записи в таблицу
function renderTable() {
    ordersTable.innerHTML = "";

    orders.forEach(function (order, index) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${order.clientName}</td>
            <td>${order.phone}</td>
            <td>${order.service}</td>
            <td>${formatDate(order.orderDate)}</td>
            <td>${order.status}</td>
            <td>${order.price} руб.</td>
            <td>
                <button class="deleteButton" onclick="deleteOrder(${index})">
                    Удалить
                </button>
            </td>
        `;

        ordersTable.appendChild(row);
    });
}

// Удаляем одну запись по номеру
function deleteOrder(index) {
    orders.splice(index, 1);
    saveOrders();
    renderTable();
}

// Преобразуем дату из формата yyyy-mm-dd в dd.mm.yyyy
function formatDate(dateText) {
    if (!dateText) {
        return "";
    }

    const parts = dateText.split("-");
    return `${parts[2]}.${parts[1]}.${parts[0]}`;
}
