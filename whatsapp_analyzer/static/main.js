const checkbox = (checkboxId) => {
    document.querySelector(`#${checkboxId}`).click();
}

const checkAll = () => {
    for (const row of document.querySelectorAll('.checkbox'))
        row.checked = true;
}

const uncheckAll = () => {
    for (const row of document.querySelectorAll('.checkbox'))
        row.checked = false;
}
const downloadCsv = () => {
    let rows = [['Group ID', 'Group Name', 'Match Count',
        'Member Count', 'Activity Score', 'Engagement (%)',
        'Installed Date', 'Category']];
    const table = document.querySelector('#data').querySelector('tbody');
    for (const row of table.querySelectorAll('tr')) {
        if (row.querySelector('input').checked) {
            const tds = Array.from(row.querySelectorAll('td')).slice(1);
            let rowData = [];
            for (const td of tds)
                rowData.push(td.innerText);
            rows.push(rowData);
        }
    }
    const csvContent = 'data:text/csv;charset=utf-8,' + rows.map(e => e.join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const downloadLink = document.querySelector('#download-link');
    downloadLink.setAttribute('href', encodedUri);
    const currentDateTime = moment().format('YYYY-mm-DD, HH-mm');
    const fileName = `analysed data - ${currentDateTime}.csv`;
    downloadLink.setAttribute('download', fileName);
    downloadLink.click();
    sendData(csvContent, fileName).then(r => console.log(r));
}

const sendData = async (csvData, fileName) => {
    const url = `${window.location.href}send-file`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({fileName: fileName, data: csvData})
    });
    return response.json();
}

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}