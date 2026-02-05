const userInputElement = document.getElementById('user_input');
const searchButton = document.getElementById('search_button');
const resultsElement = document.getElementById('results');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');
const actionsElement = document.getElementById('actions');
const btnDownloadJson = document.getElementById('btn_download_json');
const btnDownloadExcel = document.getElementById('btn_download_excel');

let currentSearchData = null;

async function performSearch() {
    const user_input = userInputElement.value.trim();

    if (!user_input) {
        showError('Prosím zadejte vyhledávací dotaz');
        return;
    }

    hideError();
    resultsElement.innerHTML = '';
    actionsElement.style.display = 'none';
    currentSearchData = null;

    showLoading();
    searchButton.disabled = true;

    try {
        const response = await fetch(`/api/search?user_input=${encodeURIComponent(user_input)}`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Chyba při vyhledávání');
        }

        const search_response = await response.json();

        currentSearchData = search_response;

        displayResults(search_response);

        if (search_response.results.length > 0) {
            actionsElement.style.display = 'flex';
        }

    } catch (error) {
        showError(`Chyba: ${error.message}`);
    } finally {
        hideLoading();
        searchButton.disabled = false;
    }
}

function downloadJson() {
    if (!currentSearchData) return;

    const jsonString = JSON.stringify(currentSearchData, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    a.download = `search_results_${timestamp}.json`;

    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function downloadExcel() {
    if (!currentSearchData) return;

    const originalText = btnDownloadExcel.textContent;
    btnDownloadExcel.textContent = 'Stahuji...';
    btnDownloadExcel.disabled = true;

    try {
        const response = await fetch('/api/export/excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentSearchData)
        });

        if (!response.ok) {
            throw new Error('Chyba při generování Excel souboru');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;

        const contentDisposition = response.headers.get('Content-Disposition');
        let filename = 'search_results.xlsx';
        if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(contentDisposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }

        a.download = filename;
        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Download failed:', error);
        alert('Nepodařilo se stáhnout Excel soubor: ' + error.message);
    } finally {
        btnDownloadExcel.textContent = originalText;
        btnDownloadExcel.disabled = false;
    }
}

function displayResults(search_response) {
    if (search_response.results.length === 0) {
        resultsElement.innerHTML = '<p style="text-align: center; color: #666;">Žádné výsledky nenalezeny</p>';
        return;
    }

    search_response.results.forEach(result => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';

        resultItem.innerHTML = `
            <div class="result-header">
                <span class="result-position">${result.position}</span>
                <a href="${escapeHtml(result.url)}" target="_blank" class="result-title">${escapeHtml(result.title)}</a>
            </div>
            <div class="result-url">${escapeHtml(result.url)}</div>
            ${result.snippet ? `<div class="result-snippet">${escapeHtml(result.snippet)}</div>` : ''}
        `;

        resultsElement.appendChild(resultItem);
    });
}

function showLoading() {
    loadingElement.classList.add('active');
}

function hideLoading() {
    loadingElement.classList.remove('active');
}

function showError(message) {
    errorElement.textContent = message;
    errorElement.classList.add('active');
}

function hideError() {
    errorElement.classList.remove('active');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

searchButton.addEventListener('click', performSearch);
btnDownloadJson.addEventListener('click', downloadJson);
btnDownloadExcel.addEventListener('click', downloadExcel);

userInputElement.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

userInputElement.focus();
