document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("steam-form");
    const historyButton = document.getElementById("history-button");
    const resultDiv = document.getElementById("result");
    const historyDiv = document.getElementById("history");

    // Функция для извлечения SteamID из ссылки
    function extractSteamId(input) {
        const profileRegex = /https?:\/\/steamcommunity\.com\/profiles\/(\d+)/;
        const match = input.match(profileRegex);
        if (match) {
            return match[1]; // Возвращаем найденный SteamID
        }
        return input; // Если это не ссылка, возвращаем оригинальный ввод
    }

    // Обработка формы для запроса SteamID
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        let steamId = document.getElementById("steam-id").value.trim();
        steamId = extractSteamId(steamId); // Преобразуем ссылку в SteamID, если нужно

        try {
            const response = await fetch(`/api/steam/${steamId}`);
            if (!response.ok) {
                throw new Error("Ошибка в поле ввода. Пожалуйста убедитесь в правильности ввода SteamID/ссылки на профиль. P.S. Если в последнем слэше ссылки на профиль отсутсвуют цифры (SteamID), то результат получить невозможно.");
            }
            const data = await response.json();
            resultDiv.innerHTML = `
                <h2>Стоимость игр в библиотеке</h2>
                <p>Итог: ${data.total_cost} руб.</p>
                <p>Последнее обновление: ${data.last_updated}</p>
            `;
        } catch (error) {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });

    // Обработка кнопки "История запросов"
    historyButton.addEventListener("click", async () => {
        try {
            const response = await fetch(`/api/history/`);
            if (!response.ok) {
                throw new Error("Failed to fetch history.");
            }
            const data = await response.json();
            if (data.length === 0) {
                historyDiv.innerHTML = `<p>No recent requests found.</p>`;
                return;
            }

            historyDiv.innerHTML = `
                <h2>История запросов</h2>
                <table>
                    <thead>
                        <tr>
                            <th>SteamID</th>
                            <th>Итоговая стоимость</th>
                            <th>Последние обновление</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data
                            .map(
                                (item) => `
                                <tr>
                                    <td>${item.steam_id}</td>
                                    <td>${item.total_cost} руб.</td>
                                    <td>${item.last_updated}</td>
                                </tr>
                            `
                            )
                            .join("")}
                    </tbody>
                </table>
            `;
        } catch (error) {
            historyDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });
});
