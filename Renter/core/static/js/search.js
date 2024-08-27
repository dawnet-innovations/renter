

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const tableBody = document.getElementById('table-body');

    searchInput.addEventListener('input', () => {
        const searchValue = searchInput.value.toLowerCase();
        console.log(searchValue)
        const rows = tableBody.querySelectorAll('tr');

        rows.forEach(row => {
            const cells = row.querySelectorAll('td, th');
            let rowContainsSearchTerm = false;
            console.log(cells)

            cells.forEach(cell => {
                if (cell.textContent.toLowerCase().includes(searchValue)) {
                    rowContainsSearchTerm = true;
                }
            });
            console.log(rowContainsSearchTerm)

            if (rowContainsSearchTerm) {
                row.classList.remove('hidden');
            } else {
                row.classList.add('hidden');
            }
        });
    });
});