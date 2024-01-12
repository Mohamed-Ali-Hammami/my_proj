// static/main.js
document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    socket.on('update_data', function (data) {
        console.log('Received data:', data);
        const tableBody = document.getElementById('data-body');
        tableBody.innerHTML = '';

        if (Array.isArray(data) && data.length > 0) {
            console.log('Properties of the first item:', Object.keys(data[0]));
        }

        data.forEach((item) => {
            const row = document.createElement('tr');
            const propertiesToShow = ['symbol', 'price_change', 'price_change_percent', 'bid_price', 'ask_price','weighted_avg_price',
            'prev_day_close_price','current_day_close_price','close_trade_quantity','bid_quantity','ask_quantity','open_price','high_price',
            'low_price','bid_volume', 'ask_volume','open_time','close_time','first_trade_id','last_trade_id','total_trades','total_gains'];

            propertiesToShow.forEach((prop) => {
                const cell = document.createElement('td');
                cell.textContent = item[prop];
                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
    });
});

