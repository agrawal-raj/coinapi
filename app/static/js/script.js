document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    let currentPage = 1;
    let currentCurrency = 'usd';
    let currentPerPage = 25;
    let allCoinsData = [];
    
    // DOM Elements
    const tableBody = document.getElementById('cryptoTableBody');
    const searchInput = document.getElementById('searchInput');
    const currencySelect = document.getElementById('currencySelect');
    const perPageSelect = document.getElementById('perPageSelect');
    const refreshBtn = document.getElementById('refreshBtn');
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const lastUpdatedSpan = document.querySelector('.last-updated');
    
    // Initialize
    fetchData();
    
    // Event Listeners
    refreshBtn.addEventListener('click', fetchData);
    searchInput.addEventListener('input', filterCoins);
    currencySelect.addEventListener('change', function() {
        currentCurrency = this.value;
        fetchData();
    });
    perPageSelect.addEventListener('change', function() {
        currentPerPage = parseInt(this.value);
        currentPage = 1;
        fetchData();
    });
    prevPageBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });
    nextPageBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const maxPage = Math.ceil(allCoinsData.length / currentPerPage);
        if (currentPage < maxPage) {
            currentPage++;
            renderTable();
        }
    });
    
    // Functions
    async function fetchData() {
        try {
            showLoading(true);
            const response = await fetch(`/api/v3/coins/markets?vs_currency=${currentCurrency}&per_page=${currentPerPage}&page=${currentPage}`);
            allCoinsData = await response.json();
            renderTable();
            updateLastUpdated();
            showLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            showLoading(false);
            alert('Failed to fetch data. Please try again.');
        }
    }
    
    function renderTable() {
        tableBody.innerHTML = '';
        
        const startIdx = (currentPage - 1) * currentPerPage;
        const endIdx = startIdx + currentPerPage;
        const coinsToDisplay = allCoinsData.slice(startIdx, endIdx);
        
        coinsToDisplay.forEach(coin => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${coin.market_cap_rank}</td>
                <td>
                    <img src="${coin.image}" alt="${coin.name}" class="coin-logo">
                    <span class="coin-name">${coin.name}</span>
                    <span class="coin-symbol">${coin.symbol}</span>
                </td>
                <td>${formatCurrency(coin.current_price, currentCurrency)}</td>
                <td class="price-change ${coin.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}">
                    ${coin.price_change_percentage_24h >= 0 ? '+' : ''}${coin.price_change_percentage_24h.toFixed(2)}%
                </td>
                <td>${formatCurrency(coin.market_cap, currentCurrency)}</td>
                <td><canvas class="sparkline-chart" data-values="[0,2,5,9,5,10,3]"></canvas></td>
            `;
            tableBody.appendChild(row);
        });
        
        currentPageSpan.textContent = currentPage;
        renderSparklines();
    }
    
    function filterCoins() {
        const searchTerm = searchInput.value.toLowerCase();
        const filteredData = allCoinsData.filter(coin => 
            coin.name.toLowerCase().includes(searchTerm) || 
            coin.symbol.toLowerCase().includes(searchTerm)
        );
        
        tableBody.innerHTML = '';
        filteredData.forEach(coin => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${coin.market_cap_rank}</td>
                <td>
                    <img src="${coin.image}" alt="${coin.name}" class="coin-logo">
                    <span class="coin-name">${coin.name}</span>
                    <span class="coin-symbol">${coin.symbol}</span>
                </td>
                <td>${formatCurrency(coin.current_price, currentCurrency)}</td>
                <td class="price-change ${coin.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}">
                    ${coin.price_change_percentage_24h >= 0 ? '+' : ''}${coin.price_change_percentage_24h.toFixed(2)}%
                </td>
                <td>${formatCurrency(coin.market_cap, currentCurrency)}</td>
                <td><canvas class="sparkline-chart" data-values="[0,2,5,9,5,10,3]"></canvas></td>
            `;
            tableBody.appendChild(row);
        });
        
        renderSparklines();
    }
    
    function formatCurrency(value, currency) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency.toUpperCase(),
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(value);
    }
    
    function renderSparklines() {
        document.querySelectorAll('.sparkline-chart').forEach(canvas => {
            const values = JSON.parse(canvas.getAttribute('data-values'));
            const ctx = canvas.getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array(values.length).fill(''),
                    datasets: [{
                        data: values,
                        borderColor: '#0d6efd',
                        borderWidth: 1,
                        fill: false,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { display: false },
                        y: { display: false }
                    }
                }
            });
        });
    }
    
    function updateLastUpdated() {
        const now = new Date();
        lastUpdatedSpan.textContent = `Last updated: ${now.toLocaleTimeString()}`;
    }
    
    function showLoading(show) {
        if (show) {
            refreshBtn.innerHTML = '<div class="loading-spinner"></div>';
            refreshBtn.disabled = true;
        } else {
            refreshBtn.innerHTML = '<i class="bi bi-arrow-clockwise"></i> Refresh';
            refreshBtn.disabled = false;
        }
    }
});