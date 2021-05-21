document.addEventListener('DOMContentLoaded', function () {
    fetch('https://www.kingslayer.cc/nodejs/getAll')
    .then(response => response.json())
    .then(data => loadHTMLTable(data['data']));
    
});

 const searchBtn = document.querySelector('#search-btn');

 searchBtn.onclick = function() {
     const searchValue = document.querySelector('#search-input').value;
 
     fetch('https://www.kingslayer.cc/nodejs/search/' + searchValue)
     .then(response => response.json())
     .then(data => loadHTMLTable(data['data']));
 }

function loadHTMLTable(data) {
    const table = document.querySelector('table tbody');

    if (data.length === 0) {
        table.innerHTML = "<tr><td class='no-data' colspan='16'>No Data</td></tr>";
        return;
    }

    let tableHtml = "";

    data.forEach(function ({id, user, algo, gpu, temp, fan, speed, share, core, mem, power, eff, logtime, uptime, energy, gpunr}) {
        tableHtml += "<tr>";
        tableHtml += `<td>${id}</td>`;
        tableHtml += `<td>${user}</td>`;
        tableHtml += `<td>${algo}</td>`;
        tableHtml += `<td>${gpu}</td>`;
        tableHtml += `<td>${temp}</td>`;
        tableHtml += `<td>${fan}</td>`;
        tableHtml += `<td>${speed}</td>`;
        tableHtml += `<td>${share}</td>`;
        tableHtml += `<td>${core}</td>`;
        tableHtml += `<td>${mem}</td>`;
        tableHtml += `<td>${power}</td>`;
        tableHtml += `<td>${eff}</td>`;
        tableHtml += `<td>${logtime}</td>`;
        tableHtml += `<td>${uptime}</td>`;
        tableHtml += `<td>${energy}</td>`;
        tableHtml += `<td>${gpunr}</td>`;
        tableHtml += "</tr>";
    });
     table.innerHTML = tableHtml;
     

}
